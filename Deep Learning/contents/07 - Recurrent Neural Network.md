---
subject: Deep Learning
chapter: 7
tags: [ds, deep-learning, rnn, lstm, gru, bptt, perplexity, zipf, language-model, gradient-clipping]
source: "Zhang, Lipton, Li & Smola, *Dive into Deep Learning*, ch. 9 (Recurrent Neural Networks) and §10.1–10.4 (LSTM, GRU, Deep RNNs, Bidirectional RNNs)"
---

# Recurrent Neural Network

D2L ch. 9 and §10.1–10.4: sequence models, tokenization, language models and perplexity, the RNN, backpropagation through time and gradient clipping, then LSTM, GRU, deep and bidirectional RNNs. Each section gives the idea, the analysis, D2L's code and its printed outputs.

## 📘 Main Knowledge

### 1. Sequence models (§9.1)

Sequence data are not IID: order carries information. Autoregressive models factor the joint probability:
$$P(x_1,\dots,x_T)=\prod_{t=1}^{T}P(x_t\mid x_{t-1},\dots,x_1)$$

A Markov model of order $n-1$ keeps only the last $n-1$ tokens. A latent autoregressive model keeps a summary $h_{t-1}$ of the whole past.

- D2L notes that predicting forward is usually easier than predicting backward. That is why bidirectional models suit text (where the whole sequence is known) but not forecasting.
- Multi-step prediction feeds the model its own outputs, so errors compound, often badly.
- D2L ex. 9.1.2 (picking stocks by past returns) is a distribution-shift problem: the past sample is conditioned on survival ([[03 - Logistic Regression|ch. 03]] §11).

**The sine-wave experiment (§9.1.3–9.1.4).** 1000 points $x_t=\sin(0.01t)+\epsilon$, $\epsilon\sim\mathcal N(0,0.2^2)$. Treat it as a Markov model of order $\tau=4$: features $[x_{t-4},\dots,x_{t-1}]$, label $x_t$, giving $T-\tau=996$ examples (the first $\tau$ lack history and are dropped); train a linear regression on the first 600, 5 epochs, `lr=0.01`.

```python
class Data(d2l.DataModule):
    def __init__(self, batch_size=16, T=1000, num_train=600, tau=4):
        self.save_hyperparameters()
        self.time = torch.arange(1, T + 1, dtype=torch.float32)
        self.x = torch.sin(0.01 * self.time) + torch.randn(T) * 0.2

def get_dataloader(self, train):
    features = [self.x[i : self.T-self.tau+i] for i in range(self.tau)]
    self.features = torch.stack(features, 1)
    self.labels = self.x[self.tau:].reshape((-1, 1))
    i = slice(0, self.num_train) if train else slice(self.num_train, None)
    return self.get_tensorloader([self.features, self.labels], train, i)
```

**One-step** predictions look good up to $t=1000$. **Multi-step**: having seen only up to $x_{604}$, predict $\hat x_{605}=f(x_{601},\dots,x_{604})$, then $\hat x_{606}=f(x_{602},x_{603},x_{604},\hat x_{605})$ and so on, feeding predictions back as inputs. This fails: predictions decay to a constant after a few steps. Errors compound: if step 1 has error $\epsilon_1=\epsilon$, step 2 has $\epsilon_2=\epsilon+c\epsilon_1$, and so on (like weather forecasts beyond 24 hours). Comparing $k=1,4,16,64$-step predictions over the whole series, 4-step predictions still look good and anything longer is almost useless.

### 2. Text to tokens (§9.2)

Pipeline: load text, tokenize, build a vocabulary (token → index), convert. D2L uses *The Time Machine*, keeping only letters and spaces in lower case.

| | vocabulary | sequence length | notes |
|---|---|---|---|
| characters | tiny (28 here: 26 letters, space, `<unk>`) | long (173,428) | no unknown tokens; must learn spelling |
| words | tens of thousands or more | short | meaningful tokens; long tail of rare words |
| word pieces | tunable | medium | the modern compromise |

D2L prints `(173428, 28)`. Rare tokens below `min_freq` and unseen tokens become `<unk>`, losing information; word vocabularies need it often, character vocabularies almost never, which is one reason subword tokenization is standard.

**Code (§9.2).**

```python
class TimeMachine(d2l.DataModule):
    def _download(self):
        fname = d2l.download(d2l.DATA_URL + 'timemachine.txt', self.root,
                             '090b5e7e70c295757f55df93cb0a180b9691891a')
        with open(fname) as f:
            return f.read()
    def _preprocess(self, text):               # letters only, lower case
        return re.sub('[^A-Za-z]+', ' ', text).lower()
    def _tokenize(self, text):                 # characters
        return list(text)

class Vocab:
    def __init__(self, tokens=[], min_freq=0, reserved_tokens=[]):
        if tokens and isinstance(tokens[0], list):          # flatten 2-D lists
            tokens = [token for line in tokens for token in line]
        counter = collections.Counter(tokens)
        self.token_freqs = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        self.idx_to_token = list(sorted(set(['<unk>'] + reserved_tokens + [
            token for token, freq in self.token_freqs if freq >= min_freq])))
        self.token_to_idx = {token: idx for idx, token in enumerate(self.idx_to_token)}
    def __len__(self):
        return len(self.idx_to_token)
    def __getitem__(self, tokens):
        if not isinstance(tokens, (list, tuple)):
            return self.token_to_idx.get(tokens, self.unk)
        return [self.__getitem__(token) for token in tokens]
    def to_tokens(self, indices):
        if hasattr(indices, '__len__') and len(indices) > 1:
            return [self.idx_to_token[int(index)] for index in indices]
        return self.idx_to_token[indices]
    @property
    def unk(self):
        return self.token_to_idx['<unk>']

def build(self, raw_text, vocab=None):
    tokens = self._tokenize(self._preprocess(raw_text))
    if vocab is None: vocab = Vocab(tokens)
    corpus = [vocab[token] for token in tokens]
    return corpus, vocab
```

The raw text starts `'The Time Machine, by H. G. Wells [1898]...'`; after preprocessing `'the time machine by h g wells i the time traveller for so it '`. Indices are assigned in **sorted** token order, so space is 0, `<unk>` is 1 and `'a'` is 2; the first ten characters `t h e ␣ t i m e ␣ m` map to `[21, 9, 6, 0, 21, 10, 14, 6, 0, 14]`. Nothing is lost: `to_tokens` maps back. "Baby needs a new pair of shoes" is 7 word tokens or 30 character tokens (vocabulary of all 256 ASCII characters).

### 3. Why counting n-grams does not scale (§9.3.1)

An $n$-gram model stores $|\mathcal V|^n$ counts:

| $n$ | 28 characters | fp32 | 10,000 words | fp32 |
|---|---|---|---|---|
| 1 | 28 | 112 B | $10^4$ | 39 KB |
| 2 | 784 | 3.06 KB | $10^8$ | 381 MB |
| 3 | 21,952 | 85.75 KB | $10^{12}$ | 3.64 TB |
| 5 | $1.72\times10^7$ | 65.65 MB | $10^{20}$ | 347 EB |
| 10 | $2.96\times10^{14}$ | 1.05 PB | $10^{40}$ | |

The RNN in §6 has 2,876 parameters whatever the context length.

**Laplace smoothing** adds pseudo-counts:
$$\hat P(x)=\frac{n(x)+\epsilon_1/m}{n+\epsilon_1},\qquad \hat P(x'\mid x)=\frac{n(x,x')+\epsilon_2\hat P(x')}{n(x)+\epsilon_2}$$
($\epsilon\to0$: no smoothing; $\epsilon\to\infty$: uniform). D2L's objections: rare n-grams are still poorly estimated, all counts must be stored, word meaning is ignored ("cat" and "feline" share nothing), and long sequences are usually new.

### 4. Zipf's law (§9.2.5)

$$n_i\propto \frac{1}{i^{\alpha}}\iff \log n_i=-\alpha\log i+c$$

Fitting D2L's printed top-10 frequencies (D2L ex. 9.2.2):

| | $\alpha$ (ranks 1–10) | $R^2$ | $\alpha$ (ranks 2–10) | $R^2$ |
|---|---|---|---|---|
| unigram | 0.7184 | 0.948 | 0.7693 | 0.915 |
| bigram | 0.5703 | 0.965 | 0.4777 | 0.965 |
| trigram | 0.6447 | 0.931 | 0.5145 | 0.890 |

D2L says n-grams follow Zipf "with a smaller exponent". Smaller than unigrams: confirmed. A steady decrease with $n$: not supported (trigram > bigram), but ten head ranks cannot settle it (declined discrepancy D9).

Stop words fill 10/10 of the top unigrams, 9/10 of the top bigrams, but only 1/10 of the top trigrams. The top trigram is *the time traveller* (59 occurrences, vs 2,261 for *the*). Longer n-grams carry more specific information and are much rarer, which is exactly the problem for count-based models.

### 5. Perplexity and partitioning (§9.3.2–9.3.3)

$$\mathrm{ppl}=\exp\left(-\frac1n\sum_{t=1}^{n}\log P(x_t\mid x_{t-1},\dots,x_1)\right)$$

It is the reciprocal geometric mean of the probabilities given to the actual tokens, roughly "how many equally likely choices the model is guessing among".

| model | perplexity |
|---|---|
| perfect | 1 |
| uniform over $\vert \mathcal V\vert =28$ | 28 |
| assigns 0 to the truth | $\infty$ |

Any useful model must beat the uniform value. In bits: $\log_2 28=4.8074$ per character; Shannon (1951) estimated English at about 1.1 bits per character (perplexity ≈ 2.14). So the useful range for a character model is 28 → 2.14 (13.1×), or 4.81 → 1.1 bits. Perplexity, not accuracy, is used because the next token is often genuinely uncertain and perplexity scores the whole distribution.

**Partitioning**: each epoch drops a random offset at the start, then cuts the corpus into length-$n$ subsequences; targets are inputs shifted by one. The random offset varies the boundaries between epochs.

**What D2L's loader actually does** (§9.3.3 code):

```python
def __init__(self, batch_size, num_steps, num_train=10000, num_val=5000):
    super(d2l.TimeMachine, self).__init__()
    self.save_hyperparameters()
    corpus, self.vocab = self.build(self._download())
    array = torch.tensor([corpus[i:i+num_steps+1]
                          for i in range(len(corpus)-num_steps)])
    self.X, self.Y = array[:,:-1], array[:,1:]

def get_dataloader(self, train):
    idx = slice(0, self.num_train) if train else slice(
        self.num_train, self.num_train + self.num_val)
    return self.get_tensorloader([self.X, self.Y], train, idx)
```

With `num_steps=10` a printed batch shows `Y` equal to `X` shifted by one token.

> [!note] Prose vs code (discrepancy D12)
> The prose describes a random offset $d\in[0,n)$ each epoch and $m=\lfloor(T-d)/n\rfloor$ non-overlapping subsequences covering the corpus. The code instead builds every overlapping window (stride 1, no offset) and keeps windows starting at positions 0–9,999 for training and 10,000–14,999 for validation. Training therefore sees only tokens 0–10,031 (5.8% of the 173,428), consecutive training windows share 31 of 32 tokens, and 32 tokens (10,000–10,031) appear in both splits. The loader is fine for a demo, but D2L's perplexities measure a small slice of the book.

### 6. The RNN (§9.4–9.6)

$$\mathbf H_t=\phi(\mathbf X_t\mathbf W_{xh}+\mathbf H_{t-1}\mathbf W_{hh}+\mathbf b_h),\qquad \mathbf O_t=\mathbf H_t\mathbf W_{hq}+\mathbf b_q$$

Compared with an MLP layer, the only addition is $\mathbf H_{t-1}\mathbf W_{hh}$, and the same weights are used at every step. A hidden *state* is carried across time steps; a hidden *layer* sits between input and output. In code, $\mathbf X_t\mathbf W_{xh}+\mathbf H_{t-1}\mathbf W_{hh}$ is one matrix product of $[\mathbf X_t,\mathbf H_{t-1}]$ with stacked weights.

Parameters (D2L ex. 10.2.3). One gate block costs $dh+h^2+h$:

| cell | blocks | recurrent parameters |
|---|---|---|
| RNN | 1 | $dh+h^2+h$ |
| GRU | 3 ($\mathbf R,\mathbf Z,\tilde{\mathbf H}$) | $3(dh+h^2+h)$ |
| LSTM | 4 ($\mathbf I,\mathbf F,\mathbf O,\tilde{\mathbf C}$) | $4(dh+h^2+h)$ |

| $d$ | $h$ | RNN | GRU | LSTM |
|---|---|---|---|---|
| 28 | 32 | 1,952 | 5,856 | 7,808 |
| 28 | 256 | 72,960 | 218,880 | 291,840 |
| 256 | 256 | 131,328 | 393,984 | 525,312 |

The ratio is always 1:3:4. With the output layer, the Time Machine model ($d=q=28$, $h=32$) has 2,876 (RNN), 6,780 (GRU), 8,732 (LSTM) parameters.

**Concatenation check (§9.4.2).** With $\mathbf X$ $(3\times1)$, $\mathbf W_{xh}$ $(1\times4)$, $\mathbf H$ $(3\times4)$, $\mathbf W_{hh}$ $(4\times4)$: `matmul(X, W_xh) + matmul(H, W_hh)` equals `matmul(cat((X, H), 1), cat((W_xh, W_hh), 0))` (D2L's printouts agree to the fourth decimal).

**Character-level language model.** For the text "machine" (batch size 1), the input is "machin" and the target "achine": at step 3 the output $\mathbf O_3$ depends on "m", "a", "c" and is scored by cross-entropy against "h". Bengio et al. (2003) first used a neural network for language modelling.

**From scratch (§9.5).** Inputs have shape (num_steps, batch_size, num_inputs) so the loop runs over time; the state starts at zeros; the activation is tanh.

```python
class RNNScratch(d2l.Module):
    def __init__(self, num_inputs, num_hiddens, sigma=0.01):
        super().__init__()
        self.save_hyperparameters()
        self.W_xh = nn.Parameter(torch.randn(num_inputs, num_hiddens) * sigma)
        self.W_hh = nn.Parameter(torch.randn(num_hiddens, num_hiddens) * sigma)
        self.b_h = nn.Parameter(torch.zeros(num_hiddens))
    def forward(self, inputs, state=None):
        if state is None:
            state = torch.zeros((inputs.shape[1], self.num_hiddens),
                                device=inputs.device)
        else:
            state, = state
        outputs = []
        for X in inputs:
            state = torch.tanh(torch.matmul(X, self.W_xh) +
                               torch.matmul(state, self.W_hh) + self.b_h)
            outputs.append(state)
        return outputs, state

class RNNLMScratch(d2l.Classifier):
    def __init__(self, rnn, vocab_size, lr=0.01):
        super().__init__()
        self.save_hyperparameters()
        self.init_params()
    def init_params(self):
        self.W_hq = nn.Parameter(torch.randn(
            self.rnn.num_hiddens, self.vocab_size) * self.rnn.sigma)
        self.b_q = nn.Parameter(torch.zeros(self.vocab_size))
    def training_step(self, batch):
        l = self.loss(self(*batch[:-1]), batch[-1])
        self.plot('ppl', torch.exp(l), train=True)     # perplexity = exp(mean CE)
        return l
    def one_hot(self, X):                              # (num_steps, batch, vocab)
        return F.one_hot(X.T, self.vocab_size).type(torch.float32)
    def output_layer(self, rnn_outputs):
        outputs = [torch.matmul(H, self.W_hq) + self.b_q for H in rnn_outputs]
        return torch.stack(outputs, 1)
    def forward(self, X, state=None):
        embs = self.one_hot(X)
        rnn_outputs, _ = self.rnn(embs, state)
        return self.output_layer(rnn_outputs)
```

Why one-hot: feeding the index as a number would make tokens 45 ("their") and 46 ("said") look similar. A one-hot input times $\mathbf W_{xh}$ simply picks row $i$, so it is the same as a learned embedding per token (D2L ex. 9.5.3).

**Training.** `TimeMachine(batch_size=1024, num_steps=32)`, 32 hidden units, `lr=1`, 100 epochs, `gradient_clip_val=1`. That is $\lceil10{,}000/1024\rceil=10$ batches per epoch, 1000 updates in total. The state starts at zero for every batch, so the model never uses more than 32 characters of history (D2L ex. 9.5.1–2: `num_steps` controls it).

**Decoding.** Feed a prefix to warm up the state without emitting output, then predict greedily, feeding each prediction back:

```python
def predict(self, prefix, num_preds, vocab, device=None):
    state, outputs = None, [vocab[prefix[0]]]
    for i in range(len(prefix) + num_preds - 1):
        X = torch.tensor([[outputs[-1]]], device=device)
        embs = self.one_hot(X)
        rnn_outputs, state = self.rnn(embs, state)
        if i < len(prefix) - 1:                       # warm-up period
            outputs.append(vocab[prefix[i + 1]])
        else:                                         # predict num_preds steps
            Y = self.output_layer(rnn_outputs)
            outputs.append(int(Y.argmax(axis=2).reshape(1)))
    return ''.join([vocab.idx_to_token[i] for i in outputs])
```

Greedy argmax tends to loop; D2L ex. 9.5.8 suggests sampling, sharpened by $q\propto P^\alpha$ with $\alpha>1$ ([[03 - Logistic Regression|ch. 03]] temperature).

**Concise (§9.6).** `nn.RNN(num_inputs, num_hiddens)` plus a `LazyLinear(vocab_size)` output layer whose result is swapped to (batch, steps, vocab):

```python
class RNN(d2l.Module):
    def __init__(self, num_inputs, num_hiddens):
        super().__init__()
        self.save_hyperparameters()
        self.rnn = nn.RNN(num_inputs, num_hiddens)
    def forward(self, inputs, H=None):
        return self.rnn(inputs, H)

class RNNLM(d2l.RNNLMScratch):
    def init_params(self):
        self.linear = nn.LazyLinear(self.vocab_size)
    def output_layer(self, hiddens):
        return self.linear(hiddens).swapaxes(0, 1)
```

Generated continuations of `'it has '` (20 characters):

| model | output |
|---|---|
| concise RNN, untrained | `it hassuussuussuussuus` |
| scratch RNN, trained | `it has is a mere and the t` |
| concise RNN, trained | `it has a mather a mather a` |

Comparable perplexity, faster code. Note PyTorch's recurrent layers keep **two** bias vectors ($\mathbf b_{ih}$ and $\mathbf b_{hh}$), so `nn.RNN(28, 32)` has 1,984 parameters, `nn.GRU` 5,952 and `nn.LSTM` 7,936, i.e. $h$ more per gate block than the scratch formulas above (checked).

### 7. Backpropagation through time (§9.7)

BPTT is backprop on the unrolled graph. Because weights are shared, each parameter's gradient is summed over all time steps. The hidden-state gradient is recursive:
$$\frac{\partial h_t}{\partial w_h}=\frac{\partial f}{\partial w_h}+\frac{\partial f}{\partial h_{t-1}}\frac{\partial h_{t-1}}{\partial w_h}$$
which unrolls to
$$\frac{\partial h_t}{\partial w_h}=\frac{\partial f}{\partial w_h}+\sum_{i=1}^{t-1}\left(\prod_{j=i+1}^{t}\frac{\partial f(x_j,h_{j-1},w_h)}{\partial h_{j-1}}\right)\frac{\partial f(x_i,h_{i-1},w_h)}{\partial w_h}$$

The product of $t-i$ Jacobians causes the trouble. With factor $\gamma$:

| $\gamma$ | $\gamma^{10}$ | $\gamma^{100}$ | $\gamma^{1000}$ |
|---|---|---|---|
| 0.90 | 0.3487 | $2.66\times10^{-5}$ | $1.75\times10^{-46}$ |
| 0.99 | 0.9044 | 0.3660 | $4.32\times10^{-5}$ |
| 1.00 | 1 | 1 | 1 |
| 1.01 | 1.105 | 2.705 | $2.10\times10^{4}$ |
| 1.10 | 2.594 | $1.38\times10^{4}$ | $2.47\times10^{41}$ |

To keep $\gamma^T$ within $[10^{-3},10^3]$, $\gamma$ must lie in $[0.501, 1.995]$ for $T=10$, $[0.933, 1.072]$ for $T=100$, and $[0.993116, 1.006932]$ (±0.693%) for $T=1000$. D2L notes sequences of over a thousand tokens are common.

Compared with the sigmoid MLP of [[04 - Neural Network|ch. 04]] §8 (factor ≤ 0.25, independent weights per layer), an RNN's factor can be above or below 1 and is the same matrix each step. So gradients can vanish or explode, and RNNs need two fixes: clipping and gating.

D2L's options: full computation (unstable, never used); truncation after $\tau$ steps (standard; D2L argues its bias toward short dependencies stabilizes training); randomized truncation (unbiased but rarely better).

**BPTT in detail (§9.7.2).** Take a linear RNN without biases: $\mathbf h_t=\mathbf W_{hx}\mathbf x_t+\mathbf W_{hh}\mathbf h_{t-1}$, $\mathbf o_t=\mathbf W_{qh}\mathbf h_t$, objective $L=\frac1T\sum_{t=1}^Tl(\mathbf o_t,y_t)$. Walking the graph backward:
$$\frac{\partial L}{\partial\mathbf o_t}=\frac1T\frac{\partial l(\mathbf o_t,y_t)}{\partial\mathbf o_t},\qquad \frac{\partial L}{\partial\mathbf W_{qh}}=\sum_{t=1}^T\frac{\partial L}{\partial\mathbf o_t}\mathbf h_t^\top,$$
$$\frac{\partial L}{\partial\mathbf h_T}=\mathbf W_{qh}^\top\frac{\partial L}{\partial\mathbf o_T},\qquad \frac{\partial L}{\partial\mathbf h_t}=\mathbf W_{hh}^\top\frac{\partial L}{\partial\mathbf h_{t+1}}+\mathbf W_{qh}^\top\frac{\partial L}{\partial\mathbf o_t}\quad(t\lt T),$$
which unrolls to
$$\frac{\partial L}{\partial\mathbf h_t}=\sum_{i=t}^T\left(\mathbf W_{hh}^\top\right)^{T-i}\mathbf W_{qh}^\top\frac{\partial L}{\partial\mathbf o_{T+t-i}}.$$
Then $\frac{\partial L}{\partial\mathbf W_{hx}}=\sum_t\frac{\partial L}{\partial\mathbf h_t}\mathbf x_t^\top$ and $\frac{\partial L}{\partial\mathbf W_{hh}}=\sum_t\frac{\partial L}{\partial\mathbf h_t}\mathbf h_{t-1}^\top$. (Checked against autograd on a random $d=3$, $h=4$, $q=2$, $T=6$ example.) Even this linear model contains large powers of $\mathbf W_{hh}^\top$: eigenvalues below 1 vanish, above 1 explode. Truncation can be implemented by **detaching** the state after a number of steps. The hidden-state gradients are stored and reused for both parameter gradients, which is why BPTT keeps all intermediate states in memory.

### 8. Gradient clipping (§9.5.3)

$$\mathbf g\leftarrow\min\left(1,\frac{\theta}{\|\mathbf g\|}\right)\mathbf g$$

The norm never exceeds $\theta$, gradients below $\theta$ are unchanged, and the direction is preserved. Justification: if $f$ is $L$-Lipschitz, one step changes $f$ by at most $L\eta\|\mathbf g\|$. At $\eta=0.1$, $L=1$, a gradient of norm 1000 could move the objective by 100; clipped at 1, by 0.1. It also limits any single minibatch's influence. D2L calls it "a hack": it is biased, and it does nothing for vanishing gradients.

**Code.** The norm is taken over all parameters concatenated into one vector:

```python
def clip_gradients(self, grad_clip_val, model):
    params = [p for p in model.parameters() if p.requires_grad]
    norm = torch.sqrt(sum(torch.sum((p.grad ** 2)) for p in params))
    if norm > grad_clip_val:
        for param in params:
            param.grad[:] *= grad_clip_val / norm
```

`Trainer.fit_epoch` calls it between `backward()` and `step()` when `gradient_clip_val > 0`. Shrinking the learning rate instead would also bound $L\eta\|\mathbf g\|$ without bias, but slows every step to guard against rare explosions. PyTorch: `torch.nn.utils.clip_grad_norm_`.

### 9. LSTM (§10.1)

Gates (sigmoid, values in $(0,1)$):
$$\mathbf I_t=\sigma(\mathbf X_t\mathbf W_{xi}+\mathbf H_{t-1}\mathbf W_{hi}+\mathbf b_i),\quad \mathbf F_t=\sigma(\mathbf X_t\mathbf W_{xf}+\mathbf H_{t-1}\mathbf W_{hf}+\mathbf b_f),\quad \mathbf O_t=\sigma(\mathbf X_t\mathbf W_{xo}+\mathbf H_{t-1}\mathbf W_{ho}+\mathbf b_o)$$
Input node: $\tilde{\mathbf C}_t=\tanh(\mathbf X_t\mathbf W_{xc}+\mathbf H_{t-1}\mathbf W_{hc}+\mathbf b_c)$.
$$\mathbf C_t=\mathbf F_t\odot\mathbf C_{t-1}+\mathbf I_t\odot\tilde{\mathbf C}_t,\qquad \mathbf H_t=\mathbf O_t\odot\tanh(\mathbf C_t)$$

The key derivative is $\partial\mathbf C_t/\partial\mathbf C_{t-1}=\mathbf F_t$, so the gradient along the cell is $\prod_j F_j$, controlled by the network. With $F=1$ it is exactly 1 for any length (the "constant error carousel"); with $F=1$, $I=0$ the cell keeps its value forever.

$F$ is a sigmoid, so it never reaches 1. Memory half-life $=\ln0.5/\ln F$:

| forget pre-activation $z$ | $F=\sigma(z)$ | half-life (steps) |
|---|---|---|
| 0 | 0.5 | 1 |
| 2 | 0.8808 | 5.5 |
| 4 | 0.9820 | 38.2 |
| 6 | 0.9975 | 280 |
| 8 | 0.99966 | 2,065 |

A 1,000-step half-life needs $z\approx7.3$. With zero bias (D2L's init) the half-life is one step, which is why practitioners often initialize the forget-gate bias to +1 or +2 (beyond D2L).

The output gate lets a cell store information without affecting the rest of the network until $\mathbf O_t$ opens.

**Code (§10.1).** Weights $\mathcal N(0,0.01^2)$, biases 0; only $\mathbf H$ goes to the output layer, $\mathbf C$ stays internal.

```python
class LSTMScratch(d2l.Module):
    def __init__(self, num_inputs, num_hiddens, sigma=0.01):
        super().__init__()
        self.save_hyperparameters()
        init_weight = lambda *shape: nn.Parameter(torch.randn(*shape) * sigma)
        triple = lambda: (init_weight(num_inputs, num_hiddens),
                          init_weight(num_hiddens, num_hiddens),
                          nn.Parameter(torch.zeros(num_hiddens)))
        self.W_xi, self.W_hi, self.b_i = triple()  # input gate
        self.W_xf, self.W_hf, self.b_f = triple()  # forget gate
        self.W_xo, self.W_ho, self.b_o = triple()  # output gate
        self.W_xc, self.W_hc, self.b_c = triple()  # input node

    def forward(self, inputs, H_C=None):
        if H_C is None:
            H = torch.zeros((inputs.shape[1], self.num_hiddens), device=inputs.device)
            C = torch.zeros((inputs.shape[1], self.num_hiddens), device=inputs.device)
        else:
            H, C = H_C
        outputs = []
        for X in inputs:
            I = torch.sigmoid(torch.matmul(X, self.W_xi) + torch.matmul(H, self.W_hi) + self.b_i)
            F = torch.sigmoid(torch.matmul(X, self.W_xf) + torch.matmul(H, self.W_hf) + self.b_f)
            O = torch.sigmoid(torch.matmul(X, self.W_xo) + torch.matmul(H, self.W_ho) + self.b_o)
            C_tilde = torch.tanh(torch.matmul(X, self.W_xc) + torch.matmul(H, self.W_hc) + self.b_c)
            C = F * C + I * C_tilde
            H = O * torch.tanh(C)
            outputs.append(H)
        return outputs, (H, C)
```

Trained like the RNN but `lr=4`, 50 epochs, clipping 1. Concise: `nn.LSTM(num_inputs, num_hiddens)`, state passed as the tuple `(H, C)`; it generates `it has the the the the the`. History: published 1997, prominent after competition wins in the mid-2000s, dominant for sequence learning from 2011 until Transformers (2017), which borrowed some of its ideas.

### 10. GRU (§10.2)

Two gates (Cho et al. 2014):
$$\mathbf R_t=\sigma(\mathbf X_t\mathbf W_{xr}+\mathbf H_{t-1}\mathbf W_{hr}+\mathbf b_r),\qquad \mathbf Z_t=\sigma(\mathbf X_t\mathbf W_{xz}+\mathbf H_{t-1}\mathbf W_{hz}+\mathbf b_z)$$
$$\tilde{\mathbf H}_t=\tanh(\mathbf X_t\mathbf W_{xh}+(\mathbf R_t\odot\mathbf H_{t-1})\mathbf W_{hh}+\mathbf b_h),\qquad \mathbf H_t=\mathbf Z_t\odot\mathbf H_{t-1}+(1-\mathbf Z_t)\odot\tilde{\mathbf H}_t$$

- $\mathbf R\to1$: vanilla RNN. $\mathbf R\to0$: candidate ignores the old state.
- $\mathbf Z\to1$: copy the old state and skip this step.
- The update is a convex combination, so the GRU cannot forget without writing, while the LSTM's $\mathbf F$ and $\mathbf I$ are independent. In exchange it has 25% fewer parameters, and D2L reports similar performance.

D2L: reset gates capture short-term dependencies, update gates long-term ones.

**Code (§10.2).**

```python
class GRUScratch(d2l.Module):
    def __init__(self, num_inputs, num_hiddens, sigma=0.01):
        super().__init__()
        self.save_hyperparameters()
        init_weight = lambda *shape: nn.Parameter(torch.randn(*shape) * sigma)
        triple = lambda: (init_weight(num_inputs, num_hiddens),
                          init_weight(num_hiddens, num_hiddens),
                          nn.Parameter(torch.zeros(num_hiddens)))
        self.W_xz, self.W_hz, self.b_z = triple()  # update gate
        self.W_xr, self.W_hr, self.b_r = triple()  # reset gate
        self.W_xh, self.W_hh, self.b_h = triple()  # candidate hidden state

    def forward(self, inputs, H=None):
        if H is None:
            H = torch.zeros((inputs.shape[1], self.num_hiddens), device=inputs.device)
        outputs = []
        for X in inputs:
            Z = torch.sigmoid(torch.matmul(X, self.W_xz) + torch.matmul(H, self.W_hz) + self.b_z)
            R = torch.sigmoid(torch.matmul(X, self.W_xr) + torch.matmul(H, self.W_hr) + self.b_r)
            H_tilde = torch.tanh(torch.matmul(X, self.W_xh) +
                                 torch.matmul(R * H, self.W_hh) + self.b_h)
            H = Z * H + (1 - Z) * H_tilde
            outputs.append(H)
        return outputs, H
```

Same training (`lr=4`, 50 epochs). Concise `nn.GRU(num_inputs, num_hiddens)` generates `it has of the fore and the`.

### 11. Deep and bidirectional RNNs (§10.3–10.4)

**Deep RNNs** stack layers: layer $\ell$'s state at time $t$ feeds layer $\ell+1$ at time $t$ and layer $\ell$ at $t+1$. Parameters $(dh+h^2+h)+(L-1)(2h^2+h)$ plus output; at $d=q=28$, $h=32$: 2,876, 4,956, 7,036, 11,196 for $L=1,2,3,5$.

**Bidirectional RNNs** run a forward and a backward RNN and concatenate their states:

| | one direction | bidirectional | ratio |
|---|---|---|---|
| RNN | 2,876 | 5,724 | 1.99× |
| GRU | 6,780 | 13,532 | 2.00× |
| LSTM | 8,732 | 17,436 | 2.00× |

A bidirectional model sees tokens after $t$. For next-token prediction this leaks the answer, and for forecasting the future is not available. Use it for tasks where the whole sequence is known: tagging, named-entity recognition, filling masked tokens (BERT's setting, not GPT's).

**Deep RNN code (§10.3).** Each layer is its own `RNNScratch`; layer $\ell$'s output sequence is layer $\ell+1$'s input:

```python
class StackedRNNScratch(d2l.Module):
    def __init__(self, num_inputs, num_hiddens, num_layers, sigma=0.01):
        super().__init__()
        self.save_hyperparameters()
        self.rnns = nn.Sequential(*[d2l.RNNScratch(
            num_inputs if i==0 else num_hiddens, num_hiddens, sigma)
            for i in range(num_layers)])
    def forward(self, inputs, Hs=None):
        outputs = inputs
        if Hs is None: Hs = [None] * self.num_layers
        for i in range(self.num_layers):
            outputs, Hs[i] = self.rnns[i](outputs, Hs[i])
            outputs = torch.stack(outputs, 0)
        return outputs, Hs

class GRU(d2l.RNN):                     # multilayer GRU
    def __init__(self, num_inputs, num_hiddens, num_layers, dropout=0):
        d2l.Module.__init__(self)
        self.save_hyperparameters()
        self.rnn = nn.GRU(num_inputs, num_hiddens, num_layers, dropout=dropout)
```

Two layers of 32 units, `lr=2`, 100 epochs; the 2-layer GRU generates `it has some about the time`. `dropout` applies between layers.

**Bidirectional (§10.4).** Context on both sides matters for tagging and for filling blanks: "I am ___." (happy), "I am ___ hungry." (not, very), "I am ___ hungry, and I can eat half a pig." ("not" no longer fits). Schuster & Paliwal (1997): run one RNN forward and one backward over the same input and concatenate:
$$\overrightarrow{\mathbf H}_t=\phi(\mathbf X_t\mathbf W^{(f)}_{xh}+\overrightarrow{\mathbf H}_{t-1}\mathbf W^{(f)}_{hh}+\mathbf b^{(f)}_h),\qquad \overleftarrow{\mathbf H}_t=\phi(\mathbf X_t\mathbf W^{(b)}_{xh}+\overleftarrow{\mathbf H}_{t+1}\mathbf W^{(b)}_{hh}+\mathbf b^{(b)}_h)$$
$\mathbf H_t=[\overrightarrow{\mathbf H}_t,\overleftarrow{\mathbf H}_t]\in\mathbb R^{n\times2h}$ and $\mathbf O_t=\mathbf H_t\mathbf W_{hq}+\mathbf b_q$ with $\mathbf W_{hq}\in\mathbb R^{2h\times q}$.

```python
class BiRNNScratch(d2l.Module):
    def __init__(self, num_inputs, num_hiddens, sigma=0.01):
        super().__init__()
        self.save_hyperparameters()
        self.f_rnn = d2l.RNNScratch(num_inputs, num_hiddens, sigma)
        self.b_rnn = d2l.RNNScratch(num_inputs, num_hiddens, sigma)
        self.num_hiddens *= 2           # output dimension doubles
    def forward(self, inputs, Hs=None):
        f_H, b_H = Hs if Hs is not None else (None, None)
        f_outputs, f_H = self.f_rnn(inputs, f_H)
        b_outputs, b_H = self.b_rnn(reversed(inputs), b_H)
        outputs = [torch.cat((f, b), -1) for f, b in zip(
            f_outputs, reversed(b_outputs))]
        return outputs, (f_H, b_H)
```

Concise: `nn.GRU(num_inputs, num_hiddens, bidirectional=True)` with `num_hiddens *= 2`. The backward outputs must be reversed again so that position $t$ pairs with position $t$. D2L: mostly useful for encoding sequences and estimating observations from both sides; costly to train because of the long gradient chains.

## ✏️ Exercises

> [!example]- **1.** *(Easy) Perplexity*
> **(a)** Probabilities 0.5, 0.25, 0.125, 0.125 on the actual tokens: perplexity? **(b)** The three anchor values and this corpus's bound. **(c)** Convert perplexity 28 and 2.14 to bits per character.
>
> ---
> **(a)** Mean NLL $=\frac14(0.6931+1.3863+2.0794+2.0794)=1.5596$; perplexity $e^{1.5596}=4.7568$.
>
> **(b)** 1 (perfect), 28 (uniform), $\infty$.
>
> **(c)** 4.8074 and 1.0977 bits. Perplexity 10 (3.32 bits) covers $(4.81-3.32)/(4.81-1.10)=40\%$ of that range, so the multiplicative scale overstates progress.

> [!example]- **2.** *(Easy–medium) Cell costs*
> **(a)** Parameters for RNN, GRU, LSTM with $d$ inputs, $h$ hidden. **(b)** At $d=28$, $h=256$. **(c)** Deep and bidirectional.
>
> ---
> **(a)** $dh+h^2+h$ per block; 1, 3, 4 blocks.
>
> **(b)** 72,960 / 218,880 / 291,840 (+ output layer).
>
> **(c)** Deep adds $(L-1)(2h^2+h)$; bidirectional roughly doubles. A bidirectional LSTM is about 8× a vanilla RNN's recurrent cost.

> [!example]- **3.** *(Medium) Read the implementation*
> D2L feeds `X = torch.ones((100, 2, 16))` (steps, batch, inputs) to `RNNScratch(16, 32)`, and trains the language model with `TimeMachine(batch_size=1024, num_steps=32)`.
> **(a)** Length and shapes of `outputs` and `state`? **(b)** Shape of `one_hot(X)` for a token batch `X` of shape (1024, 32) with 28 tokens, and why is it transposed? **(c)** Parameters of `RNNScratch(28, 32)` + output layer, and of `nn.RNN(28, 32)`? **(d)** How much history can the trained model use? **(e)** What fraction of the book does D2L's loader train on?
>
> ---
> **(a)** 100 outputs, each (2, 32); final state (2, 32).
>
> **(b)** (32, 1024, 28). `X.T` puts time first so `for X in inputs` loops over steps.
>
> **(c)** Scratch: $28\cdot32+32\cdot32+32=1{,}952$, plus output $32\cdot28+28=924$: 2,876. `nn.RNN(28, 32)` has two bias vectors: 1,984 (before the output layer).
>
> **(d)** At most 32 characters: the state is reset to zero for each batch and BPTT runs over 32 steps.
>
> **(e)** Windows start at 0–9,999, so tokens 0–10,031: 5.8% of 173,428 (D12).

> [!example]- **4.** *(Medium–hard) The BPTT window*
> **(a)** Gradient factor over $T$ steps with Jacobian magnitude $\gamma$? **(b)** Range of $\gamma$ keeping it in $[10^{-3},10^3]$ for $T=10,100,1000$. **(c)** Does clipping solve this?
>
> ---
> **(a)** $\gamma^T$, the same matrix each step.
>
> **(b)** $[10^{-3/T},10^{3/T}]$: $[0.501,1.995]$, $[0.933,1.072]$, $[0.993116,1.006932]$.
>
> **(c)** Only the exploding side. A gradient of $1.75\times10^{-46}$ cannot be rescaled into usefulness; vanishing needs the LSTM/GRU's additive path.

> [!example]- **5.** *(Hard) How long can an LSTM remember?*
> **(a)** $\partial\mathbf C_t/\partial\mathbf C_{t-1}$ and the gradient over $T$ steps. **(b)** Forget-gate pre-activation for a half-life of 100 and 1,000 steps. **(c)** Implication for initialization.
>
> ---
> **(a)** $\mathbf F_t$; the product $\prod_j F_j$, equal to 1 when $F=1$.
>
> **(b)** $F=0.5^{1/\text{half-life}}$, $z=\sigma^{-1}(F)$: 100 steps needs $F=0.99309$, $z=4.97$; 1,000 steps needs $F=0.999307$, $z=7.28$.
>
> **(c)** At zero bias $F=0.5$ and memory lasts one step, and the gradient that would teach longer memory is the one being forgotten. Initialize the forget bias positive (+1 or +2).

## 📝 Summary

- Sequences are not IID; autoregression factors the joint distribution and an RNN summarizes the past in a hidden state.
- Tokenization choice: characters (28 tokens, 173,428 long) vs words (large vocabulary, `<unk>`) vs subwords.
- n-gram counts grow as $|\mathcal V|^n$; an RNN's parameters do not depend on context length.
- Zipf exponents from D2L's data: 0.72 (unigram), 0.57 (bigram), 0.64 (trigram). Longer n-grams are more informative and rarer.
- Perplexity ranges from 1 to the vocabulary size (28); convert to bits to compare (4.81 uniform vs ~1.1 for English).
- An RNN adds $\mathbf H_{t-1}\mathbf W_{hh}$ to an MLP layer; RNN:GRU:LSTM parameters are 1:3:4.
- BPTT multiplies the same Jacobian $T$ times; at $T=1000$ it must be within 0.7% of 1 in magnitude.
- Clipping caps exploding gradients; gating (LSTM's $\partial\mathbf C_t/\partial\mathbf C_{t-1}=\mathbf F_t$) addresses vanishing, but $F\lt 1$ always, so long memory has to be learned (or helped by a positive forget bias).
- GRU merges forget and write into one gate; deep RNNs stack layers; bidirectional RNNs suit tagging, not prediction.
- Code pattern: inputs (steps, batch, features), loop over steps, one-hot inputs, `RNNLMScratch` for output and perplexity, `predict` with a warm-up prefix and greedy decoding; concise `nn.RNN`/`nn.GRU`/`nn.LSTM` (two bias vectors each). Training: batch 1024, 32 steps, clip 1.
- Multi-step prediction compounds errors: D2L's sine model is fine at 4 steps and useless beyond.
- Linear BPTT: $\partial L/\partial\mathbf h_t=\sum_i(\mathbf W_{hh}^\top)^{T-i}\mathbf W_{qh}^\top\partial L/\partial\mathbf o_{T+t-i}$: powers of $\mathbf W_{hh}$ cause vanishing and exploding.

## ⚠️ Important Notes

1. Do not use a bidirectional model for next-token prediction or forecasting; validation numbers will look great because of leakage.
2. Clipping does not help vanishing gradients.
3. A zero forget-gate bias means a one-step memory half-life at the start.
4. Report perplexity with the vocabulary size.
5. Perplexity drops look larger than the corresponding bit improvements.
6. Truncated BPTT cannot learn dependencies longer than the truncation length.
7. Shared weights receive gradients summed over time steps; averaging the loss over steps keeps the scale sensible.
8. Gating extends memory but does not remove the product; attention ([[08 - Sequence to Sequence|ch. 08]]) does.
9. Use a random offset when partitioning sequences.
10. If a task needs to clear state without taking in the current input, an LSTM can do that and a GRU cannot.
11. Character and word perplexities are not comparable; compare bits per character.
12. Modern neural models do not need stop-word removal.
13. Check the `<unk>` rate before blaming the model.
14. "2-layer LSTM with 256 units": 2 stacked layers, 256-dimensional hidden state.
15. Never feed token indices as numbers; use one-hot or embeddings.
16. Reversed sequences in a BiRNN must be reversed back before concatenating.
17. Greedy decoding repeats itself (`a mather a mather`); sampling or beam search ([[08 - Sequence to Sequence|ch. 08]]) helps.
18. D2L's loader trains on overlapping windows from 5.8% of the book (D12); a perplexity from it is not a whole-book result.
19. PyTorch recurrent layers have two biases per gate block; parameter counts differ from the textbook formula by $h$ per block.

> [!warning] Gaps in the source material
> - **Figures:** partitioning, the unrolled RNN, and LSTM/GRU diagrams are reconstructed from the prose. Lost: Zipf log–log plots (the exponents were fitted from the printed frequency lists instead) and all training/perplexity curves, so no perplexity results are quoted.
> - **Added by me:** Zipf fits (D2L ex. 9.2.2) and the stop-word counts; the $|\mathcal V|^n$ table; all parameter counts (ex. 10.2.3); the BPTT stability window and comparison with ch. 04; the clipping numbers; the forget-gate half-life analysis and positive-bias advice; Shannon's 1.1 bits/char; the explicit BERT/GPT leakage point; the GRU convex-combination remark.
> - **Declined discrepancy D9:** n-gram Zipf exponents are smaller than the unigram one but not monotone in $n$; ten ranks cannot decide.
> - **Also added by me:** the linear-BPTT check against autograd; PyTorch's two-bias parameter counts; the loader coverage figures and discrepancy D12; the Vocab index check.
> - **Lost:** the sine-wave and k-step prediction plots and all perplexity curves are images, so no perplexities are quoted; the generated strings are quoted as printed.
> - **Skipped:** plotting code. Machine translation and attention are in [[08 - Sequence to Sequence|ch. 08]].

**Previous:** [[06 - Object Detection]] · **Next:** [[08 - Sequence to Sequence]]
