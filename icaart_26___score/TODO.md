# ICAART 2027 投稿 TODO

対象: `main.tex`（Fair Admissions with Overlapping Reserve Categories under Score Constraints）
最終更新: 2026-08-18

## 投稿先の規定

| 項目 | 規定 |
|---|---|
| Regular Papers 締切 | **2026-09-30** |
| Position Papers 締切 | 2026-11-13 |
| 投稿時の分量 | **10,000〜50,000字（空白を除く）**。逸脱は査読に回らない |
| Full Paper 採択時 | 12ページ（+4ページは有料） |
| Short Paper 採択時 | 8ページ |
| 査読 | double-blind（著者情報なし） |

出典: <https://icaart.scitevents.org/Guidelines.aspx> / <https://icaart.scitevents.org/callforpapers.aspx>

---

## 【最優先・要著者判断】AyTu23b の置換ペーパーを特定する

本稿の **δ制約（Ashoka Kumar Thakur 判決の10点ルール）の根拠そのもの**である

> Aygün, O. and Turhan, B., *Inconsistency of Score-Elevated Reserve Policy for Indian
> Affirmative Action*, arXiv:2312.14648 (v2, 2023-12-26)

が、[Turhan 氏の研究ページ](https://sites.google.com/site/bertanturhan/research) で
**"Subsumed and Replaced Papers"**（吸収・置換済み論文）に分類されている。

同ページで同じく subsumed 扱いになっているもの:

1. Over-and-Above Implementation of Reserve Policy in India (arXiv:2305.11758)
2. A Tale of Two Supreme Court Rulings on Indian Affirmative Action
3. **Inconsistency of Score-Elevated Reserve Policy** ← 本稿が依拠

**ページ上に「どの論文が置換したか」の明示はない。** 置換先の候補:

- **"Reconciling Affirmative Action and Merit in India: An Axiomatic Analysis"**
  (Aygün & Turhan, under review) — タイトルから merit/cutoff の緊張を扱っており最有力。
  ただし 2026-08-18 時点で arXiv・SSRN いずれにも公開版が見つからない。
- **"Affirmative Action in India with Hierarchical Reservations"** (arXiv:2602.09189, under review)
  — 公開済みだが、内容は overlapping horizontal categories の階層処理であり、
  10点ルール／score-elevation の inconsistency 論とは別筋に見える。
- "How to Implement Reservation Policy in India" (Aygün & Turhan, WINE 2024)
  — 査読付き会議録。1 の置換先である可能性が高い。

### やること

- [ ] Aygün 氏または Turhan 氏に直接照会し、`AyTu23b` の正式な置換先を確認する
- [ ] 置換先が判明したら `references.bib` の `AyTu23b` を差し替え、
      Introduction 第2段落と "Relation to the closest prior work" の記述を更新する
- [ ] それまでは arXiv ID 付きプレプリントとして引用を維持する（現状の bib はその形）

**CLAUDE.md の「ワーキングペーパーの引用」禁止・「最新版を引用」に抵触するため、
投稿前に必ず解消すること。** 本稿の中核制約の出典であり、査読者が最初に当たる文献でもある。

---

## 分量: 投稿要件クリア（2026-08-27）

| | 規定 | 0826改稿後 | 圧縮後 | **削減後（現在）** |
|---|---|---|---|---|
| 非空白文字数（参考文献・表・図込み） | ≤50,000 | 67,362 | 62,124 | **49,986** ✅ |
| ページ数（tectonic 実測） | 12 | 17 | 16 | **13**（あと1ページ） |

- **投稿を止める文字数制限（50,000）はクリア。** 概算スクリプトなので ±10% の誤差はある
- ページは13。Full Paper 採択時は12ページだが **+4ページは有料**なので提出自体は可能。
  査読後に本文が動くので、camera-ready 時に再測定すること
- コンパイル: error 0 / Overfull hbox 0 / 未定義参照 0

### 削除したもの（バックアップ `main.tex.before_cuts`）

1. **`\subsection{Order Dependence and Non-Minimality}` 全体**（Ex.~order、非最小性の議論、
   MinDeres Remark、Csáji--Sun 段落）。順序依存の主張は Lemma monotone を畳んだ2文と
   Conclusion の open question に残した
2. **nremark 6個すべて**。中身は本文に畳み込み済みで、主張は落としていない:
   - `rem:overlap-cause`（2原因の切り分け）→ Prop. spse-not-sf 直後の段落
   - `rem:hall`（Hall 障害）→ Prop. impossibility 直後の段落
   - `rem:computation`（多項式時間）→ Lemma matroid 直後の段落
   - `rem:tada-nw`（NW の射程）→ Ex. tada-idle 直後の段落
   - `sec:trigger`（何が de-reservation を起こすか）→ 削除（Prototype 第4読みに要約が残る）
3. **TA-DA を落として A-STDA に一本化**。走査版 Algorithm 2 と Lemma「走査は失敗しない」を削除し、
   `prop:tada-props` を A-STDA の命題（停止性を含む）に書き換え。
   Ex.~tada-idle も A-STDA の2反復として記述し直した（同じ出力になることは実測で確認済み）。
   **0826 スライドの3本立て（SPSE / PA-ODR / A-STDA）と一致した**
4. **Prototype 第2ファミリ（|I|=500）**。表・本文の数値をすべて2ファミリに修正
5. Lemma「open cutoff は単調に下がる」→ 散文に吸収

### 圧縮したもの（主張は不変）

- 全節の散文を2周、証明14本、example 3本を引き締め
- レイアウト: Algorithm 1・3 を `algorithm*`（段抜き）→ `algorithm`（1段）に、
  表を `\footnotesize` + `tabcolsep` 詰めに。**内容ゼロ損失で約1ページ分**

### 残っているもの（すべて維持）

4つの公平性の定義と入れ子補題、SPSE / A-STDA / PA-ODR の全命題と証明、
不可能性定理、PA-ODR の反例2つ（|T|=1 と reserve 内のみ）、実験2ファミリ。

---

## 完了済み（2026-08-27）— 進捗_マスター_0826 ミーティング反映

`進捗/main.tex`（0826 ミーティング修正後スライド）の内容に合わせて公平性の定義体系を入れ替えた。
バックアップ: `main.tex.before_0826_meeting`

### 定義の変更

- **swap stability を全面削除**（`def:swap` / `lem:nje-swap` / TA-DA の swap 節 /
  `prop:paodr-swap`）。スライドの注記「旧版は Alcalde (1995) の exchange stability に
  基づいていたが…定義に変更した」に従った。criterion 3 の存在理由は
  「reserve 間の交換要求は依然として満たす」という2〜3行の議論として PA-ODR 節に残した
- **within-category fairness を強化**: 条件 (iv) を `i ∉ M(μ)` から `t ≻_i μ(i)` に変更。
  旧定義は `def:fair-unm`（Fairness against unmatched claimants）として残した
- **across-category fairness を新設**（`def:across`）。c' を V 全体に走らせた版
- **`lem:hierarchy`**: nje ⇒ across ⇒ within ⇒ unmatched の入れ子関係を証明付きで追加

### 証明（スライドの「証明スケッチ」を本文の証明に）

- SPSE: `prop:spse-nje` の系として across/within/unmatched を導出
- TA-DA: `prop:tada-props` の within+swap 証明を **across-category fairness の2場合分け**
  （閾値内 = DA の標準論法 / 閾値で排除 = 排除条件から σ_t(j) > σ_t(i)）に置換
- A-STDA: `prop:astda` に across を追加。スライドが「要補題」としていた
  **τ* の不動点性は不要**であることを明記（場合分けは τ* 自身で回り、
  e_o(μ) ≤ τ* は score-feasibility にしか使わない）
- PA-ODR: **`prop:paodr-unfair` を新設**（within/across を満たさない）。
  スライドの反例は既存の `ex:paodr-envy` と同一インスタンスなので流用し、
  さらに **open カテゴリを含まない reserve 内だけの反例**
  （i1(100,∅), i2(95,{t1,t2}), i3(90,{t2}), t2 ≻_{i2} t1）を追加した。
  どちらも score-relative 読みでも成立することを確認済み

**スライドの比較表は PA-ODR の within を ✓ としているが、同スライドの反例と矛盾する。
反例が新しい内容なので反例側を採用した（表 `tab:comparison` は × に修正済み）。**

### 実験の再実行（`scripts/paper_table.py` を新設）

`algorithms/admissions.py` に定義どおりの判定関数を追加
（`realized_score_feasible` / `effectively_score_feasible` / `non_wasteful` /
`non_wasteful_plain` / `within_category_fairness_strong` / `across_category_fairness` /
`no_justified_envy`）。seed 100・3ファミリ・各100件で 4メカニズムを再測定した。

- 旧表の数値は再現した（SPSE score-feas. 54/52/45、matched 62.97/187.33/55.48 など）
- 表2に **A-STDA 行**と **Across-fair 列**を追加。時間は本セッションの実測値に更新
- 主要な新事実:
  - across-category fairness は SPSE / TA-DA / A-STDA で **600/600 成立**、
    PA-ODR は 0/0/63。**no justified envy と綺麗に分離する**
    （TA-DA の nje 違反は全て「空席」に対する不満で、across はその節を落としている）
  - PA-ODR は across と nje が完全に一致（停止時に全枠が埋まるので空席の不満が出ない）
  - within（新定義）と across は 1,200 回すべてで一致 → PA-ODR の損失は open 枠に限らない
  - A-STDA は TA-DA と 100/100/78 で完全一致、割当人数は常に同じ
- δ 感度（34,43,54,79,97 / 30.32,26.38,18.57,7.84,0.61）と overlap 0.15 の 6/100 も再現

### 未着手

- スライドの A-STDA 動作例（A/B/C/D, 2反復で停止）は**分量の都合で本文に入れていない**
- スライドのまとめにある「加点だけして留保カテゴリを考えずに全員割り当てる」案は
  Conclusion の open question に1文だけ入れた

---

## 完了済み（2026-08-18）

### 引用文献の実在確認（2026-08-18, 29件すべて）

`main.tex` が `\cite` している29キー全件を arXiv API と Crossref API で照合した。
**捏造・存在しない文献はゼロ。** バックアップ: `references.bib.before_ref_check`

修正済み（3件）:

| key | 誤 | 正 | 出典 |
|---|---|---|---|
| `DKT23a` | Matching Mechanisms for Refugee **Settlement** | Refugee **Resettlement** | AER 113(10) 2689–2717, doi:10.1257/aer.20210096 |
| `ABB24a` | number={1} | number={1--2}（合併号） | Math. Prog. 203(1-2) 247–269, doi:10.1007/s10107-022-01917-1 |
| `Roth08a` | number={3} | number={3--4}（合併号） | IJGT 36(3-4) 537–569, doi:10.1007/s00182-008-0117-6 |

要判断（1件）:

- `Glit26a`（Near-Feasible Stable Matchings）は **AAMAS 2026（Paphos, 2026-05-25/29,
  IFAAMAS, doi:10.65109/rzem3915）に extended abstract として採録済み**。
  ただし arXiv 側の note が "EA to appear at AAMAS 2026" であり、本文が引用している
  incentive 分析はフルバージョン（arXiv:2602.10851v1）にしかない。
  arXiv のまま維持するか、AAMAS 版を併記するかは著者判断。Crossref にページ番号はまだない

確認結果（問題なし）:

- arXiv 5件は API で実在・著者・タイトル一致を確認:
  2312.14648v2 (2023-12-26) / 2602.09189v2 (2026-02-17) / 2604.27823v1 (2026-04-30) /
  2602.10851v1 (2026-02-11) / 2504.04689**v4 (2026-06-10)**
  ※ `HuZh25a` は v4 が最新（bib は版指定なしなので最新版に解決される）
- Crossref 掲載24件は誌名・巻・号・ページ・年・著者姓すべて bib と一致
- `KaKo24a`（REStud 91(2) 1162–1199）は Crossref の issued が 2023（online-first）だが
  冊子体は 2024。`AyTu23a` と同じ online-first のずれで、bib の 2024 のままでよい
- `KoSo16a` は DOI 未記載だが実在（TE 11(2) 683–710, doi:10.3982/te1839）

未解決のまま残るもの:

- `AyTu23b` は依然として著者ページで "Subsumed and Replaced" 扱い（本ファイル冒頭の項目）。
  arXiv 上の実在は確認済みだが、置換先の照会は未了

### A-STDA（adaptive 版）の追加 — `swap公平性追加.pptx` スライド 16〜20 より

- 本文: `\subsection{An Adaptive Variant}`（`sec:astda`）を TA-DA 節末に追加。
  τ←−∞ → DA(τ) → e_o(μ)≤τ なら停止、そうでなければ τ←e_o(μ) という不動点反復。
  `Proposition~\ref{prop:astda}`（停止は高々 |I|+1 回の DA、score-feasible、
  within-category fair、swap stable）を証明付きで追加
- 参考文献: スライドの文献リストのうち本文未引用だったのは **Roth (2008)** のみだったので
  `\cite{GaSh62a,Roth08a}`（DA の標準）と `\cite{AyTu20a}`（dynamic reserves = 閾値を
  自分が生む cutoff に合わせる発想の出所）として A-STDA 節に引用した。他は既に引用済み
- 実装: `algorithms/admissions.py` の `adaptive_score_threshold_da`。
  スライド20の動作例（A=100,B=92,C=80,D=78）を再現することを確認済み
- 検証スクリプト: `scripts/check_astda.py`。ランダム4,000件で
  停止までの DA 実行回数は常に2回、score-feasible 4000/4000、
  TA-DA と出力一致 3,775/4,000、A-STDA の方が少なくマッチ 35件、多いことは0件

### 【要判断】Remark~\ref{rem:tada-nw} の open question に反例が見つかった

本文は「TA-DA が Def.~\ref{def:nw}（score-relative 非浪費性）を一般に満たすかは未解決、
実験では全インスタンスで成立」としているが、**3人インスタンスで反例が出た**:

    T={t1,t2}, q^o=2, q^{t1}=q^{t2}=1, k=5, δ=10
    i1(96, ∅) は o のみ、i2(74, {t1}) は t1≻o、i3(72, {t2}) は t2≻o

- e=96: A_{i2}=A_{i3}={o}（79<86, 77<86）→ μ_o={i1,i2}、留保は空、i3 は未割当。
  留保が空なので score-feasible。マッチ2人
- e=74, 72: μ_o={i1}, μ_{t1}={i2}, μ_{t2}={i3} で e_o−e_{t1}^+=96−79=17>δ → 棄却
- よって TA-DA の出力は μ_o={i1,i2}。ところが i3 を t2 に入れると
  e_o=74, e_{t2}^+=77 で gap=−3≤δ、容量も空いている → **Def.~\ref{def:nw} 違反**
- Remark~\ref{rem:tada-nw} が「未解決」としていた $e>e_o(\mu)$ のケースそのもの
  （e=96 > e_o(μ)=74）。同じ例で A-STDA も違反する
- ランダム4,000件では TA-DA 11件・A-STDA 12件の違反率（Prototype の3ファミリ300件では
  両者とも違反なし ＝ Table~\ref{tab:prototype} の記載は有効）

反映するなら Table~\ref{tab:comparison} の TA-DA 行、Remark~\ref{rem:tada-nw}、
Conclusion の第2 open question、Contribution 4 の4箇所を同時に直す必要がある。
**主張を変える修正なので未実施。**

### 【要修正】`is_score_feasible()` が Definition~\ref{def:scorefeas} と食い違う

`algorithms/admissions.py` の `is_score_feasible` は
`len(μ_o) < q^o` のとき無条件に True を返す。Definition~\ref{def:scorefeas} は
μ_o が**空**のときだけ vacuous なので、「非空だが定員割れ」の場合に食い違う。
上の3人インスタンスでは、この分岐のせいで実装版 TA-DA が
e=74 の候補（gap 17 > δ=10）を score-feasible と誤判定して出力してしまう。

- Prototype の3ファミリ300件では実装版と Definition 準拠版の出力は**全件一致**し、
  Table~\ref{tab:prototype} の数値に影響はない（定員割れは |I|=60 の12件で発生したが結果は同じ）
- ただし実装としては誤りなので投稿用コード公開前に要修正

### swap stability（across category fairness）の反映 — `swap公平性追加.pptx` より

スライド 21〜23 の内容を本文に取り込んだ。バックアップ: `main.tex.before_swap`

- `Definition~\ref{def:swap}`（Blocking swap / swap stable / swap stable within reserves）を
  Model 節の Def.~\ref{def:nje} の直後に追加。スライド通り「留保のみ」と「一般カテゴリ込み」の2版
- `Lemma~\ref{lem:nje-swap}`：**共通加点の下では no justified envy ⇒ swap stability**。
  スライドは SPSE について拒否連鎖で直接示していたが、SPSE は既に Prop.~\ref{prop:spse-nje} で
  no justified envy を持つので、補題1本に集約して SPSE は系として得た（証明の重複を回避）
- TA-DA（スライドの A-STDA）：`Prop.~\ref{prop:tada-props}` に swap stability を追加。
  スライドの「SPSE と同じ拒否連鎖」だけでは不十分で、$c'\notin A_i(e)$（閾値で応募を止められた）
  場合の場合分けが要る。共通加点により $A_i(e)$ が $\T(i)$ を全部含むか全く含まないかなので、
  その場合は $c=o$ に限られ、相手の $o$ での拒否と点数の大小が矛盾する、という形で補完した
- PA-ODR：`Prop.~\ref{prop:paodr-swap}`（留保カテゴリ間の swap stability）。
  スライドの「順位ベクトルだけを改善 ⇒ 基準3の辞書式最小性に矛盾」を証明として整形
- PA-ODR の広義不成立：スライドの反例（$i_1(100,\{t\})$ は $t\succ o$、$i_2(90,\{t\})$ は $o\succ t$）は
  既存の `Example~\ref{ex:paodr-envy}` と数値が同一だったので、同例に「$i_2$ の選好だけ入れ替える」
  段落として追加。交換後も score-feasible であることを確認済み（Def.~\ref{def:nje} の扱いに合わせた）
- Prototype: Table~\ref{tab:prototype} のキャプションに実測を追記
  （狭義は全300件で3機構とも成立、広義は SPSE・TA-DA が全件成立、
  PA-ODR は 99/100・100/100・37/100 で違反。`scripts/check_swap_stability.py`）
- `Table~\ref{tab:comparison}` に2行追加（留保内 swap stability = 3機構とも Yes、
  全カテゴリ = SPSE/TA-DA が Yes、PA-ODR が No）。Introduction の Contribution 1/4/5 と
  Conclusion も更新
- スライド24の「最大マッチング」行は未反映（swap 公平性の追加分ではなく、
  かつ PA-ODR の飽和は Prototype 節に既述）

### 構成・フォーマット

- [x] **Abstract 251語 → 195語**（SCITEPRESS 規定は70〜200語。251語は明確な違反だった）
      旧版は `\abstract{}` 直前に `%` コメントで保存
- [x] **不可能性定理を独立セクションに昇格**
      `\subsection{An Impossibility Driven by Overlap}` → `\section{...}` + `\label{sec:impossibility}`
      理由: Contribution 3 で「This is the pivot of the paper」と自称する結果が SPSE 章の
      一小節に埋もれ、目次上で論文の骨格（3機構 ⇄ それらを分岐させる1つの不可能性）が
      見えなかった。Introduction の Contribution 3 から `Section~\ref{sec:impossibility}` を参照
- [x] `latexmkrc` を platex/pbibtex → pdflatex/bibtex に修正（PRIMA から引き継いだ誤設定）
- [x] Keywords の titlecase 修正（`De-reservation` → `De-Reservation`）

現在の構成:
Introduction → Model → SPSE → **Impossibility** → TA-DA → PA-ODR → Prototype → Conclusion

バックアップ: `main.tex.before_icaart_structure`

### 引用の誤り修正

- [x] **`SoYe22a` のタイトルが誤り**（ワーキングペーパー時代の題名だった）
      `Affirmative Action in India via Vertical and Horizontal Reservations`
      → `Affirmative Action in India via Vertical, Horizontal, and Overlapping Reservations`
      Econometrica 90(3), 1143–1176, doi:10.3982/ECTA17788
- [x] **`SoYe20a`（BC Working Paper 990）は Econometrica 版に吸収され消滅**
      Econometrica 2022 が 2本の WP（"Vertical and Horizontal Reservations" と
      "Affirmative Action with Overlapping Reserves"）を subsume・置換したもの。
      本文2箇所の引用を `SoYe22a` に統合。bib エントリは `% SUPERSEDED` コメント付きで残置
      （他ドラフトが壊れないように）

バックアップ: `references.bib.before_prior_work_check`

### 推奨引用の追加（5件）

| key | 文献 | 挿入箇所 | 目的 |
|---|---|---|---|
| `AyTu26a` | Aygün & Turhan, *Affirmative Action in India with Hierarchical Reservations*, arXiv:2602.09189 (2026) | Relation to the closest prior work | one-to-one counting と **one-to-all** の切り分け |
| `Glit26a` | Glitzner, *Near-Feasible Stable Matchings: Incentives and Optimality*, arXiv:2602.10851 (2026) | Sec. PA-ODR 冒頭 | de-reservation を near-feasibility の一事例として位置づけ |
| `CGH20a` | Chen, Ganian & Hamm, *Stable Matchings with Diversity Constraints: Affirmative Action is beyond NP*, IJCAI 2020, 146–152 | Introduction / MinDeres の open problem | AI側の overlapping types 標準文献。Σ₂ᴾ-complete |
| `CsSu26a` | Csáji & Sun, *Maximally Diverse Stable Matchings*, arXiv:2604.27823 (2026) | MinDeres の open problem | hardness 予想への反証リスクを先回りして遮断 |
| `HuZh25a` | Hu & Zhang, *Verifiable Affirmative Action in Centralized School Admissions*, arXiv:2504.04689 (2025) | Introduction 第2段落 | cutoff 系の最新文献 |

検証済み: 引用28件すべて bib に存在／`\ref` の未定義なし／環境の対応取れている

---

## 残りの査読対策（未着手）

- [ ] **`SoYe22a` との novelty 切り分けを本文に明記する。**
      最も近い先行研究の**タイトルに本稿の中核キーワード "Overlapping" が入っている**。
      現状 "Relation to the closest prior work" には「reserve capacities as given、cutoff-gap なし」
      としか書いておらず、overlapping の扱いがどう違うのかが書かれていない。
      `AyTu26a` については one-to-all との対比を追加済みだが、`SoYe22a` については未対応。
      ※ Sönmez–Yenmez の horizontal reservation 処理が one-to-one か one-to-all かは
        原論文を読んで確認してから書くこと（今回は未確認のため断定を避けた）
- [ ] TA-DA の strategy-proofness（本稿が「最も鋭い open question」と位置づけているもの）に
      ついて、`Glit26a` の incentive 分析が示唆を与えないか確認する
- [ ] CLAUDE.md の分野設定 `{{例: 機械学習 / 材料科学 ...}}` と投稿先が未記入のまま。
      ICAART / matching・mechanism design に書き換える

## 版の照合結果（問題なし）

ディレクトリ内 PDF と arXiv 最新版は一致していた:
2312.14648 v2 / 2305.11758 v2 / 2203.01483 v3 / 2103.05899 v5 / 2310.02660 v3 / 2008.00374 v3

なお `AyTu23a`（How to De-Reserve Reserves, Management Science）は Turhan 氏のページでは
2022年掲載、bib は 69(10) 2023。online-first と巻号確定のずれと判断し **69(10), 2023 のまま**とした。

## 実効カットオフ（定員割れ=0）導入に伴う未処理項目

2026-08-25 に Definition `def:dereserve`（総量保存つき de-reservation）と
Definition `def:effcutoff`（定員割れカテゴリのカットオフは 0）をモデルに追加した。
残る作業:

- [ ] **Prototype に実効カットオフ違反率を追加する。** 現在 Sec.~\ref{sec:experiments} は
  TA-DA の「plain NW 違反」を 54/52/46 件と報告しているが、実効カットオフ違反
  （$|\mu_t|<q^t$ かつ $\tilde e_o(\mu)>\delta$）は同一ではない（前者は後者を含意しない）。
  数値を実測するまで本文に件数を書かないこと。
- [ ] **A-STDA も実効 score-feasibility は満たさない**はず（TA-DA と同じ理由）。
  Prop.~\ref{prop:astda} に一言添えるか、Table~\ref{tab:comparison} の扱いに合わせるか判断する。
- [ ] **分量.** この追加で約 +2,000 字。Full Paper 12 ページ枠に対して既に超過中なので、
  削減候補（TODO 上部の表）と併せて再計算する。
