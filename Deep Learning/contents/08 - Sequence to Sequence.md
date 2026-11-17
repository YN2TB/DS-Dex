---
subject: Deep Learning
chapter: 8
tags: [ds, deep-learning, seq2seq, encoder-decoder, bleu, beam-search, attention, transformer, self-attention, positional-encoding]
source: "Zhang, Lipton, Li & Smola, *Dive into Deep Learning*, §10.5–10.8 (Machine Translation, Encoder–Decoder, Seq2seq, Beam Search) and §11.1–11.7 (Attention, Multi-Head, Self-Attention, the Transformer)"
---

# Sequence to Sequence

D2L §10.5–10.8 covers the translation data, the encoder–decoder, BLEU and beam search, each with code. §11.1–11.7 (attention and the Transformer) is added to this topic as a scope extension recorded in [[00-Index]], since seq2seq without attention stops just before the modern approach. The lectures (8 Encoder–Decoder, 9 Attention) also add Luong attention and BERT/GPT: §11–13.

## 📘 Main Knowledge

### 1. Machine translation data (§10.5)

Unlike language modelling ([[07 - Recurrent Neural Network|ch. 07]]), input and output are different sequences, in different languages, of different lengths. This requires:
- two vocabularies (source and target);
- padding to a fixed length with `<pad>` plus a recorded valid length, hence masking throughout;
- special tokens: `<bos>` starts decoding, `<eos>` ends it, `<unk>` replaces unknown words.

**The dataset (§10.5).** English–French sentence pairs from the Tatoeba Project, one tab-separated pair per line (`Go.\tVa !`, `Hi.\tSalut !`, `Run!\tCours !`, …). The file is ordered roughly from the shortest sentences up.

```python
def _preprocess(self, text):
    text = text.replace(' ', ' ').replace('\xa0', ' ')   # non-breaking spaces
    no_space = lambda char, prev_char: char in ',.!?' and prev_char != ' '
    out = [' ' + char if i > 0 and no_space(char, text[i - 1]) else char
           for i, char in enumerate(text.lower())]
    return ''.join(out)                       # 'go . va !'

def _tokenize(self, text, max_examples=None):
    src, tgt = [], []
    for i, line in enumerate(text.split('\n')):
        if max_examples and i > max_examples: break
        parts = line.split('\t')
        if len(parts) == 2:
            src.append([t for t in f'{parts[0]} <eos>'.split(' ') if t])
            tgt.append([t for t in f'{parts[1]} <eos>'.split(' ') if t])
    return src, tgt                           # [['go', '.', '<eos>'], ...]
```

Word-level tokens (each word or punctuation mark), `<eos>` appended to every sequence. Most sequences have under 20 tokens.

**Fixed length.** Each sequence is truncated or padded with `<pad>` to `num_steps=9`; targets get `<bos>` in front; tokens seen fewer than twice become `<unk>` (`min_freq=2`); the source's **valid length** (non-pad tokens) is recorded. The arrays are `(src, tgt[:, :-1], src_valid_len, tgt[:, 1:])`: decoder input and label are the same target shifted by one.

```python
def __init__(self, batch_size, num_steps=9, num_train=512, num_val=128): ...

def _build_array(sentences, vocab, is_tgt=False):
    pad_or_trim = lambda seq, t: (
        seq[:t] if len(seq) > t else seq + ['<pad>'] * (t - len(seq)))
    sentences = [pad_or_trim(s, self.num_steps) for s in sentences]
    if is_tgt:
        sentences = [['<bos>'] + s for s in sentences]
    if vocab is None:
        vocab = d2l.Vocab(sentences, min_freq=2)
    array = torch.tensor([vocab[s] for s in sentences])
    valid_len = (array != vocab['<pad>']).type(torch.int32).sum(1)
    return array, vocab, valid_len
```

`data.build(['hi .'], ['salut .'])` gives source `['hi', '.', '<eos>', '<pad>', …]` and target `['<bos>', 'salut', '.', '<eos>', '<pad>', …]`. In a printed batch the decoder input starts with index 3 (`<bos>`) and the label is the same row shifted left. Modern implementations bucket sequences of similar length to waste less compute on padding.

(Mine, from the downloaded file with D2L's SHA-1: the loader keeps lines 0–640, i.e. 641 pairs, 512 for training and 129 for validation. Source vocabulary 194 tokens, target 214; 3.3% of source tokens become `<unk>`; no sentence needs truncation at 9 tokens. The 512 training pairs contain only 2,136 target tokens.)

### 2. Encoder–decoder, seq2seq and BLEU (§10.6–10.7)

The **encoder** turns a variable-length input into a fixed-shape state; the **decoder** uses that state and the tokens generated so far to produce the next token. Any encoder can be paired with any decoder through this interface.

**Teacher forcing**: during training the decoder receives the true previous token, not its own prediction. Training is faster and more stable, but at test time the model sees its own outputs, a mismatch called **exposure bias** (D2L ex. 10.7.4).

**Masked loss**: padded positions are multiplied by zero, as with `bbox_masks` in [[06 - Object Detection|ch. 06]].

**BLEU** (Papineni et al. 2002) measures n-gram overlap with a reference:
$$\mathrm{BLEU}=\exp\left(\min\left(0,\ 1-\frac{\mathrm{len}_{\text{label}}}{\mathrm{len}_{\text{pred}}}\right)\right)\prod_{n=1}^{k}p_n^{1/2^n}$$
where $p_n$ is the clipped n-gram precision (each reference n-gram can be matched only once). The first factor is the brevity penalty. The exponent $1/2^n$ halves with each $n$, so precision on longer n-grams affects the score less (see D13 below).

Target `A B C D E F`, prediction `A B B C D`: $p_1=4/5$, $p_2=3/4$, $p_3=1/3$, $p_4=0$, as in D2L. Prediction `A B` has perfect precision but brevity penalty $e^{1-3}=0.1353$.

D2L's printed translations:

| English | predicted | target | BLEU |
|---|---|---|---|
| go . | va ! | va ! | 1.000 |
| i lost . | j'ai perdu . | j'ai perdu . | 1.000 |
| he's calm . | soyez calmes . | il est calme . | 0.000 |
| i'm home . | je suis chez moi . | je suis chez moi . | 1.000 |

In the third row $p_2=0$, so the product is 0 even though one token matches and "soyez calmes" is a reasonable imperative translation. Sentence-level BLEU against one reference measures n-gram overlap, not translation quality. The original metric uses multiple references and corpus-level counts to reduce these problems. The other three rows are training sentences (see below).

**The interface (§10.6).** "They are watching ." → encoder → state → decoder → "Ils regardent .".

```python
class Encoder(nn.Module):
    def forward(self, X, *args):
        raise NotImplementedError

class Decoder(nn.Module):
    def init_state(self, enc_all_outputs, *args):   # encoder output -> decoder state
        raise NotImplementedError
    def forward(self, X, state):
        raise NotImplementedError

class EncoderDecoder(d2l.Classifier):
    def __init__(self, encoder, decoder):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
    def forward(self, enc_X, dec_X, *args):
        enc_all_outputs = self.encoder(enc_X, *args)
        dec_state = self.decoder.init_state(enc_all_outputs, *args)
        return self.decoder(dec_X, dec_state)[0]       # decoder output only
```

**RNN seq2seq (§10.7).** The encoder maps $\mathbf h_t=f(\mathbf x_t,\mathbf h_{t-1})$ and summarizes with $\mathbf c=q(\mathbf h_1,\dots,\mathbf h_T)$, here simply $\mathbf c=\mathbf h_T$. The decoder updates $\mathbf s_{t'}=g(y_{t'-1},\mathbf c,\mathbf s_{t'-1})$ and outputs $P(y_{t'+1}\mid y_1,\dots,y_{t'},\mathbf c)$. An **embedding layer** (`nn.Embedding(vocab_size, embed_size)`) maps token $i$ to row $i$ of a learned matrix: the learned version of one-hot × matrix.

```python
def init_seq2seq(module):                        # Xavier for Linear and GRU weights
    if type(module) == nn.Linear:
        nn.init.xavier_uniform_(module.weight)
    if type(module) == nn.GRU:
        for param in module._flat_weights_names:
            if "weight" in param:
                nn.init.xavier_uniform_(module._parameters[param])

class Seq2SeqEncoder(d2l.Encoder):
    def __init__(self, vocab_size, embed_size, num_hiddens, num_layers, dropout=0):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.rnn = d2l.GRU(embed_size, num_hiddens, num_layers, dropout)
        self.apply(init_seq2seq)
    def forward(self, X, *args):
        embs = self.embedding(X.t().type(torch.int64))  # (num_steps, batch, embed)
        outputs, state = self.rnn(embs)
        return outputs, state     # (num_steps, batch, hiddens), (layers, batch, hiddens)

class Seq2SeqDecoder(d2l.Decoder):
    def __init__(self, vocab_size, embed_size, num_hiddens, num_layers, dropout=0):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.rnn = d2l.GRU(embed_size+num_hiddens, num_hiddens, num_layers, dropout)
        self.dense = nn.LazyLinear(vocab_size)
        self.apply(init_seq2seq)
    def init_state(self, enc_all_outputs, *args):
        return enc_all_outputs
    def forward(self, X, state):
        embs = self.embedding(X.t().type(torch.int32))
        enc_output, hidden_state = state
        context = enc_output[-1]                          # c = last encoder output
        context = context.repeat(embs.shape[0], 1, 1)     # same c at every step
        embs_and_context = torch.cat((embs, context), -1)
        outputs, hidden_state = self.rnn(embs_and_context, hidden_state)
        outputs = self.dense(outputs).swapaxes(0, 1)      # (batch, steps, vocab)
        return outputs, [enc_output, hidden_state]
```

The decoder's initial hidden state is the encoder's final state (so both need the same number of layers and hidden units), and $\mathbf c$ is concatenated to the decoder input at every step. Shapes on a toy batch (vocab 10, embed 8, hidden 16, 2 layers, batch 4, 9 steps): encoder outputs (9, 4, 16), state (2, 4, 16); decoder output (4, 9, 10).

**Teacher forcing** feeds `<bos>` + target (minus the last token) and predicts the target shifted by one: `<bos> Ils regardent .` → `Ils regardent . <eos>`.

**Masked loss:**

```python
class Seq2Seq(d2l.EncoderDecoder):
    def __init__(self, encoder, decoder, tgt_pad, lr):
        super().__init__(encoder, decoder)
        self.save_hyperparameters()
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr)

def loss(self, Y_hat, Y):
    l = super(Seq2Seq, self).loss(Y_hat, Y, averaged=False)
    mask = (Y.reshape(-1) != self.tgt_pad).type(torch.float32)
    return (l * mask).sum() / mask.sum()       # mean over real tokens only
```

**Training:** batch 128, embedding and hidden size 256, 2 GRU layers, dropout 0.2, Adam `lr=0.005`, 30 epochs, clipping 1. (Mine: 1,935,062 parameters.)

**Prediction** is greedy: feed `<bos>`, take the argmax token, feed it back, stop at `<eos>`:

```python
def predict_step(self, batch, device, num_steps, save_attention_weights=False):
    batch = [a.to(device) for a in batch]
    src, tgt, src_valid_len, _ = batch
    enc_all_outputs = self.encoder(src, src_valid_len)
    dec_state = self.decoder.init_state(enc_all_outputs, src_valid_len)
    outputs, attention_weights = [tgt[:, 0].unsqueeze(1), ], []
    for _ in range(num_steps):
        Y, dec_state = self.decoder(outputs[-1], dec_state)
        outputs.append(Y.argmax(2))
        if save_attention_weights:
            attention_weights.append(self.decoder.attention_weights)
    return torch.cat(outputs[1:], 1), attention_weights
```

**BLEU code** (clipped counts via a dictionary of remaining reference n-grams):

```python
def bleu(pred_seq, label_seq, k):
    pred_tokens, label_tokens = pred_seq.split(' '), label_seq.split(' ')
    len_pred, len_label = len(pred_tokens), len(label_tokens)
    score = math.exp(min(0, 1 - len_label / len_pred))
    for n in range(1, min(k, len_pred) + 1):
        num_matches, label_subs = 0, collections.defaultdict(int)
        for i in range(len_label - n + 1):
            label_subs[' '.join(label_tokens[i: i + n])] += 1
        for i in range(len_pred - n + 1):
            if label_subs[' '.join(pred_tokens[i: i + n])] > 0:
                num_matches += 1
                label_subs[' '.join(pred_tokens[i: i + n])] -= 1
        score *= math.pow(num_matches / (len_pred - n + 1), math.pow(0.5, n))
    return score
```

> [!note] How much weight long n-grams get (discrepancy D13)
> D2L says that because $p_n^{1/2^n}$ increases with $n$ for fixed $p_n$, BLEU "assigns a greater weight when a longer n-gram has high precision". The factor does increase, but that means a poor long-n-gram precision costs **less**: the exponent of $\log p_n$ is $1/2^n$, which halves with every $n$. At $p_n=0.5$ the factors are 0.707, 0.841, 0.917, 0.958 for $n=1..4$. The original BLEU (Papineni et al. 2002) uses equal weights, $p_n^{1/N}$ with $N=4$; D2L's parenthesis says $p_n^{1/n}$. The maths of D2L's own formula is right; "greater weight" describes it backwards.

**What D2L's four test translations show** (mine, checked against the downloaded dataset). D2L translates four hand-picked sentences rather than its validation split. In the 641-pair file, "go ." is pair 0, "i lost ." pair 49 and "i'm home ." pair 349: all three are among the 512 **training** pairs, so their BLEU of 1.000 is recall of memorized pairs. "he's calm ." does not occur in the data at all. Its predicted "soyez calmes ." is the exact training target of "be calm ." (pair 77). With about 1.9 million parameters fitted to 2,136 target tokens, memorization is expected. The one unseen sentence scores 0.

### 3. Decoding: greedy, exhaustive, beam (§10.8)

**Greedy search** picks the most likely token at each step, which does not give the most likely sequence. D2L's example:

| sequence | probability |
|---|---|
| greedy `A B C <eos>` | $0.5\times0.4\times0.4\times0.6=0.048$ |
| alternative `A C B <eos>` | $0.5\times0.3\times0.6\times0.6=0.054$ |

The better sequence picks the second-best token at step 2; after that the conditional probabilities differ.

| strategy                                     | sequences scored ($\vert \mathcal Y\vert =10^4$, $T'=10$) |
| -------------------------------------------- | --------------------------------------------------------- |
| greedy, $O(\vert \mathcal Y\vert T')$        | $10^5$                                                    |
| beam, $k=10$, $O(k\vert \mathcal Y\vert T')$ | $10^6$                                                    |
| exhaustive, $O(\vert \mathcal Y\vert ^{T'})$ | $10^{40}$                                                 |

**Beam search** keeps the $k$ best partial sequences. Final candidates are compared with a length-normalized score $\frac{1}{L^\alpha}\log P$: since $\log P$ is a sum of negative terms, unnormalized scores always favour short outputs.

**Beam search in detail (§10.8.3).** Vocabulary $\{A,B,C,D,E\}$ (one of them `<eos>`), beam size 2, maximum length 3. Step 1 keeps the two best first tokens, say $A$ and $C$. Step 2 scores all $2\times5=10$ extensions $P(A,y_2\mid\mathbf c)=P(A\mid\mathbf c)P(y_2\mid A,\mathbf c)$ and $P(C,y_2\mid\mathbf c)$ and keeps the best two, say $AB$ and $CE$; step 3 likewise gives $ABD$ and $CED$. The final candidates are all six prefixes $A, C, AB, CE, ABD, CED$ (cut after `<eos>`), and the winner maximizes
$$\frac1{L^\alpha}\log P(y_1,\dots,y_L\mid\mathbf c)=\frac1{L^\alpha}\sum_{t'=1}^L\log P(y_{t'}\mid y_1,\dots,y_{t'-1},\mathbf c),$$
with $\alpha$ usually 0.75. Greedy search is beam search with $k=1$. Exhaustive search is the limit where the beam keeps every candidate, $k=|\mathcal Y|^{t'}$ (D2L ex. 10.8.1).

> [!note] Which way the length term pushes (discrepancy D14)
> D2L writes that the $L^\alpha$ in the denominator "penalizes long sequences". It does the opposite: the sum of log-probabilities is negative and grows more negative with every token, which is what penalizes long sequences; dividing by $L^\alpha$ shrinks that sum and so *favours* longer candidates relative to the raw score. Example: two tokens at probability 0.5 each score $\log0.25=-1.386$ raw and $-1.386/2^{0.75}=-0.824$ normalized; four tokens at 0.5 score $-2.773$ raw but $-2.773/4^{0.75}=-0.980$ normalized. The formula is right; the sentence is reversed.

### 4. Attention as a soft lookup (§11.1–11.3)

Given a query $\mathbf q$ and key–value pairs $(\mathbf k_i,\mathbf v_i)$:
$$\mathrm{Attention}(\mathbf q,\mathcal D)=\sum_i\alpha(\mathbf q,\mathbf k_i)\,\mathbf v_i,\qquad \alpha=\mathrm{softmax}\big(a(\mathbf q,\mathbf k_i)\big)$$
A database lookup is the case where $\alpha$ is 1 on one key and 0 elsewhere. Attention is a differentiable version.

D2L derives the dot product from a Gaussian kernel: $-\tfrac12\|\mathbf q-\mathbf k_i\|^2=\mathbf q^\top\mathbf k_i-\tfrac12\|\mathbf k_i\|^2-\tfrac12\|\mathbf q\|^2$. The $\|\mathbf q\|^2$ term is the same for every key and cancels in the softmax, and $\|\mathbf k_i\|^2$ is roughly constant after layer normalization, leaving $\mathbf q^\top\mathbf k_i$.

**Additive attention** $a=\mathbf w_v^\top\tanh(\mathbf W_q\mathbf q+\mathbf W_k\mathbf k)$ handles queries and keys of different sizes; otherwise the parameter-free dot product is preferred.

**Masked softmax** sets padded logits to a large negative number ($-10^6$) instead of branching, which is faster on GPUs.

**Databases (§11.1).** A database of (key, value) pairs, e.g. (last name, first name) of the authors: the exact query "Li" returns "Mu"; an approximate query could return "Lipton" → "Zachary". Lessons: a query can work regardless of database size, the same query gives different answers on different contents, the lookup "code" is simple, and the database need not be compressed. Special cases of $\sum_i\alpha(\mathbf q,\mathbf k_i)\mathbf v_i$: nonnegative weights (output in the convex cone of the values), a convex combination (the usual case), exactly one weight 1 (a database query), all weights $1/m$ (average pooling). Any score $a(\mathbf q,\mathbf k)$ can be turned into weights with a softmax, which is differentiable and whose gradient never vanishes. (Non-differentiable "hard" attention trained by RL exists but is harder.)

**Nadaraya–Watson regression (§11.2)**, attention before deep learning: with a kernel $\alpha(\mathbf q,\mathbf k)$,
$$f(\mathbf q)=\sum_i\mathbf v_i\frac{\alpha(\mathbf q,\mathbf k_i)}{\sum_j\alpha(\mathbf q,\mathbf k_j)}.$$

| kernel | $\alpha(q,k)$ |
|---|---|
| Gaussian | $\exp(-\tfrac12\Vert q-k\Vert ^2)$ |
| Boxcar | $1$ if $\Vert q-k\Vert \le1$ |
| Epanechikov | $\max(0,1-\Vert q-k\Vert )$ |
| constant | 1 (gives the plain mean $\frac1n\sum_iy_i$) |

D2L's data: 40 training points $y_i=2\sin x_i+x_i+\epsilon$, $x_i\sim U(0,5)$ sorted, $\epsilon\sim\mathcal N(0,1)$; validation queries $0,0.1,\dots,4.9$.

```python
def nadaraya_watson(x_train, y_train, x_val, kernel):
    dists = x_train.reshape((-1, 1)) - x_val.reshape((1, -1))
    k = kernel(dists).type(torch.float32)      # rows: keys, columns: queries
    attention_w = k / k.sum(0)                 # normalize over keys per query
    y_hat = y_train@attention_w
    return y_hat, attention_w
```

No training is needed, and with kernels narrowed as data grows the estimator is consistent. Gaussian, boxcar and Epanechikov give similar fits because their attention weights are similar; the constant kernel is useless. A Gaussian of width $\sigma$, $\exp(-\|q-k\|^2/2\sigma^2)$, trades smoothness ($\sigma=1$) for local detail ($\sigma=0.1$). Hand-tuned kernels are limited; the better strategy is to **learn** query and key representations, which is what the following sections do.

**Masked softmax (§11.3.2).**

```python
def masked_softmax(X, valid_lens):           # X: 3-D, valid_lens: 1-D or 2-D
    def _sequence_mask(X, valid_len, value=0):
        maxlen = X.size(1)
        mask = torch.arange((maxlen), dtype=torch.float32,
                            device=X.device)[None, :] < valid_len[:, None]
        X[~mask] = value
        return X
    if valid_lens is None:
        return nn.functional.softmax(X, dim=-1)
    shape = X.shape
    if valid_lens.dim() == 1:
        valid_lens = torch.repeat_interleave(valid_lens, shape[1])
    else:
        valid_lens = valid_lens.reshape(-1)
    X = _sequence_mask(X.reshape(-1, shape[-1]), valid_lens, value=-1e6)
    return nn.functional.softmax(X.reshape(shape), dim=-1)
```

With valid lengths `[2, 3]` on a (2, 2, 4) input, rows of the first example have zeros after position 2 and rows of the second after position 3; a 2-D `[[1, 3], [2, 4]]` sets the length per row (a length of 1 gives weight 1.0000 on the first key).

**Batch matrix multiplication**: `torch.bmm` multiplies $\mathbf Q_i\mathbf K_i$ for each item of a batch, $(n,a,b)\times(n,b,c)\to(n,a,c)$, e.g. `(2, 3, 4) × (2, 4, 6) → (2, 3, 6)`.

**Additive attention code:**

```python
class AdditiveAttention(nn.Module):
    def __init__(self, num_hiddens, dropout, **kwargs):
        super(AdditiveAttention, self).__init__(**kwargs)
        self.W_k = nn.LazyLinear(num_hiddens, bias=False)
        self.W_q = nn.LazyLinear(num_hiddens, bias=False)
        self.w_v = nn.LazyLinear(1, bias=False)
        self.dropout = nn.Dropout(dropout)
    def forward(self, queries, keys, values, valid_lens):
        queries, keys = self.W_q(queries), self.W_k(keys)
        # (batch, queries, 1, h) + (batch, 1, kv pairs, h): all pairs by broadcasting
        features = torch.tanh(queries.unsqueeze(2) + keys.unsqueeze(1))
        scores = self.w_v(features).squeeze(-1)     # (batch, queries, kv pairs)
        self.attention_weights = masked_softmax(scores, valid_lens)
        return torch.bmm(self.dropout(self.attention_weights), values)
```

Equivalently, query and key are concatenated and fed to a one-hidden-layer MLP with tanh. D2L's toy: queries (2, 1, 20), keys (2, 10, 2), values (2, 10, 4), valid lengths (2, 6) → output (2, 1, 4), weights zero beyond positions 2 and 6.

### 5. Bahdanau attention (§11.4)

The basic encoder–decoder squeezes the whole source sentence into one fixed vector. Bahdanau et al. (2014) use the decoder's previous hidden state as the query and the encoder's states at all source positions as keys and values, recomputing the context at every output step.

This also shortens gradient paths. Without attention, information from source token 1 must pass through the whole encoder and then the decoder ($O(n+t)$ steps; [[07 - Recurrent Neural Network|ch. 07]] §7 shows how hard 1,000 steps are). With attention, every output position reads every source position directly.

**Model (§11.4).** The context is recomputed at every decoding step:
$$\mathbf c_{t'}=\sum_{t=1}^T\alpha(\mathbf s_{t'-1},\mathbf h_t)\,\mathbf h_t,$$
with the decoder's previous state as query, encoder states as keys and values, and additive attention as score. $\mathbf c_{t'}$ then produces $\mathbf s_{t'}$ and the next token. (Later versions also attend over the tokens already generated.)

```python
class AttentionDecoder(d2l.Decoder):
    @property
    def attention_weights(self):
        raise NotImplementedError

class Seq2SeqAttentionDecoder(AttentionDecoder):
    def __init__(self, vocab_size, embed_size, num_hiddens, num_layers, dropout=0):
        super().__init__()
        self.attention = d2l.AdditiveAttention(num_hiddens, dropout)
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.rnn = nn.GRU(embed_size + num_hiddens, num_hiddens, num_layers,
                          dropout=dropout)
        self.dense = nn.LazyLinear(vocab_size)
        self.apply(d2l.init_seq2seq)
    def init_state(self, enc_outputs, enc_valid_lens):
        outputs, hidden_state = enc_outputs
        return (outputs.permute(1, 0, 2), hidden_state, enc_valid_lens)
    def forward(self, X, state):
        enc_outputs, hidden_state, enc_valid_lens = state
        X = self.embedding(X).permute(1, 0, 2)
        outputs, self._attention_weights = [], []
        for x in X:
            query = torch.unsqueeze(hidden_state[-1], dim=1)   # (batch, 1, h)
            context = self.attention(query, enc_outputs, enc_outputs, enc_valid_lens)
            x = torch.cat((context, torch.unsqueeze(x, dim=1)), dim=-1)
            out, hidden_state = self.rnn(x.permute(1, 0, 2), hidden_state)
            outputs.append(out)
            self._attention_weights.append(self.attention.attention_weights)
        outputs = self.dense(torch.cat(outputs, dim=0))
        return outputs.permute(1, 0, 2), [enc_outputs, hidden_state, enc_valid_lens]
    @property
    def attention_weights(self):
        return self._attention_weights
```

The decoder state holds (i) the last encoder layer's outputs at all steps (keys and values), (ii) the encoder's final state at all layers (initial decoder state), (iii) the source valid lengths (so padding gets no attention). The query is the top decoder layer's previous state; context and embedding are concatenated as the GRU input. Same training settings as §2 (mine: 2,066,390 parameters, +131,328 for attention).

Printed translations: "go ." → "va !" (1.000), "i lost ." → "j'ai perdu ." (1.000), "he's calm ." → "je suis mouillé ." (0.000), "i'm home ." → "je suis chez moi ." (1.000). "je suis mouillé ." is the training target of "i'm wet ." (pair 173): again a memorized output for the unseen sentence. The attention heatmap for "i'm home ." shows each query spreading non-uniform weights over the source positions.

### 6. Scaled dot-product attention (§11.3.3)

If $\mathbf q,\mathbf k\in\mathbb R^d$ have independent zero-mean, unit-variance entries, $\mathbf q^\top\mathbf k$ has variance $d$. So
$$a(\mathbf q,\mathbf k_i)=\frac{\mathbf q^\top\mathbf k_i}{\sqrt d}$$

Simulated variance: 3.9959 ($d=4$), 63.9494 ($d=64$), 510.4430 ($d=512$); about 1 after scaling.

Why it matters (beyond D2L's variance argument):

| | sd of logits | max weight | entropy (nats) |
|---|---|---|---|
| unscaled, $d=512$, 10 keys | 22.63 | 0.9523 | 0.1170 |
| unscaled, $d=64$, 10 keys | 8.00 | 0.8646 | 0.3489 |
| scaled, 10 keys | 1.00 | 0.3205 | 1.9228 (max 2.3026) |

Unscaled, the softmax is nearly one-hot, and its Jacobian $p_i(\delta_{ij}-p_j)$ is then almost zero, so queries and keys stop learning. The scaling keeps attention trainable.

**Code (§11.3.3).** For $n$ queries $\mathbf Q\in\mathbb R^{n\times d}$, $m$ keys $\mathbf K\in\mathbb R^{m\times d}$ and values $\mathbf V\in\mathbb R^{m\times v}$:
$$\mathrm{softmax}\!\left(\frac{\mathbf Q\mathbf K^\top}{\sqrt d}\right)\mathbf V\in\mathbb R^{n\times v}.$$

```python
class DotProductAttention(nn.Module):
    def __init__(self, dropout):
        super().__init__()
        self.dropout = nn.Dropout(dropout)
    def forward(self, queries, keys, values, valid_lens=None):
        d = queries.shape[-1]
        scores = torch.bmm(queries, keys.transpose(1, 2)) / math.sqrt(d)
        self.attention_weights = masked_softmax(scores, valid_lens)
        return torch.bmm(self.dropout(self.attention_weights), values)
```

Queries and keys must have the same length $d$ (otherwise use $\mathbf q^\top\mathbf M\mathbf k$ or additive attention). Dropout on the attention weights regularizes.

### 7. Multi-head attention (§11.5)

Project queries, keys and values into $h$ subspaces, attend in each, concatenate, and project with $\mathbf W_o$. With D2L's choice $p_q=p_k=p_v=p_o/h$:

| heads $h$ | per-head size | Q, K, V parameters | $\mathbf W_o$ |
|---|---|---|---|
| 1 | 512 | 786,432 | 262,144 |
| 8 | 64 | 786,432 | 262,144 |
| 16 | 32 | 786,432 | 262,144 |

The total is $4p_o^2$ for any $h$: the heads split one budget. Several heads cost the same as one and can attend to different things. As with grouped convolutions ([[05 - Convolutional Neural Network|ch. 05]] §15), heads do not exchange information until $\mathbf W_o$ mixes them.

**Model and code (§11.5).** Head $i$ is $\mathbf h_i=f(\mathbf W_i^{(q)}\mathbf q,\mathbf W_i^{(k)}\mathbf k,\mathbf W_i^{(v)}\mathbf v)\in\mathbb R^{p_v}$, and the output is $\mathbf W_o[\mathbf h_1;\dots;\mathbf h_h]\in\mathbb R^{p_o}$. With $p_qh=p_kh=p_vh=p_o$ all heads come out of one projection and run in parallel by folding heads into the batch axis:

```python
class MultiHeadAttention(d2l.Module):
    def __init__(self, num_hiddens, num_heads, dropout, bias=False, **kwargs):
        super().__init__()
        self.num_heads = num_heads
        self.attention = d2l.DotProductAttention(dropout)
        self.W_q = nn.LazyLinear(num_hiddens, bias=bias)
        self.W_k = nn.LazyLinear(num_hiddens, bias=bias)
        self.W_v = nn.LazyLinear(num_hiddens, bias=bias)
        self.W_o = nn.LazyLinear(num_hiddens, bias=bias)
    def forward(self, queries, keys, values, valid_lens):
        queries = self.transpose_qkv(self.W_q(queries))
        keys = self.transpose_qkv(self.W_k(keys))
        values = self.transpose_qkv(self.W_v(values))
        if valid_lens is not None:
            valid_lens = torch.repeat_interleave(valid_lens, repeats=self.num_heads, dim=0)
        output = self.attention(queries, keys, values, valid_lens)
        output_concat = self.transpose_output(output)
        return self.W_o(output_concat)

def transpose_qkv(self, X):        # (batch, n, h*p) -> (batch*h, n, p)
    X = X.reshape(X.shape[0], X.shape[1], self.num_heads, -1)
    X = X.permute(0, 2, 1, 3)
    return X.reshape(-1, X.shape[2], X.shape[3])

def transpose_output(self, X):     # inverse of transpose_qkv
    X = X.reshape(-1, self.num_heads, X.shape[1], X.shape[2])
    X = X.permute(0, 2, 1, 3)
    return X.reshape(X.shape[0], X.shape[1], -1)
```

Toy check: 100 hidden units, 5 heads, queries (2, 4, 100), keys = values (2, 6, 100), valid lengths (3, 2) → output (2, 4, 100). To prune heads, measure how much the loss rises when one head's output is zeroed (D2L ex. 11.5.2).

### 8. Self-attention vs CNNs and RNNs (§11.6.1–11.6.2)

Self-attention uses the sequence as queries, keys and values.

| | complexity | sequential ops | max path length |
|---|---|---|---|
| CNN (kernel $k$) | $O(knd^2)$ | $O(1)$ | $O(n/k)$ |
| RNN | $O(nd^2)$ | $O(n)$ | $O(n)$ |
| self-attention | $O(n^2d)$ | $O(1)$ | $O(1)$ |

Self-attention is cheaper than an RNN when $n\lt d$. At $d=512$ that covers sequences under 512 tokens; beyond that the $n^2$ term dominates, which is why long-context attention is its own research area.

The main gain is path length. From [[07 - Recurrent Neural Network|ch. 07]] §7, keeping $\gamma^T$ within $[10^{-3},10^3]$ requires $\gamma$ within ±0.693% of 1 at $T=1000$, but allows $[0.001, 1000]$ at $T=1$. With path length 1 there is no long product of Jacobians to control. Combined with $O(1)$ sequential steps (full parallelism on GPUs), this is why attention replaced recurrence despite worse asymptotic cost.

This links the subject's architectures (my synthesis, not in D2L): sigmoid MLPs fail at ~11 layers because each factor is ≤ 0.25 ([[04 - Neural Network|ch. 04]] §8); ResNet adds an identity path ([[05 - Convolutional Neural Network|ch. 05]] §14); the LSTM adds a path with gain $\prod F_j$ ([[07 - Recurrent Neural Network|ch. 07]] §9); self-attention makes the path length 1. Each deals with the same product of Jacobians.

### 9. Positional encoding (§11.6.3)

Self-attention ignores order: permuting the input permutes the output the same way. Position is added to the input:
$$p_{i,2j}=\sin\!\left(\frac{i}{10000^{2j/d}}\right),\qquad p_{i,2j+1}=\cos\!\left(\frac{i}{10000^{2j/d}}\right)$$

Frequencies fall along the columns: column 0 has wavelength 6.3, column 8 about 628, column 15 about 35,333. D2L compares it to a binary counter with continuous values.

For a fixed offset $\delta$, a $2\times2$ rotation independent of $i$ maps position $i$ to $i+\delta$:
$$\begin{pmatrix}\cos\delta\omega_j & \sin\delta\omega_j\\-\sin\delta\omega_j & \cos\delta\omega_j\end{pmatrix}\begin{pmatrix}p_{i,2j}\\p_{i,2j+1}\end{pmatrix}=\begin{pmatrix}p_{i+\delta,2j}\\p_{i+\delta,2j+1}\end{pmatrix}$$
(checked for $\delta=1,5,17$, all column pairs, 60 positions; max error $3.7\times10^{-15}$). So relative positions are reachable by a fixed linear map, and since the encoding is a formula, it extends to positions longer than those seen in training.

**Code (§11.6.3).**

```python
class PositionalEncoding(nn.Module):
    def __init__(self, num_hiddens, dropout, max_len=1000):
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        self.P = torch.zeros((1, max_len, num_hiddens))
        X = torch.arange(max_len, dtype=torch.float32).reshape(-1, 1) / torch.pow(
            10000, torch.arange(0, num_hiddens, 2, dtype=torch.float32) / num_hiddens)
        self.P[:, :, 0::2] = torch.sin(X)       # even columns
        self.P[:, :, 1::2] = torch.cos(X)       # odd columns
    def forward(self, X):
        X = X + self.P[:, :X.shape[1], :].to(X.device)
        return self.dropout(X)
```

Self-attention on its own (§11.6.1) maps $\mathbf x_1,\dots,\mathbf x_n$ to $\mathbf y_1,\dots,\mathbf y_n$ of the same shape: `MultiHeadAttention(...)(X, X, X, valid_lens)`. D2L notes continuous encodings are more space-efficient than binary ones.

### 10. The Transformer (§11.7)

**Encoder layer**: multi-head self-attention → add & LayerNorm → positionwise FFN → add & LayerNorm.
**Decoder layer**: masked self-attention → add & norm → encoder–decoder attention (queries from the decoder, keys/values from the encoder) → add & norm → FFN → add & norm.

The decoder's mask lets position $t$ attend only to positions $\le t$; without it the model sees the answer.

Parameters per encoder layer ($d_{\text{model}}=512$, $d_{\text{ffn}}=2048$; D2L gives no count):

| component | parameters | share |
|---|---|---|
| multi-head attention ($4d^2$) | 1,048,576 | 33.3% |
| positionwise FFN | 2,099,712 | 66.7% |
| 2 × LayerNorm | 2,048 | 0.1% |
| total | 3,150,336 | |

The FFN has twice the attention's parameters ($d_{\text{ffn}}/2d=2$). Attention is where the $O(n^2)$ computation is; the FFN is where most weights are. Six layers: 18,902,016 parameters (72.1 MB).

Most components come from earlier chapters:

| component | origin |
|---|---|
| residual connections | ResNet ([[05 - Convolutional Neural Network|ch. 05]] §14); they keep $d_{\text{model}}$ constant |
| layer normalization | like batch norm ([[05 - Convolutional Neural Network|ch. 05]] §13) but over features, so it works at any batch size and does not mix examples |
| positionwise FFN | the same MLP at every position, i.e. a $1\times1$ convolution |
| encoder–decoder, masking | §2 and §4 of this chapter |

Multi-head self-attention is the main new component. Layer norm is used instead of batch norm because batch statistics over padded variable-length sequences are unreliable.

**Components (§11.7).**

```python
class PositionWiseFFN(nn.Module):
    def __init__(self, ffn_num_hiddens, ffn_num_outputs):
        super().__init__()
        self.dense1 = nn.LazyLinear(ffn_num_hiddens)
        self.relu = nn.ReLU()
        self.dense2 = nn.LazyLinear(ffn_num_outputs)
    def forward(self, X):                        # same MLP at every position
        return self.dense2(self.relu(self.dense1(X)))

class AddNorm(nn.Module):
    def __init__(self, norm_shape, dropout):
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        self.ln = nn.LayerNorm(norm_shape)
    def forward(self, X, Y):                     # residual, then layer norm
        return self.ln(self.dropout(Y) + X)
```

On identical inputs at three positions, `PositionWiseFFN(4, 8)` returns identical rows. Layer norm vs batch norm on $\mathbf X=\begin{pmatrix}1&2\\2&3\end{pmatrix}$: layer norm (per row) gives $\begin{pmatrix}-1&1\\-1&1\end{pmatrix}$, batch norm (per column) $\begin{pmatrix}-1&-1\\1&1\end{pmatrix}$.

```python
class TransformerEncoderBlock(nn.Module):
    def __init__(self, num_hiddens, ffn_num_hiddens, num_heads, dropout, use_bias=False):
        super().__init__()
        self.attention = d2l.MultiHeadAttention(num_hiddens, num_heads, dropout, use_bias)
        self.addnorm1 = AddNorm(num_hiddens, dropout)
        self.ffn = PositionWiseFFN(ffn_num_hiddens, num_hiddens)
        self.addnorm2 = AddNorm(num_hiddens, dropout)
    def forward(self, X, valid_lens):
        Y = self.addnorm1(X, self.attention(X, X, X, valid_lens))
        return self.addnorm2(Y, self.ffn(Y))

class TransformerEncoder(d2l.Encoder):
    def __init__(self, vocab_size, num_hiddens, ffn_num_hiddens,
                 num_heads, num_blks, dropout, use_bias=False):
        super().__init__()
        self.num_hiddens = num_hiddens
        self.embedding = nn.Embedding(vocab_size, num_hiddens)
        self.pos_encoding = d2l.PositionalEncoding(num_hiddens, dropout)
        self.blks = nn.Sequential()
        for i in range(num_blks):
            self.blks.add_module("block"+str(i), TransformerEncoderBlock(
                num_hiddens, ffn_num_hiddens, num_heads, dropout, use_bias))
    def forward(self, X, valid_lens):
        # embeddings scaled by sqrt(d) so they are not swamped by encodings in [-1, 1]
        X = self.pos_encoding(self.embedding(X) * math.sqrt(self.num_hiddens))
        self.attention_weights = [None] * len(self.blks)
        for i, blk in enumerate(self.blks):
            X = blk(X, valid_lens)
            self.attention_weights[i] = blk.attention.attention.attention_weights
        return X
```

No encoder layer changes the shape: (2, 100, 24) stays (2, 100, 24).

```python
class TransformerDecoderBlock(nn.Module):
    def __init__(self, num_hiddens, ffn_num_hiddens, num_heads, dropout, i):
        super().__init__()
        self.i = i
        self.attention1 = d2l.MultiHeadAttention(num_hiddens, num_heads, dropout)
        self.addnorm1 = AddNorm(num_hiddens, dropout)
        self.attention2 = d2l.MultiHeadAttention(num_hiddens, num_heads, dropout)
        self.addnorm2 = AddNorm(num_hiddens, dropout)
        self.ffn = PositionWiseFFN(ffn_num_hiddens, num_hiddens)
        self.addnorm3 = AddNorm(num_hiddens, dropout)
    def forward(self, X, state):
        enc_outputs, enc_valid_lens = state[0], state[1]
        if state[2][self.i] is None:                 # training: whole sequence at once
            key_values = X
        else:                                        # prediction: append new token
            key_values = torch.cat((state[2][self.i], X), dim=1)
        state[2][self.i] = key_values
        if self.training:
            batch_size, num_steps, _ = X.shape
            dec_valid_lens = torch.arange(           # row t may see positions 1..t
                1, num_steps + 1, device=X.device).repeat(batch_size, 1)
        else:
            dec_valid_lens = None
        X2 = self.attention1(X, key_values, key_values, dec_valid_lens)   # masked self-attn
        Y = self.addnorm1(X, X2)
        Y2 = self.attention2(Y, enc_outputs, enc_outputs, enc_valid_lens) # cross-attn
        Z = self.addnorm2(Y, Y2)
        return self.addnorm3(Z, self.ffn(Z)), state
```

The causal mask is implemented with valid lengths $[1,2,\dots,T]$ per query row. At prediction time the block caches the representations of tokens generated so far in `state[2][i]` and needs no mask, because only past tokens exist. `TransformerDecoder` stacks the blocks after embedding × $\sqrt d$ + positional encoding, ends with `nn.LazyLinear(vocab_size)`, keeps `init_state = [enc_outputs, enc_valid_lens, [None] * num_blks]`, and stores both self- and cross-attention weights.

**Training (§11.7.6).** 2 encoder and 2 decoder blocks, $d=256$, **FFN hidden size 64**, 4 heads, dropout 0.2, Adam `lr=0.001`, batch 128, 30 epochs. (Mine: 1,869,782 parameters; each encoder block 296,256 and each decoder block 558,912. With an FFN narrower than $d$, attention holds most of the block's weights here, unlike the 512/2048 budget in the table above.)

Printed translations: "go ." → "va !" (1.000), "i lost ." → "j'ai perdu ." (1.000), "he's calm ." → "il est mouillé ." (**0.658**), "i'm home ." → "je suis chez moi ." (1.000). The third sentence means "he is wet" ("he's wet ." → "il est mouillé ." is training pair 273) yet scores 0.658, because "il est" and "." match: $p_1=3/4$, $p_2=1/3$, BLEU $=(3/4)^{1/2}(1/3)^{1/4}=0.658$. A wrong translation outscores the RNN's equally wrong one only through n-gram overlap. The encoder self-attention weights have shape (2 blocks, 4 heads, 9, 9); no query attends to padding.

D2L's summary: the Transformer is an encoder–decoder, but either half can be used alone; residual connections and layer norm make deep stacks trainable; the positionwise FFN applies one MLP to every position. Vision Transformers (§11.8) and large-scale pretraining (§11.9) build on it.

## From the lecture slides (8 Encoder–Decoder, 9 Attention Mechanism)

### 11. Lecture 8: the encoder–decoder in symbols

**Preprocessing (slide 3).**
- Read the parallel corpus.
- Tokenize into words and punctuation.
- Build a separate vocabulary for each language.
- Make every sentence exactly `num_steps` tokens, by truncating or padding with `<pad>` (§1).

**Encoder.** It reads $x_1,\dots,x_T$ with $\mathbf h_t=f(\mathbf x_t,\mathbf h_{t-1})$. A function $q$ then summarizes all states into a context vector:
$$\mathbf c=q(\mathbf h_1,\dots,\mathbf h_T)\qquad(\text{D2L and §2: }\mathbf c=\mathbf h_T)$$

**Decoder.** It models $P(y_{t'}\mid y_1,\dots,y_{t'-1},\mathbf c)$ with its own state:
$$\mathbf s_{t'}=g(\mathbf y_{t'-1},\mathbf c,\mathbf s_{t'-1})$$
- Its initial state is the encoder's final state.
- Each step outputs scores over the vocabulary, turned into probabilities by softmax and trained with cross-entropy.
- At prediction time the previous predicted token is fed back in (greedy decoding: "hello world ." → "bonjour le monde .").

**Beam search (slides 12–14).**
- **Search space.** With vocabulary $\mathcal Y$ (including `<eos>`) and maximum output length $T'$, there are $O(\vert\mathcal Y\vert^{T'})$ possible outputs. The slide writes $\vert\mathcal Y\vert^{T}$; $T$ is the *input* length, so it should be $T'$.
- **The algorithm.**
  - Keep the $k$ best first tokens.
  - At each later step, extend each of the $k$ candidates by every token, giving $k\vert\mathcal Y\vert$ candidates, and keep the $k$ best.
  - Finally, cut each candidate at its `<eos>`.
- **Example.** The slide's example ($k=2$, length 3, candidates A, C, AB, CE, ABD, CED) is D2L's (§3).

### 12. Lecture 9: attention worked by hand, and Luong attention

**Roles in encoder–decoder attention (slide 5):**

| role | source | meaning |
|---|---|---|
| key $K_i$ | encoder state $\mathbf h_i$ | what input word $i$ represents |
| value $V_i$ | encoder state $\mathbf h_i$ | the content to extract |
| query $Q$ | decoder state $\mathbf s_{t-1}$ | what the decoder is looking for now |
| weights $\alpha$ | softmax of scores | soft alignment between input and output |
| context $\mathbf c_t$ | $\sum_i\alpha_i V_i$ | passed to the decoder |

**Steps.**
1. Take $Q=\mathbf s_{t-1}$.
2. Score each key, e.g. $\text{score}(Q,K_i)=Q^\top K_i$.
3. Compute $\alpha_i=\dfrac{e^{\text{score}(Q,K_i)}}{\sum_je^{\text{score}(Q,K_j)}}$.
4. Form $\mathbf c_t=\sum_i\alpha_i\mathbf h_i$.
5. A dense layer with softmax predicts the next word from $\mathbf c_t$ and $\mathbf s_{t-1}$.

**Worked example (slides 7–11): "Tôi là người Việt Nam" → "I am Vietnamese".** The encoder gives $\mathbf h_1,\dots,\mathbf h_5$, one per source word.

| output | query | $\alpha$ over (Tôi, là, người, Việt, Nam) | context |
|---|---|---|---|
| I | $\mathbf s_0$ | (0.8, 0.05, 0.05, 0.05, 0.05) | mostly "Tôi" |
| am | $\mathbf s_1$ | (0.1, 0.7, 0.1, 0.05, 0.05) | mostly "là" |
| Vietnamese | $\mathbf s_2$ | (0.05, 0.05, 0.2, 0.35, 0.35) | "người Việt Nam" |

Each row sums to 1, and the context is $\mathbf c_t=\sum_i\alpha_{t,i}\mathbf h_i$; for "I", $\mathbf c_1=0.8\mathbf h_1+0.05(\mathbf h_2+\mathbf h_3+\mathbf h_4+\mathbf h_5)$. The weights are illustrative, not from a trained model. The third row shows the point of *soft* alignment: one output word can draw on three input words, which a fixed context vector cannot do selectively.

**Bahdanau attention (2015).** It scores the *previous* decoder state against each encoder state with a small feed-forward network:
$$e_{t,i}=\mathbf v_a^\top\tanh(\mathbf W_s\mathbf s_{t-1}+\mathbf W_h\mathbf h_i),\qquad \alpha_{t,i}=\frac{\exp(e_{t,i})}{\sum_j\exp(e_{t,j})},\qquad \mathbf c_t=\sum_i\alpha_{t,i}\mathbf h_i$$
This is additive attention (§4) with $\mathbf W_q=\mathbf W_s$, $\mathbf W_k=\mathbf W_h$, $\mathbf w_v=\mathbf v_a$, as used in §5. The slide's figure has a bidirectional encoder, $\mathbf h_i=[\overrightarrow{\mathbf h}_i,\overleftarrow{\mathbf h}_i]$.

**Luong attention (2015, not in D2L).** There are two differences from Bahdanau. First, the current decoder state $\mathbf s_t$ is computed before attending, and that state is the query. Second, the scoring is multiplicative, which is faster but can be less expressive. Three score functions:

| name | score $e_{t,i}$ | parameters |
|---|---|---|
| dot | $\mathbf s_t^\top\mathbf h_i$ | none; needs equal sizes |
| general | $\mathbf s_t^\top\mathbf W_a\mathbf h_i$ | $\mathbf W_a$; sizes may differ |
| concat | $\mathbf v_a^\top\tanh(\mathbf W_a[\mathbf s_t;\mathbf h_i])$ | like Bahdanau, but uses $\mathbf s_t$ |

Then, as before, $\alpha_{t,i}=\operatorname{softmax}_i(e_{t,i})$ and $\mathbf c_t=\sum_i\alpha_{t,i}\mathbf h_i$. In Luong et al.'s paper, $\mathbf c_t$ and $\mathbf s_t$ are then combined, as $\tanh(\mathbf W_c[\mathbf c_t;\mathbf s_t])$, to predict $y_t$. That detail is from the paper, not the slide. Scaled dot-product attention (§6) is Luong's dot score divided by $\sqrt d$.

**Self-attention and multi-head (slides 15–20).**
- **Projections.** $\mathbf Q=\mathbf X\mathbf W^Q$, $\mathbf K=\mathbf X\mathbf W^K$, $\mathbf V=\mathbf X\mathbf W^V$, and $\text{Attention}(\mathbf Q,\mathbf K,\mathbf V)=\operatorname{softmax}(\mathbf Q\mathbf K^\top/\sqrt{d_k})\mathbf V$. In the original Transformer $d_k=64=512/8$ (§6–7).
- **Multi-head.** $\text{MultiHead}(\mathbf Q,\mathbf K,\mathbf V)=\text{Concat}(\text{head}_1,\dots,\text{head}_h)\mathbf W^O$ with $\text{head}_i=\text{Attention}(\mathbf Q\mathbf W_i^Q,\mathbf K\mathbf W_i^K,\mathbf V\mathbf W_i^V)$. The slide's 8-head illustration shows the input passed through 8 sets of $\mathbf W_i^{Q,K,V}$, outputs $\mathbf Z_0,\dots,\mathbf Z_7$ concatenated and multiplied by $\mathbf W^O$ (§7).
- **The comparison table conflates two things.** Slide 20 contrasts "self-attention" (one sequence) with "multi-head attention" (several heads). These are independent choices: *self* vs *cross* says where $\mathbf Q,\mathbf K,\mathbf V$ come from, and *single* vs *multi-head* says how many attention functions run in parallel. The Transformer uses multi-head self-attention.
- **The Transformer** (slides 21–24) matches §10:
  - Encoder block: multi-head self-attention, add & norm, then an FFN (two linear layers with ReLU), add & norm.
  - Decoder block: masked self-attention, then cross-attention to the encoder, then the FFN, each with add & norm.
  - $N=6$ blocks in the original.

### 13. Encoder-only and decoder-only: BERT and GPT (lecture 9; D2L §11.9, §15.8–15.10)

D2L §11.9 sorts Transformers into three modes:

| mode | attention pattern | example | pretraining objective |
|---|---|---|---|
| encoder-only | every token attends to every token | BERT | masked language modelling |
| encoder–decoder | encoder: all-to-all; decoder: causal + cross-attention | original Transformer, T5, BART | translation; reconstructing corrupted spans (T5) |
| decoder-only | each token attends to itself and earlier tokens (causal) | GPT | next-token prediction (target = input shifted by one) |

**BERT** (Devlin et al. 2018; "Bidirectional Encoder Representations from Transformers") is a stack of Transformer encoder blocks.
- **Bidirectional.** A token's representation uses context on both sides, because nothing is masked in encoder self-attention.
- **Input.**
  - One text: `<cls>` text `<sep>`. Two texts: `<cls>` A `<sep>` B `<sep>`.
  - Each token's embedding is the sum of a token embedding, a segment embedding ($\mathbf e_A$ or $\mathbf e_B$) and a **learnable** positional embedding. The original Transformer's positional encodings are fixed sinusoids (§9).

Sizes (D2L §15.10):

| | layers | hidden size | heads | parameters |
|---|---|---|---|---|
| BERT-Base | 12 | 768 | 12 | 110 million |
| BERT-Large | 24 | 1024 | 16 | 340 million |

My count with a 30,522-token vocabulary, 512 positions, FFN width $4H$ and the pooler gives 109,482,240 and 335,141,888. D2L §11.9 once says "350-million-parameter BERT".

**Pretraining tasks:**
- **Masked language modelling (MLM).** 15% of tokens are selected for prediction. Of those, 80% are replaced by `<mask>`, 10% by a random token and 10% left unchanged. The `<mask>` token never appears during fine-tuning, and the mix reduces that mismatch. Slide example: "The cat [MASK] on the mat." → "sat".
- **Next sentence prediction (NSP).** Half the pairs are consecutive sentences ("IsNext"), half are random. A one-hidden-layer MLP on the `<cls>` representation classifies them. RoBERTa later found NSP of little use (D2L §11.9).

**Fine-tuning.** Add a small output layer, e.g. on `<cls>` for classification, and update all parameters. Tasks:
- text classification (sentiment);
- text-pair classification (paraphrase, inference);
- question answering (SQuAD);
- tagging (named-entity recognition).

Benchmarks: GLUE, SQuAD. Variants: RoBERTa, ALBERT (parameter sharing), DistilBERT (distillation), multilingual mBERT; D2L adds SpanBERT and ELECTRA.

**GPT** is a Transformer decoder trained as a language model.
- It drops the encoder *and* the cross-attention sublayer (D2L §11.9.3). The slide's GPT sketch still draws a cross-attention block, which a decoder-only model cannot have; the slide marks its figure "illustrative".
- **GPT** had 100 million parameters and was fine-tuned per task.
- **GPT-2** had 1.5 billion, trained on 40 GB of text, and handled several tasks without parameter updates.
- **GPT-3** was trained on 300 billion tokens and introduced in-context learning: zero-, one- and few-shot prompts, no gradient updates.

BERT suits understanding tasks (it sees the whole input); GPT suits generation (it produces one token at a time).

## ✏️ Exercises

> [!example]- **1.** *(Easy) BLEU by hand*
> **(a)** Target `A B C D E F`, prediction `A B B C D`: $p_1$ to $p_4$. **(b)** BLEU with $k=2$. **(c)** Prediction `A B`, $k=2$. **(d)** What are the weaknesses?
>
> ---
> **(a)** $p_1=4/5$ (only one `B` counts), $p_2=3/4$ (`AB`, `BC`, `CD`), $p_3=1/3$ (`BCD`), $p_4=0/2$.
>
> **(b)** Brevity penalty $\exp(1-6/5)=0.8187$. BLEU $=0.8187\times0.8^{1/2}\times0.75^{1/4}=0.6815$.
>
> **(c)** $p_1=p_2=1$, penalty $e^{-2}=0.1353$, BLEU 0.1353.
>
> **(d)** Precision alone rewards very short outputs (only the brevity penalty prevents that), and one zero precision makes the whole score zero.

> [!example]- **2.** *(Easy–medium) Greedy vs beam*
> **(a)** Verify the two sequence probabilities. **(b)** Why does greedy miss the better one? **(c)** Cost of greedy, beam ($k=5$), exhaustive at $|\mathcal Y|=10^4$, $T'=10$. **(d)** Why normalize by length?
>
> ---
> **(a)** 0.048 and 0.054; greedy's is 11.11% lower.
>
> **(b)** The better path takes the second-best token at step 2, and later probabilities depend on that choice. Greedy never revisits it.
>
> **(c)** $10^5$, $5\times10^5$, $10^{40}$.
>
> **(d)** Log-probabilities only decrease as a sequence grows, so short outputs win unless scores are normalized.

> [!example]- **3.** *(Medium) The $\sqrt d$*
> **(a)** Show $\operatorname{Var}[\mathbf q^\top\mathbf k]=d$. **(b)** What happens to the softmax at $d=512$ without scaling? **(c)** Why does that stop learning?
>
> ---
> **(a)** $\sum_i q_ik_i$: each term has mean 0 and variance 1, and they are independent, so the variance is $d$ (simulated 510.44 at $d=512$).
>
> **(b)** Logit sd 22.63; max weight 0.9523; entropy 0.117 of 2.303 nats.
>
> **(c)** The softmax Jacobian $p_i(\delta_{ij}-p_j)$ is near zero for a one-hot $p$. With scaling the entropy is 1.92 and gradients flow.

> [!example]- **4.** *(Medium–hard) Count a Transformer layer*
> $d_{\text{model}}=512$, $d_{\text{ffn}}=2048$, $h=8$. **(a)** Attention parameters; does $h$ matter? **(b)** FFN parameters. **(c)** Which dominates? **(d)** Six layers in MB.
>
> ---
> **(a)** $4\times512^2=1{,}048{,}576$, independent of $h$.
>
> **(b)** $512\cdot2048+2048+2048\cdot512+512=2{,}099{,}712$.
>
> **(c)** FFN 66.7%, attention 33.3%.
>
> **(d)** $6\times3{,}150{,}336=18{,}902{,}016$ parameters, 72.1 MB in fp32; with Adam training state ([[04 - Neural Network|ch. 04]] §5), 288.4 MB.

> [!example]- **5.** *(Hard) Why attention replaced recurrence*
> **(a)** Complexity, sequential ops and path length for RNN, CNN, self-attention. **(b)** When is self-attention cheaper than an RNN? **(c)** What does path length 1 buy, using ch. 07 §7? **(d)** So why did attention win?
>
> ---
> **(a)** RNN $O(nd^2)$, $O(n)$, $O(n)$; CNN $O(knd^2)$, $O(1)$, $O(n/k)$; self-attention $O(n^2d)$, $O(1)$, $O(1)$.
>
> **(b)** When $n\lt d$; at $d=512$, below 512 tokens.
>
> **(c)** The allowed Jacobian range widens from ±0.693% (length 1000) to $[0.001, 1000]$ (length 1): no long product remains.
>
> **(d)** Not speed in general (it is worse for $n>d$), but short gradient paths and full parallelism over positions.

## 📝 Summary

- Seq2seq uses two vocabularies, padding with valid lengths, and `<bos>`/`<eos>`/`<unk>`; masks appear in the loss, the softmax and the decoder.
- Encoder–decoder: variable input → fixed state → variable output. Teacher forcing causes exposure bias.
- BLEU = brevity penalty × product of clipped n-gram precisions; one zero precision gives 0, so single-reference sentence BLEU is a weak quality measure. D2L's weights $1/2^n$ make long n-grams count less (D13).
- D2L's MT demo: 512 training pairs (2,136 target tokens), ~1.9M parameters per model, `num_steps=9`, `min_freq=2`. Three of its four test sentences are training pairs; the unseen one comes out as another sentence's memorized translation in all three models.
- Greedy picks the best token, not the best sequence. Beam search costs $k$× greedy and far less than exhaustive search; normalize by length.
- Attention is a soft, differentiable lookup; dot-product attention is a simplified Gaussian kernel.
- Bahdanau attention recomputes the context per output step, removing the fixed-vector bottleneck and shortening gradient paths.
- Scale dot products by $1/\sqrt d$, or the softmax saturates and gradients vanish.
- Multi-head attention costs $4p_o^2$ for any number of heads.
- Self-attention is cheaper than an RNN when $n\lt d$, has path length 1 and runs in parallel.
- Sinusoidal positional encodings supply order; relative shifts are fixed rotations.
- A Transformer layer is about two-thirds FFN parameters at 512/2048; it combines residual connections, layer norm and position-wise MLPs with multi-head self-attention.
- Code: `masked_softmax` (−1e6 fill), `bmm`, `DotProductAttention`, `AdditiveAttention`, `MultiHeadAttention` (heads folded into the batch axis), `PositionalEncoding`, `AddNorm`, `PositionWiseFFN`, encoder and decoder blocks; the causal mask is `dec_valid_lens = [1..T]`, and prediction caches past keys/values per block.
- Nadaraya–Watson kernel regression is attention with a fixed kernel; deep attention learns the queries and keys.

## ⚠️ Important Notes

1. Do not treat single-reference, sentence-level BLEU as a quality score; inspect examples too.
2. Normalize beam scores by length.
3. Larger beams find more probable outputs, which are not always better (they favour short, generic text); $k$ is a hyperparameter.
4. Always include the $1/\sqrt d$ scaling; without it training stalls silently.
5. Mask decoder self-attention, or the model sees future tokens.
6. Without positional encoding, self-attention treats the input as a bag of tokens.
7. Attention's $O(n^2)$ is also memory: at $n=4096$, 8 heads, 12 layers the attention matrices are about 1.6 billion floats, kept for the backward pass. Sequence length often limits GPU memory more than model size.
8. Use layer norm, not batch norm, for variable-length padded batches.
9. Multi-head is "free" only with per-head size $p_o/h$; check the convention before comparing parameter counts.
10. Teacher forcing means one early error at inference time can compound (scheduled sampling is one fix; D2L does not use it).
11. Cross-attention is where source and target meet; inspect it when translations are fluent but wrong.
12. Attention weights show what was read, not necessarily what influenced the output.
13. Evaluate translation on held-out data. D2L's four demo sentences are mostly training pairs, so their BLEU of 1.0 shows memorization, not generalization.
14. Length normalization $1/L^\alpha$ helps longer candidates; it does not penalize them (D14).
15. Scale embeddings by $\sqrt d$ before adding sinusoidal encodings, or position swamps content.
16. The decoder's initial state is the encoder's final state only if both have the same layers and width; otherwise add a projection.
17. `nn.Embedding` is a lookup of learned rows, equivalent to one-hot × weight matrix.
18. Bahdanau queries with the previous decoder state $\mathbf s_{t-1}$ and an additive score; Luong first computes $\mathbf s_t$ and scores multiplicatively (dot, general, concat).
19. Self vs cross attention and single vs multi-head are independent axes; the Transformer encoder uses multi-head self-attention, its decoder also multi-head cross-attention.
20. BERT = encoder-only, bidirectional, MLM (15%: 80/10/10) + NSP, learnable positions; GPT = decoder-only, causal, next-token prediction, no cross-attention.

> [!warning] Gaps in the source material
> - **Figures:** greedy/beam probability trees, attention pooling, multi-head and Transformer diagrams are reconstructed from the prose (the trees' probabilities are in the text). Lost: attention heatmaps, kernel-regression plots, positional-encoding plots, and all training curves, so no loss or BLEU curves are quoted.
> - **Added by me:** the BLEU zero-precision analysis; the beam cost comparison and length-normalization reasoning; the softmax saturation simulation; the multi-head parameter table; the $n\lt d$ crossover; the path-length argument and the cross-chapter link (ch. 04, 05, 07, 08); the positional-encoding rotation check; the Transformer parameter budget and inheritance table; the memory and interpretability cautions. Multiple-reference BLEU and exposure bias are named beyond D2L.
> - **Correction:** exercise 1(b)'s BLEU is 0.6815 (an earlier version of this note said 0.6816). An earlier version also repeated D2L's claim that longer n-grams carry more weight; it is the reverse (D13).
> - **Discrepancies:** D13 (BLEU weighting described backwards), D14 (length normalization said to penalize long sequences).
> - **Checked against the real data** (fra-eng.zip, SHA-1 matching D2L's): positions of D2L's test sentences in the 641 loaded pairs, the memorized outputs (pairs 77, 173, 273), vocabulary sizes, `<unk>` rate and token counts; parameter counts of the three models.
> - **Lost:** Nadaraya–Watson fit plots and all attention heatmaps and loss curves (images); their conclusions are stated in the text.
> - **Skipped:** plotting helpers; vision Transformers (§11.8). Large-scale pretraining (§11.9) is summarized in §13 because the lecture covers BERT; the BERT pretraining code (§15.9–15.10) belongs to the NLP subject.
> - **Lecture slides (8, 9), added 2026-11-17:** §11–13. BERT and GPT are now covered at overview level from D2L §11.9 and §15.8–15.10 (the pretraining code in §15.9–15.10 is left to the NLP subject). Luong attention is not in D2L: the three scores come from the slide, the $\tanh(\mathbf W_c[\mathbf c_t;\mathbf s_t])$ step from the paper. Flagged: $\vert\mathcal Y\vert^{T}$ → $\vert\mathcal Y\vert^{T'}$; the self vs multi-head table; the cross-attention block in the GPT sketch. The BERT parameter count is mine.

**Previous:** [[07 - Recurrent Neural Network]] · **Next:** end of subject (see [[00-Index]])
