# PA-ODR: 重複適合の動作例(feasibility graph $G(e)$)

`tex/slides.tex` の PA-ODR 4〜6 に入れた TikZ 図の Mermaid 版。
凡例は全図共通で、**太い赤線 = 採用された辺**、細い灰線 = $G(e)$ にあるが不採用、
灰の破線 = 辺はあるが容量 0、点線枠 = $\sigma(i)+k < e-\delta$ で不適格。

---

## 例 A: 基準 1 が選好を上書きし、de-reserve は起きない

$q^o=q^{t_1}=q^{t_2}=1$, $k=5$, $\delta=10$;
$i_1(100,\emptyset)$, $i_2(88,\{t_1,t_2\})$ [$t_2 \succ t_1 \succ o$], $i_3(84,\{t_1\})$, $i_4(86,\{t_2\})$

$\mu_o=\{i_1\}$, $e=100$ なので admissible の条件は $\sigma(i)+5 \ge 90$。

```mermaid
graph LR
  subgraph S["学生(open に入らない者)"]
    i2["i₂ · 88+5 = 93 ✓"]
    i3["i₃ · 84+5 = 89 ✗"]
    i4["i₄ · 86+5 = 91 ✓"]
  end
  subgraph C["留保カテゴリ(q̂ = 1)"]
    t1["t₁"]
    t2["t₂"]
  end
  i2 === t1
  i2 -.- t2
  i4 === t2
  classDef dead stroke:#aaa,stroke-dasharray:4 3,color:#888
  class i3 dead
  linkStyle 0 stroke:#c0392b,stroke-width:3px
  linkStyle 1 stroke:#999,stroke-width:1px
  linkStyle 2 stroke:#c0392b,stroke-width:3px
```

最大カーディナリティ 2 を達成する割当は $i_2 \mapsto t_1$, $i_4 \mapsto t_2$ の**一意**。
$i_2$ は $t_2$ を好むのに $t_1$ へ回される — 重複適合者の行き先は**まず基準 1 が決める**。
全席が埋まるので即停止($\hat q$ 不変)、gap は $7, 9 \le \delta$。

---

## 例 B: 振り分けが de-reservation を連鎖させる

$i_1(100,\emptyset)$, $i_2(95,\{t_1,t_2\})$ [$t_1 \succ t_2 \succ o$], $i_3(82,\{t_2\})$,
$q=(1,1,1)$, $k=5$, $\delta=10$

### 反復 1: $G(100)$、条件 $\sigma(i)+5 \ge 90$

```mermaid
graph LR
  subgraph S1["学生"]
    i2["i₂ · 95+5 = 100 ✓"]
    i3["i₃ · 82+5 = 87 ✗"]
  end
  subgraph C1["留保カテゴリ"]
    t1["t₁ (q̂ = 1)"]
    t2["t₂ (q̂ = 1) → 空"]
  end
  i2 === t1
  i2 -.- t2
  classDef dead stroke:#aaa,stroke-dasharray:4 3,color:#888
  class i3 dead
  linkStyle 0 stroke:#c0392b,stroke-width:3px
  linkStyle 1 stroke:#999,stroke-width:1px
```

$i_2$ はどちらのカテゴリでも加点後 100 で「弱すぎる候補」ではない。
基準 3 が第一志望 $t_1$ へ流したこと自体が $t_2$ を空にする → $t_2$ を de-reserve。

### 反復 2: $G(95)$、条件 $\sigma(i)+5 \ge 85$

```mermaid
graph LR
  subgraph S2["学生(i₁, i₂ は open に吸収済)"]
    i3b["i₃ · 82+5 = 87 ✓"]
  end
  subgraph C2["留保カテゴリ"]
    t1b["t₁ (q̂ = 1) → 候補なし"]
    t2b["t₂ (q̂ = 0)"]
  end
  i3b -.- t2b
  linkStyle 0 stroke:#999,stroke-width:1.5px,stroke-dasharray:6 4
```

$i_3$ は今回 admissible になるが、唯一の適合先 $t_2$ の容量は既に 0。
$t_1$ には辺が無い($i_2$ が open に吸収された)ので、再び de-reserve。

### 反復の連鎖

```mermaid
flowchart TD
  A["反復 1<br/>q̂ = (1,1,1), e = 100<br/>μ_o = {i₁}, t₁ ← i₂, t₂ 空"]
  B["反復 2<br/>q̂ = (2,1,0), e = 95<br/>μ_o = {i₁,i₂}, t₁ 候補なし"]
  C["反復 3<br/>q̂ = (3,0,0), e = 82<br/>μ_o = {i₁,i₂,i₃} で停止"]
  A -->|"t₂ を de-reserve"| B
  B -->|"t₁ を de-reserve"| C
```

3 人全員がマッチするが**両方の留保枠が消滅**する。
同じ事例で TA-DA は $\mu_o=\{i_1\}$, $\mu_{t_1}=\{i_2\}$ と枠を保ったまま 2 人を取る。

---

## 例 C: 重複適合者は虚偽申告で得をしうる

$i_1(100,\emptyset)$, $i_2(95,\{t_1,t_2\})$, $i_3(94,\{t_1,t_2\})$, $q=(1,1,1)$, $k=5$, $\delta=10$。
真の選好は $t_1 \succ_{i_2} t_2 \succ_{i_2} o$、$o \succ_{i_3} t_1 \succ_{i_3} t_2$。
$\mu_o=\{i_1\}$, $e=100$ で 4 辺すべてが現れ、基準 1–2 は両者のマッチを確定させる。

```mermaid
graph LR
  subgraph S3["学生"]
    i2c["i₂ · 100 ✓"]
    i3c["i₃ · 99 ✓"]
  end
  subgraph C3["留保カテゴリ"]
    t1c["t₁"]
    t2c["t₂"]
  end
  i2c --- t1c
  i3c --- t2c
  i2c --- t2c
  i3c --- t1c
  linkStyle 0 stroke:#2563eb,stroke-width:3px
  linkStyle 1 stroke:#2563eb,stroke-width:3px
  linkStyle 2 stroke:#ea580c,stroke-width:3px,stroke-dasharray:6 4
  linkStyle 3 stroke:#ea580c,stroke-width:3px,stroke-dasharray:6 4
```

青実線 = 割当 $\alpha$($i_2 \mapsto t_1$, $i_3 \mapsto t_2$)、
橙破線 = 割当 $\beta$($i_2 \mapsto t_2$, $i_3 \mapsto t_1$)。決めるのは基準 3 だけ。

| $i_2$ の申告 | $\alpha$ | $\beta$ | 選択 |
|---|---|---|---|
| 真 $t_1 \succ t_2 \succ o$ | $(3,1)$ | $(2,2)$ | $\beta$: 第二志望 $t_2$ |
| 偽 $t_1 \succ o \succ t_2$ | $(3,1)$ | $(3,2)$ | $\alpha$: 第一志望 $t_1$ |

値は順位ベクトルの降順ソート、辞書式に小さい方が選ばれる。
$t_2$ を $o$ の下に落とすと $r_{i_2}(t_2)$ が $2 \to 3$ となり、$\beta$ の評価**だけ**が悪化する。
単一適合では起こりえない(振り分けの余地がないため)。

---

数値・反復トレースは `algorithms/admissions.py` の `pa_odr` で実行して再現を確認済み。
本文での対応箇所は `icaart_26___score/main.tex` の Remark `sec:trigger`(例 B)、
Prop. `paodr-notsp`(例 C)、および 527 行以降のコメントアウト部分(例 A)。
