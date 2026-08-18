---
subject: AI Test — ôn thi
tags: [ai, on-thi, tong-hop, cheatsheet]
source: "https://hungbil.github.io/AI-TEST/ — tổng hợp từ 1380 câu của 23 đề"
---

# AI Test — Kiến thức cần nhớ

> [!info] Nguồn
> Tổng hợp từ **https://hungbil.github.io/AI-TEST/**: 23 đề × 60 câu = **1380 câu** (1265 trắc nghiệm, 69 tự luận, 46 code). Mọi công thức và con số dưới đây đều rút ra từ chính lời giải trong bộ đề, và **đã được kiểm tra lại bằng tính toán**.
>
> Trang tự ghi rõ đây là **bộ ôn tập cộng đồng, không phải đề chính thức hay đề bị lộ**. Dùng để luyện dạng bài, đừng học tủ.
>
> Ngân hàng câu hỏi tự luận: [[AI Test - Ngan hang cau tu luan]]

## 🗺️ Cấu trúc đề

| Module | Nội dung | Số câu (trên 1380) | Tỷ trọng |
|---|---|---|---|
| **A** | Xác suất & Đại số tuyến tính | 360 | 26% |
| **B** | Python, NumPy, Pandas, Euclid, gọi API | 480 | 35% |
| **C** | ML cơ bản, đánh giá mô hình, AI sản phẩm, RAG | 356 | 26% |
| **D** | Responsible AI, privacy, logic | 184 | 13% |

**Mỗi đề 60 câu, 90 phút, 100 điểm.** Câu trắc nghiệm 1–2 điểm; câu code 2–4 điểm (Module B); câu tự luận 4/6/8 điểm (Module C và D).

> [!tip] Chiến thuật thời gian
> 60 câu / 90 phút = **1,5 phút/câu**. Nhưng câu tự luận 8 điểm không thể làm trong 1,5 phút. Thực tế: **làm nhanh phần A và B trước** (đa số là công thức máy móc, ~1 phút/câu), dồn thời gian còn lại cho các câu 6–8 điểm ở C/D.
>
> Cộng cả 23 đề, phần tự luận có 452 điểm, trong đó **các câu 8 điểm chiếm 39 × 8 = 312 điểm, tức 69%**. Trung bình mỗi đề có khoảng **20 điểm tự luận trên thang 100** — bỏ trắng một câu 8 điểm là mất 8% tổng điểm, bằng 8 câu trắc nghiệm.

---

## 📗 MODULE A — Xác suất & Đại số tuyến tính

### A1. Xác suất cơ bản

| Công thức | Ghi nhớ |
|---|---|
| $P(A\mid B)=\dfrac{P(A\cap B)}{P(B)}$ | **Dạng câu hỏi phổ biến nhất của cả module** — cho $P(A\cap B)$ và $P(B)$, chia là xong |
| $P(A\cup B)=P(A)+P(B)-P(A\cap B)$ | Trừ phần giao để không đếm hai lần |
| $A,B$ độc lập $\iff P(A\cap B)=P(A)P(B)$ | **Cách kiểm tra:** nhân hai xác suất rồi so với giao |
| $P(\bar A)=1-P(A)$ | |
| $P(\text{ít nhất một})=1-P(\text{không có cái nào})$ | Mẹo tiết kiệm thời gian nhất trong đề |

**Ví dụ mẫu (lặp nhiều lần):** $P(A\cap B)=0{,}15$, $P(B)=0{,}50$ → $P(A\mid B)=0{,}15/0{,}50=\mathbf{0{,}3}$.

**"Ít nhất một":** phép thử độc lập có xác suất thất bại $2/5$, làm 2 lần → $P(\text{ít nhất 1 thành công}) = 1-(2/5)^2 = 1-4/25 = \mathbf{21/25}$.

### A2. Rút không hoàn lại (dạng túi bi)

Túi có 5 bi đỏ, 4 bi xanh, rút 2 bi **không hoàn lại**:

- **Cả hai đỏ:** $\dfrac{5}{9}\times\dfrac{4}{8}=\dfrac{20}{72}=\mathbf{\dfrac{5}{18}}$ — mẫu số giảm dần 9 → 8.
- **Hai bi khác màu:** phải tính **cả hai thứ tự**: $2\times\dfrac{5\times4}{9\times8}=\dfrac{40}{72}=\mathbf{\dfrac{5}{9}}$.

> [!warning] Lỗi sai kinh điển
> Quên nhân 2 khi đề hỏi "khác màu" / "một đỏ một xanh". Không hoàn lại thì **mẫu số phải giảm**; nếu có hoàn lại thì mẫu giữ nguyên.

### A3. Tổ hợp & nhị thức

$$C(n,k)=\binom{n}{k}=\frac{n!}{k!(n-k)!}$$

- Chọn 2 người từ 6, không phân biệt thứ tự: $C(6,2)=\mathbf{15}$.
- Tung đồng xu công bằng $n$ lần, đúng $k$ lần ngửa: $\dfrac{C(n,k)}{2^n}$.
  - 3 lần, đúng 2 ngửa: $C(3,2)/8=3/8$
  - 4 lần, đúng 1 ngửa: $C(4,1)/16=4/16=\mathbf{1/4}$
  - 4 lần, đúng 2 ngửa: $C(4,2)/16=6/16=\mathbf{3/8}$

**Nhớ nhanh:** $C(n,0)=C(n,n)=1$; $C(n,1)=n$; $C(4,2)=6$; $C(5,2)=10$; $C(6,2)=15$; $C(6,3)=20$.

### A4. Kỳ vọng & phương sai

$$E[X]=\sum_x x\,P(X=x),\qquad \operatorname{Var}(X)=E[X^2]-E[X]^2$$

- $X\in\{0,1,2\}$ với xác suất $(0{,}25;\,0{,}5;\,0{,}25)$ → $E[X]=0(0{,}25)+1(0{,}5)+2(0{,}25)=\mathbf{1}$.
- **Bernoulli:** $E[X]=p$, $\operatorname{Var}(X)=p(1-p)$. Với $p=0{,}25$: $\operatorname{Var}=0{,}25\times0{,}75=\mathbf{0{,}1875}\approx0{,}188$.

> [!note] Mẹo với phân phối đối xứng
> Nếu bảng xác suất đối xứng quanh một giá trị (như $0{,}25/0{,}5/0{,}25$), kỳ vọng **chính là giá trị ở giữa** — khỏi tính.

### A5. Bayes & xác suất toàn phần

$$P(A\mid B)=\frac{P(B\mid A)P(A)}{P(B)},\qquad P(B)=\sum_i P(B\mid A_i)P(A_i)$$

**Quy trình 3 bước không bao giờ sai:**
1. Viết ra $P(A)$, $P(\bar A)$, $P(B\mid A)$, $P(B\mid \bar A)$.
2. Tính mẫu số bằng xác suất toàn phần: $P(B)=P(B\mid A)P(A)+P(B\mid\bar A)P(\bar A)$.
3. Chia.

> [!warning] Bẫy tỷ lệ cơ sở (base rate)
> Bệnh hiếm + test rất chính xác → xác suất **thật sự** mắc bệnh khi test dương vẫn có thể rất thấp, vì $P(A)$ ở tử số quá nhỏ. Đừng trả lời theo trực giác "test chính xác 99% nên chắc chắn mắc bệnh".

### A6. Ma trận 2×2 — toàn bộ những gì cần thuộc

Với $A=\begin{pmatrix}a&b\\c&d\end{pmatrix}$:

| Đại lượng | Công thức |
|---|---|
| Định thức | $\det(A)=ad-bc$ |
| Nghịch đảo | $A^{-1}=\dfrac{1}{ad-bc}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}$ |
| Vết (trace) | $\operatorname{tr}(A)=a+d$ |
| Chuyển vị | $A^\top$: đổi hàng thành cột |

**Các kết quả xuất hiện đi xuất hiện lại:**

- $A=[[2,1],[1,1]]$ → $\det=2\cdot1-1\cdot1=\mathbf{1}$, và $A^{-1}=[[1,-1],[-1,2]]$ (phần tử (1,1) $=d/\det=1$).
- $A=[[3,1],[2,1]]$ → $\det=3-2=\mathbf{1}$.
- $A=[[1,1],[1,2]]$ → $\det=1$, $A^{-1}=[[2,-1],[-1,1]]$.
- $A=[[1,2],[3,6]]$ → $\det=6-6=\mathbf{0}$ ⇒ **suy biến, không có nghịch đảo**, và $\operatorname{rank}=1$.

> [!important] Ba câu hỏi luôn có cùng một lời giải
> "Có nghịch đảo không?", "Có suy biến không?", "Hệ có nghiệm duy nhất không?" — **cả ba đều chỉ hỏi $\det \ne 0$?** Tính định thức trước, trả lời cả ba.

**Hạng (rank):** đếm số hàng độc lập tuyến tính. Nếu một hàng là bội của hàng kia → $\operatorname{rank}=1$.
- $[[1,2],[2,4]]$: hàng 2 = 2 × hàng 1 → rank 1.
- $[[1,2],[3,6]]$: hàng 2 = 3 × hàng 1 → rank 1.

### A7. Nhân ma trận

$$(AB)_{ij}=\text{hàng } i \text{ của } A \;\cdot\; \text{cột } j \text{ của } B$$

- $A=[[1,2],[3,4]]$, $B=[[2,1],[1,2]]$ → phần tử $(1,2)$ của $AB$ = $1\times1+2\times2=\mathbf{5}$.
- $A=[[2,1],[1,1]]$, $B=[[1,2],[3,1]]$ → $AB=[[5,5],[4,3]]$ nhưng $BA=[[4,3],[7,4]]$.

> [!warning] Nhân ma trận KHÔNG giao hoán
> $AB \ne BA$ nói chung. Đây là một câu hỏi riêng trong đề, và cặp $[[2,1],[1,1]]\times[[1,2],[3,1]]$ ở trên chính là ví dụ phản chứng được dùng.

**Các tính chất hay bị hỏi:**
- $AI=IA=A$ (nhân ma trận đơn vị không đổi gì).
- $D=\operatorname{diag}(2,3)$, $x=[2,3]$ → $Dx=[2\cdot2,\,3\cdot3]=[\mathbf{4},\mathbf{9}]$ — ma trận chéo nhân **từng phần tử tương ứng**.
- $(A+B)^\top=A^\top+B^\top$, nhưng $(AB)^\top=B^\top A^\top$ — **đảo thứ tự**.

### A8. Giải hệ phương trình

$Ax=b$: cộng/trừ hai phương trình để khử một ẩn.
- $x+y=3$, $2x-y=0$ → cộng: $3x=3$, $x=1$, $y=2$.
- $A=[[1,1],[2,-1]]$, $b=[4,2]$ → $x_1+x_2=4$, $2x_1-x_2=2$ → cộng: $3x_1=6$, $x=[\mathbf{2},\mathbf{2}]$.

---

## 📘 MODULE B — Python, NumPy, API (module lớn nhất, 35%)

### B1. Thuật toán Euclid — chắc chắn có trong đề

```python
def gcd(a, b):
    while b != 0:
        a, b = b, a % b   # gán đồng thời
    return a              # khi b == 0 thì a là GCD
```

Bản đệ quy: `return a if b == 0 else gcd(b, a % b)`

**Vết chạy phải thuộc lòng:**

| Bài | Các bước | GCD |
|---|---|---|
| $(252,105)$ | $252=2\cdot105+42$; $105=2\cdot42+21$; $42=2\cdot21+0$ | **21** |
| $(84,30)$ | $84=2\cdot30+24$; $30=1\cdot24+6$; $24=4\cdot6+0$ | **6** |
| $(48,18)$ | $48=2\cdot18+12$; $18=1\cdot12+6$; $12=2\cdot6+0$ | **6** |

- Sau **một** lần lặp từ $(252,105)$: $252 \bmod 105 = 42$, nên $(a,b)=(\mathbf{105},\mathbf{42})$.
- "Số chia cuối cùng khác 0" **chính là GCD**.
- **Độ phức tạp: $O(\log n)$** — số bước tăng theo logarit của số nhỏ hơn.

> [!warning] Hai lỗi cố ý được cài trong đề
> 1. Viết `a, b = a % b, b` (sai thứ tự) → vòng lặp không hội tụ. Đúng phải là **`a, b = b, a % b`**.
> 2. Viết `while b == 0:` thay vì `while b != 0:`, rồi `return b` thay vì `return a`.
>
> **Cách nhớ:** điều kiện là **`b != 0`**, cập nhật là **`(b, a % b)`**, trả về là **`a`**.

### B2. NumPy — shape, axis, broadcasting

**`axis` là chiều bị "gộp mất", không phải chiều được giữ.**

| Lệnh | Ý nghĩa | Ví dụ với `x = [[1,2,3],[4,5,6]]` (shape `(2,3)`) |
|---|---|---|
| `x.sum(axis=0)` | gộp theo **hàng** → tổng **từng cột** | `[5, 7, 9]`, shape `(3,)` |
| `x.sum(axis=1)` | gộp theo **cột** → tổng **từng hàng** | `[6, 15]`, shape `(2,)` |
| `x.mean(axis=1)` | trung bình **từng hàng** | `[2.0, 5.0]` |

Với `x.shape == (3,4)`: `x.sum(axis=0)` → shape `(4,)`; `x.sum(axis=1)` → shape `(3,)`.

> [!important] Mẹo nhớ axis không bao giờ sai
> **`axis=k` làm biến mất chiều thứ `k` của shape.** `(2,3)` với `axis=0` → `(3,)`. `(2,3)` với `axis=1` → `(2,)`. `(3,4)` với `axis=0` → `(4,)`.

**Slicing — điểm khác biệt quan trọng nhất:**

```python
x = np.arange(6).reshape(2, 3)   # [[0,1,2],
                                 #  [3,4,5]]

x[:, 1]      # → [1, 4]      shape (2,)   ← chỉ số NGUYÊN làm MẤT chiều
x[:, 1:2]    # → [[1],[4]]   shape (2,1)  ← SLICE GIỮ chiều
x[:, 0]      # → [0, 3]      shape (2,)
x[:, 0:1]    # → [[0],[3]]   shape (2,1)
x[:, 2:3]    # → [[2],[5]]   shape (2,1)
```

> [!warning] Đây là bẫy được lặp lại nhiều nhất trong Module B
> **Chỉ số nguyên `x[:, 1]` giảm chiều; slice `x[:, 1:2]` giữ chiều.** Đề hỏi "giá trị **và** shape" chính là để bắt lỗi này.

**Broadcasting:** mảng nhỏ được "kéo giãn" để khớp mảng lớn.
- `np.array([1,2,3]) + 2` → `[3,4,5]` (scalar broadcast tới mọi phần tử).
- `x` shape `(2,3)` cộng `v` shape `(3,)` → `v` được broadcast theo **từng hàng**.
- Quy tắc: so shape **từ phải sang trái**, mỗi chiều phải **bằng nhau hoặc bằng 1**.

**Boolean indexing:**
```python
x = np.array([1,2,3,4,5])
x[x % 2 == 0]   # → [2, 4]   giữ phần tử thoả điều kiện
x[x % 2 == 1]   # → [1, 3, 5]
```

**Khác:** `np.zeros((3,4)).shape` → `(3,4)`; `np.arange(6).reshape(2,3).ndim` → `2`.

### B3. Python thuần

| Đoạn code | Kết quả | Vì sao |
|---|---|---|
| `sum` của `range(5)` bỏ qua `i==3` bằng `continue` | **7** | $0+1+2+4$ (range(5) là 0..4) |
| `a=[0,1,2,3,4,5,6]; a[2:7:2]` | **`[2,4,6]`** | bắt đầu 2, dừng **trước** 7, bước 2 |
| `d={'x':1}; d['x']=d.get('x',0)+2` | **3** | `.get` trả 1 vì key tồn tại |
| `'a,b,,c'.split(',')` → `len` | **4** | `split` **giữ** phần tử rỗng: `['a','b','','c']` |

**Độ phức tạp:**
```python
for i in range(n):
    for j in range(i):   # → n(n-1)/2 lần ≈ O(n²)
```
- Kiểm tra `x in ...`: **`set` trung bình $O(1)$**, `list` là $O(n)$. Chỉ cần biết có/không → dùng `set`.

**Pandas:**
- Giữ mọi dòng bảng trái khi merge: `how='left'` (thiếu bên phải → `NaN`).
- Đếm tần suất giá trị: `df['status'].value_counts()`.
- Lọc dòng: boolean mask `df[df['age'] >= 18]`.

### B4. Gọi API bằng `requests`

```python
import requests

# GET có tham số + timeout
r = requests.get(url, params={'q': 'ai'}, timeout=5)

# POST gửi JSON
r = requests.post(url, json=payload, timeout=6)

# Bearer token trong header
r = requests.get(url, headers={'Authorization': f'Bearer {token}'}, timeout=5)

r.raise_for_status()   # ném HTTPError nếu 4xx/5xx
data = r.json()        # parse JSON — KHÔNG dùng eval()
```

| Điểm phải nhớ | Nội dung |
|---|---|
| `params=` vs `json=` | `params` → **query string trên URL**; `json` → **body**, tự đặt `Content-Type: application/json` |
| `raise_for_status()` | Cách chuẩn để biến 4xx/5xx thành ngoại lệ |
| `r.json()` | Parse body JSON. **Tuyệt đối không `eval()` dữ liệu từ mạng** |
| Bắt lỗi | `except requests.RequestException` — **lớp cơ sở** của mọi lỗi mạng Requests |
| `timeout=` | Luôn đặt, nếu không request có thể treo vô hạn |

**Mã HTTP:**

| Mã | Ý nghĩa |
|---|---|
| **200** | OK |
| **400** | Bad Request — dữ liệu gửi lên sai |
| **401** | **Chưa xác thực** / thông tin xác thực không hợp lệ |
| **403** | Đã xác thực nhưng **không có quyền** |
| **404** | Không tìm thấy tài nguyên |
| **500** | Lỗi phía server |

> [!warning] 401 vs 403 — hay bị nhầm
> **401 = "anh là ai?"** (chưa đăng nhập / token sai). **403 = "biết anh là ai rồi, nhưng anh không được phép"**.

> [!important] Hai nguyên tắc an toàn luôn được hỏi
> 1. **API key không bao giờ nằm trong source code, trong URL, hoặc trong log.** Dùng biến môi trường / secret manager.
> 2. **Luôn validate dữ liệu API trả về trước khi tính toán** — kiểm tra key tồn tại, đúng kiểu, list không rỗng. Đề dùng đúng ví dụ: API hứa trả `{"values": [1,2,3]}` nhưng code phải phòng trường hợp thiếu field hoặc list rỗng.

---

## 📙 MODULE C — Machine Learning & AI sản phẩm

### C1. Confusion matrix — phần tính toán chắc chắn có

|  | Dự đoán **Dương** | Dự đoán **Âm** |
|---|---|---|
| **Thực tế Dương** | TP | **FN** ← *bỏ sót* |
| **Thực tế Âm** | FP ← *báo động nhầm* | TN |

$$\text{Accuracy}=\frac{TP+TN}{TP+FP+FN+TN}\qquad
\text{Precision}=\frac{TP}{TP+FP}\qquad
\text{Recall}=\frac{TP}{TP+FN}$$

$$F_1=\frac{2\cdot P\cdot R}{P+R}$$

**Bộ số được dùng lại nhiều lần trong đề — nên thuộc:**

| TP | FP | FN | TN | Accuracy | Precision | Recall |
|---|---|---|---|---|---|---|
| 30 | 10 | 5 | 55 | 85% | 75% | 85,7% |
| 24 | 6 | 8 | 42 | 82,5% | 80% | 75% |
| 36 | 4 | 9 | 51 | 87% | 90% | 80% |
| 40 | 10 | 20 | 30 | 70% | 80% | 66,7% |

> [!important] Cách nhớ Precision vs Recall không bao giờ lẫn
> **Mẫu số cho biết tất cả.** Precision chia cho **những gì model NÓI là dương** ($TP+FP$ — cột dự đoán dương). Recall chia cho **những gì THỰC SỰ dương** ($TP+FN$ — hàng thực tế dương).
>
> - **Precision thấp** → báo động nhầm nhiều (FP nhiều).
> - **Recall thấp** → bỏ sót nhiều (FN nhiều).
> - **"Số ca dương tính thật bị bỏ sót" = FN.** Đây là câu hỏi lặp lại nguyên văn nhiều lần.

> [!warning] Chọn metric theo hậu quả, không theo thói quen
> - **Bỏ sót nguy hiểm** (ung thư, gian lận, an toàn) → ưu tiên **Recall**.
> - **Báo nhầm tốn kém/gây phiền** (chặn tài khoản, gửi cảnh báo) → ưu tiên **Precision**.
> - **Dữ liệu mất cân bằng** → **Accuracy vô dụng**. Model đoán toàn "âm" cho bệnh hiếm 1% vẫn đạt 99% accuracy. Dùng Precision/Recall/F1 hoặc PR-AUC.

### C2. Overfitting & train/validation/test

**Dấu hiệu:** train 97% nhưng validation 70% → **khoảng cách lớn = overfitting**. (Đề dùng nhiều cặp số: 97/76, 98/72, 96/74 — cùng một kết luận.)

| Tập | Vai trò |
|---|---|
| **Train** | học tham số |
| **Validation** | chọn hyperparameter, chọn model |
| **Test** | đánh giá cuối, **giữ độc lập, chỉ dùng một lần** |

**Cách chữa overfitting:** thêm dữ liệu · regularization (L1/L2, weight decay) · dropout · early stopping · giảm độ phức tạp model · cross-validation · data augmentation.

> [!note] Liên hệ chéo
> Nội dung này trùng với [[Deep Learning/contents/02 - Linear Regression|Deep Learning ch. 02]] (weight decay, generalization) và [[Deep Learning/contents/03 - Logistic Regression|ch. 03]] (test set reuse). Nếu đã học hai chương đó thì phần này gần như miễn phí.

### C3. SVM

- **Mục tiêu:** tìm siêu phẳng phân tách và **tối đa hóa margin**.
- **Support vectors:** các điểm **nằm gần margin nhất** — chỉ chúng quyết định siêu phẳng; bỏ các điểm khác đi kết quả không đổi.
- Nếu hai siêu phẳng cùng phân loại đúng train → **chọn cái có margin lớn hơn**, vì ổn định hơn với dữ liệu mới.
- **Dự đoán:** với hàm quyết định $f(x)$, lớp $=+1$ nếu $f(x)\ge0$. Ví dụ $f(x)=x_1-x_2+1$, $x=(2,2)$ → $f=2-2+1=1\ge0$ → **lớp $+1$**.

### C4. Neural network & backpropagation

**Backpropagation = dùng quy tắc dây chuyền (chain rule) để truyền gradient từ output ngược về các tham số.** Nó *không* phải thuật toán tối ưu — cập nhật tham số là việc của gradient descent.

**Bài tính gradient một nơ-ron (lặp lại nhiều lần):** với $\hat y=wx$ và $L=\frac12(\hat y-y)^2$:
$$\frac{dL}{dw}=(\hat y - y)\,x$$

| $x$ | $w$ | $y$ | $\hat y = wx$ | $dL/dw=(\hat y-y)x$ |
|---|---|---|---|---|
| 2 | 0,5 | 3 | 1 | $(1-3)\times2=\mathbf{-4}$ |
| 3 | 1 | 2 | 3 | $(3-2)\times3=\mathbf{+3}$ |

**ReLU:** $\text{ReLU}(z)=\max(0,z)$, đạo hàm $=1$ khi $z>0$, $=0$ khi $z<0$ (tại $z=0$ không xác định). Ví dụ tại $z=4$ → đạo hàm $=\mathbf{1}$.

### C5. RAG (Retrieval-Augmented Generation)

**Pipeline:** `Tài liệu → chunk → embedding → vector store` ⟶ `Câu hỏi → embedding → retrieval (top-k) → đưa vào prompt → generation → trả lời kèm citation`

| Bước | Nhiệm vụ |
|---|---|
| **Retrieval** | **Lấy bằng chứng liên quan** — chỉ tìm, không sinh câu trả lời |
| **Embedding** | Biến text thành vector để **tìm kiếm theo ngữ nghĩa** bằng khoảng cách vector |
| **Generation** | Dùng bằng chứng đã lấy để soạn câu trả lời |

> [!important] Ba câu trả lời "đúng" của RAG mà đề hỏi đi hỏi lại
> 1. **Retrieval làm gì?** → *lấy bằng chứng liên quan*, generation mới là bước tạo câu trả lời.
> 2. **Không đủ bằng chứng thì sao?** → **từ chối trả lời hoặc chuyển cho người** (abstention + escalation). **Suy đoán là sai.**
> 3. **Làm sao để người dùng kiểm chứng?** → **citation + số phiên bản tài liệu**, để họ đối chiếu được.

**RAG chữa được gì:** hallucination, kiến thức lỗi thời, thiếu dữ liệu nội bộ. **Không chữa được:** retrieval lấy sai tài liệu, tài liệu gốc đã sai, quyền truy cập không được kiểm soát.

### C6. Khung trả lời câu tự luận "thiết kế tính năng AI"

Đây là **dạng câu 4–8 điểm phổ biến nhất của Module C**. Rubric của bộ đề gần như luôn gồm 5 ý sau — cứ trả lời đủ 5 gạch đầu dòng là gần kín điểm:

> [!tip] Khung 5 ý — học thuộc
> 1. **Output là gì?** — label / score / ranking / đoạn văn. Nói rõ định dạng.
> 2. **Dữ liệu đầu vào** — nêu **ít nhất 2 nguồn** hợp lý.
> 3. **Metric** — phải **gắn với mục tiêu sản phẩm**, không chỉ accuracy.
> 4. **Rủi ro và cách giảm** — bias, privacy, leakage, sai nghiêm trọng; kèm **human review** cho ca quan trọng.
> 5. **Baseline không dùng AI** — thường là rule-based theo keyword/ngưỡng/SLA. **Ý này hay bị bỏ quên nhất mà lại luôn có trong rubric.**

Với câu "chọn model A hay B", rubric yêu cầu: **chất lượng trên task thật · latency/chi phí/tài nguyên · rủi ro & safety · phương án phân tầng hoặc fallback · và KHÔNG kết luận máy móc rằng model lớn hơn luôn tốt hơn.**

---

## 📕 MODULE D — Responsible AI, Privacy & Logic

### D1. Sáu trụ cột — khung xương của mọi câu 6–8 điểm

Câu hỏi dạng *"Công ty muốn dùng AI để... Trả lời theo 6 mục"* xuất hiện nhiều lần (banking, tuyển dụng, y tế, giáo dục, marketplace). **Rubric luôn là đúng 6 ý này** — mỗi ý một điểm:

| # | Trụ cột | Nội dung cần viết |
|---|---|---|
| 1 | **Privacy / Data minimization** | Chỉ thu thập **dữ liệu cần thiết cho mục đích**; phân quyền; mã hoá |
| 2 | **Fairness / Bias** | **Đo** tỷ lệ kết quả theo nhóm; sửa feature/ngưỡng nếu lệch; theo dõi lại |
| 3 | **Transparency** | Báo cho người dùng biết **có AI tham gia**; giải thích lý do ở mức phù hợp |
| 4 | **Security / Audit** | Bảo vệ dữ liệu; **audit log**; kiểm soát truy cập |
| 5 | **Human oversight** | Người duyệt với ca **sát ngưỡng, thiếu dữ liệu, rủi ro cao, có khiếu nại** |
| 6 | **Accountability** | **Một bộ phận cụ thể chịu trách nhiệm**; có quy trình **khiếu nại và sửa sai** |

> [!tip] Mẹo ăn điểm
> Viết đúng **6 tiêu đề** rồi mỗi mục 1–2 câu cụ thể **gắn với tình huống trong đề** (ngân hàng thì nói hồ sơ vay, tuyển dụng thì nói CV...). Rubric chấm theo **sự có mặt của từng ý**, không theo độ dài.

### D2. Định nghĩa phải thuộc chính xác

| Khái niệm | Định nghĩa |
|---|---|
| **Data minimization** | Chỉ thu thập/lưu **dữ liệu thực sự cần** cho mục đích đã nêu — giảm thu thập dư thừa để giảm rủi ro |
| **Purpose limitation** | Dữ liệu thu cho mục đích nào **chỉ được dùng cho mục đích đó** |
| **Transparency** | Người bị ảnh hưởng **hiểu được** có AI tham gia và **kiểm tra được** quyết định |
| **Accountability** | **Có người/bộ phận cụ thể chịu trách nhiệm** — không được đổ lỗi mơ hồ cho "AI" |
| **Least privilege** | Quyền truy cập **giới hạn theo đúng nhiệm vụ** và phạm vi dữ liệu |
| **Human-in-the-loop** | Người xem lại/quyết định ở các ca rủi ro cao |
| **PII** | Thông tin định danh cá nhân — **cần kiểm soát chặt nhất** |

### D3. Các tình huống và câu trả lời chuẩn

| Tình huống trong đề | Đáp án đúng |
|---|---|
| Model **không chắc chắn** ở quyết định ảnh hưởng quyền lợi | **Abstain + escalate** cho người, có fallback |
| Phát hiện model **thiên lệch** với một nhóm | **Đo → xử lý → theo dõi lại** một cách có hệ thống (không phải bỏ qua, không phải xoá model) |
| Quyết định **tự động** ảnh hưởng lớn (duyệt vay) | Cần **oversight + quyền khiếu nại (appeal) + accountability** |
| Trợ lý chỉ cần **xem trạng thái hồ sơ** nhưng được cấp quyền đọc **toàn bộ hệ thống** | Vi phạm **least privilege** |
| Nhóm A không được xem dữ liệu nhóm B | **Authorization phải thực thi TRƯỚC khi dữ liệu rời lớp tin cậy** — không lọc ở tầng hiển thị |
| Demo chatbot FAQ định dùng **bản sao dữ liệu thật** có tên + số tài khoản | Vi phạm data minimization → dùng **dữ liệu giả/ẩn danh**; FAQ không cần dữ liệu giao dịch thật |
| Câu hỏi có thể ảnh hưởng **pháp lý/tài chính** mà thiếu bằng chứng | **Abstention + escalation** |

### D4. Logic & nguỵ biện

| Dạng | Quy tắc | Ví dụ trong đề |
|---|---|---|
| **Phủ định hệ quả** (modus tollens) — **đúng** | "Nếu $A$ thì $B$"; biết **không $B$** ⇒ **không $A$** | "Nếu bị tấn công thì log bất thường". Log **không** bất thường ⇒ **không bị tấn công** |
| **Phủ định lượng từ** | Phủ định của "**tất cả** đều X" là "**tồn tại ít nhất một** không X" | Phủ định "tất cả đơn hàng đều được kiểm tra" = "có ít nhất một đơn hàng **không** được kiểm tra" |
| **Nhầm tương quan với nhân quả** | Xảy ra **sau** không có nghĩa là **do** | "Triển khai AI xong doanh thu tăng, vậy AI là nguyên nhân" — **sai** |
| **Nguỵ biện người rơm** (straw man) | Bóp méo quan điểm đối phương thành phiên bản cực đoan rồi bác bỏ | "Bạn muốn kiểm soát nội dung độc hại, vậy là muốn cấm toàn bộ tự do ngôn luận" |

> [!warning] Hai lỗi suy luận KHÔNG hợp lệ — đừng chọn
> - **Khẳng định hệ quả:** "Nếu $A$ thì $B$"; biết $B$ ⇒ kết luận $A$. **SAI.**
> - **Phủ định tiền đề:** "Nếu $A$ thì $B$"; biết không $A$ ⇒ kết luận không $B$. **SAI.**
>
> Chỉ có **modus ponens** ($A$ ⇒ $B$) và **modus tollens** (không $B$ ⇒ không $A$) là hợp lệ.

---

## ✅ Checklist 10 phút trước giờ thi

1. $P(A\mid B)=P(A\cap B)/P(B)$ — dạng hỏi nhiều nhất Module A.
2. $P(\text{ít nhất một})=1-P(\text{không cái nào})$.
3. Rút không hoàn lại → mẫu số giảm; hỏi "khác màu" → **nhân 2**.
4. $\det=ad-bc$; $\det=0$ ⇒ suy biến ⇒ không nghịch đảo ⇒ rank giảm. **Một phép tính trả lời ba câu hỏi.**
5. $A^{-1}=\frac{1}{ad-bc}[[d,-b],[-c,a]]$ — đổi chỗ $a,d$; đổi dấu $b,c$.
6. $AB\ne BA$.
7. Euclid: `while b != 0: a, b = b, a % b; return a`. GCD(252,105)=21; GCD(84,30)=6; GCD(48,18)=6. Độ phức tạp $O(\log n)$.
8. `axis=k` làm **mất** chiều thứ $k$. `x[:,1]` mất chiều, `x[:,1:2]` giữ chiều.
9. `params=` → URL; `json=` → body. `raise_for_status()`. `except RequestException`. **401 = chưa xác thực, 403 = không có quyền.**
10. Precision chia $TP+FP$; Recall chia $TP+FN$; **FN = bỏ sót**. Mất cân bằng → **đừng dùng accuracy**.
11. $dL/dw=(\hat y-y)x$. Backprop = **chain rule**, không phải thuật toán tối ưu.
12. RAG thiếu bằng chứng → **từ chối / chuyển người**, kèm **citation + version**.
13. Câu thiết kế AI → khung **5 ý** (output, dữ liệu, metric, rủi ro, **baseline không-AI**).
14. Câu Responsible AI → khung **6 trụ cột** (privacy, fairness, transparency, security, oversight, accountability).
15. Logic: chỉ **modus ponens** và **modus tollens** là hợp lệ.

**Xem thêm:** [[AI Test - Ngan hang cau tu luan]]
