"""Live CNN training visualizer. Trains a small CNN on sklearn digits and
streams loss / activations / weights to the browser over SSE."""
import json, queue, threading, time
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from sklearn.datasets import load_digits
from flask import Flask, Response, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=None)

# ---------------------------------------------------------------- pub/sub
SUBS, LOCK = [], threading.Lock()

def broadcast(obj):
    data = json.dumps(obj)
    with LOCK:
        for q in list(SUBS):
            try: q.put_nowait(data)
            except queue.Full: pass

# ---------------------------------------------------------------- model
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.c1 = nn.Conv2d(1, 8, 3, padding=1)
        self.c2 = nn.Conv2d(8, 16, 3, padding=1)
        self.f1 = nn.Linear(16 * 2 * 2, 32)
        self.f2 = nn.Linear(32, 10)

    def forward(self, x):
        a1 = F.relu(self.c1(x));  p1 = F.max_pool2d(a1, 2)
        a2 = F.relu(self.c2(p1)); p2 = F.max_pool2d(a2, 2)
        a3 = F.relu(self.f1(p2.flatten(1)))
        return self.f2(a3), a1, a2, a3

# ---------------------------------------------------------------- state
S = {"running": True, "lr": 0.01, "delay": 0.04, "reset": False,
     "opt": "adam", "bs": 32}

def make_opt(net):
    if S["opt"] == "sgd":
        return torch.optim.SGD(net.parameters(), lr=S["lr"])
    if S["opt"] == "momentum":
        return torch.optim.SGD(net.parameters(), lr=S["lr"], momentum=0.9)
    return torch.optim.Adam(net.parameters(), lr=S["lr"])

def q8(a):
    """quantize array to 0..255 ints for cheap transport"""
    a = np.asarray(a, dtype=np.float32)
    m = float(a.max()) or 1.0
    return (np.clip(a / m, 0, 1) * 255).astype(np.uint8).ravel().tolist()

def norm(a):
    a = np.asarray(a, dtype=np.float32)
    m = float(a.max()) or 1.0
    return [round(float(v), 4) for v in (a / m)]

def edges(net):
    w1 = net.c1.weight.detach().abs().mean((1, 2, 3))              # 8
    w2 = net.c2.weight.detach().mean((2, 3))                       # 16 x 8
    w3 = net.f1.weight.detach().view(32, 16, 4).mean(2)            # 32 x 16
    w4 = net.f2.weight.detach()                                    # 10 x 32
    r = lambda t: np.round(t.cpu().numpy(), 3).tolist()
    return {"t": "edges", "e1": r(w1), "e2": r(w2), "e3": r(w3), "e4": r(w4)}

def trainer():
    d = load_digits()
    X = torch.tensor(d.images / 16.0, dtype=torch.float32).unsqueeze(1)
    Y = torch.tensor(d.target, dtype=torch.long)
    g = torch.Generator().manual_seed(0)
    idx = torch.randperm(len(X), generator=g)
    Xtr, Ytr, Xte, Yte = X[idx[:1500]], Y[idx[:1500]], X[idx[1500:]], Y[idx[1500:]]

    net, opt, step, epoch, testacc = None, None, 0, 0, 0.0
    def fresh():
        nonlocal net, opt, step, epoch, testacc
        torch.manual_seed(1)
        net = Net(); opt = make_opt(net)
        step = epoch = 0; testacc = 0.0
        broadcast({"t": "reset"}); broadcast(edges(net))
    fresh()
    cur_opt = S["opt"]

    while True:
        if S["reset"]:
            S["reset"] = False; fresh(); cur_opt = S["opt"]
        if S["opt"] != cur_opt:
            cur_opt = S["opt"]; opt = make_opt(net)
        if not S["running"]:
            time.sleep(0.1); continue

        for gp in opt.param_groups: gp["lr"] = S["lr"]
        b = torch.randint(0, len(Xtr), (S["bs"],))
        xb, yb = Xtr[b], Ytr[b]
        out, a1, a2, a3 = net(xb)
        loss = F.cross_entropy(out, yb)
        opt.zero_grad(); loss.backward(); opt.step()
        step += 1

        if step % 47 == 0:  # cheap periodic "epoch" + held-out check
            epoch += 1
            with torch.no_grad():
                testacc = (net(Xte)[0].argmax(1) == Yte).float().mean().item()

        if step % 2 == 0:
            with torch.no_grad():
                acc = (out.argmax(1) == yb).float().mean().item()
                p = F.softmax(out[0], 0).numpy()
                broadcast({
                    "t": "step", "step": step, "epoch": epoch,
                    "loss": round(float(loss), 4), "acc": round(acc, 3),
                    "test": round(testacc, 3),
                    "n1": norm(a1[0].abs().mean((1, 2))),
                    "n2": norm(a2[0].abs().mean((1, 2))),
                    "n3": norm(a3[0]),
                    "img": q8(xb[0, 0]),
                    "m1": q8(a1[0]), "m2": q8(a2[0]),
                    "probs": [round(float(v), 4) for v in p],
                    "label": int(yb[0]), "pred": int(out[0].argmax()),
                })
        if step % 20 == 0:
            broadcast(edges(net))
        time.sleep(S["delay"])

# ---------------------------------------------------------------- routes
@app.route("/")
def index(): return send_from_directory(app.root_path, "index.html")

@app.route("/stream")
def stream():
    q = queue.Queue(maxsize=8)
    with LOCK: SUBS.append(q)
    def gen():
        try:
            while True:
                yield "data: %s\n\n" % q.get()
        finally:
            with LOCK:
                if q in SUBS: SUBS.remove(q)
    return Response(gen(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

@app.route("/control", methods=["POST"])
def control():
    j = request.get_json(force=True)
    if "running" in j: S["running"] = bool(j["running"])
    if "lr" in j:      S["lr"] = float(j["lr"])
    if "delay" in j:   S["delay"] = float(j["delay"])
    if "opt" in j:     S["opt"] = str(j["opt"])
    if "bs" in j:      S["bs"] = max(1, min(256, int(j["bs"])))
    if j.get("reset"): S["reset"] = True
    return jsonify(ok=True, **{k: S[k] for k in ("running", "lr", "delay", "opt", "bs")})

if __name__ == "__main__":
    threading.Thread(target=trainer, daemon=True).start()
    print("http://127.0.0.1:5055")
    app.run("127.0.0.1", 5055, threaded=True, debug=False)
