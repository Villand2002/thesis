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

## 【最優先】分量が上限を超過（swap stability 追加後）

現状（2026-08-18, swap stability 反映後）:

- 本文の非空白文字数（同じ機械除去スクリプトによる概算）: **約53,100 / 50,000字**
  → **約3,100字の超過**。swap stability の追加が正味 +3,100字（総量 +4,300字、既存圧縮 −1,200字）
- 推定ページ数: 13〜13.5ページ vs Full Paper 枠 12ページ

### 実施済みの削減（本セッション）

- [x] `Remark~\ref{rem:capbound}`（容量上限）を Prop.~\ref{prop:paodr-basic} の証明中の脚注に降格
- [x] `Proposition[MinDeres]` を Remark に圧縮（主張・計算量の式・open question は保持）
- [x] Prototype 第4読み（δ 感度）を1文に圧縮
- [x] SPSE 戦略耐性の証明・`rem:hall`・`sec:trigger`・δ/k 議論を純圧縮

### 残る削減候補（**著者判断**。いずれも主張を1つ落とす）

| 候補 | 字数 | 失うもの |
|---|---|---|
| `\subsection{Order Dependence and Non-Minimality}` 全体（Ex.~order + 非最小性の議論 + MinDeres Remark） | 約3,170字 | PA-ODR の順序依存＝非最小性という限界の明示。Introduction からの `Example~\ref{ex:order}` 参照も要修正 |
| Prototype の第2ファミリ（|I|=500）を落とす | 約900字 | スケール確認。第3ファミリ（capacity-rich）が論旨の核なので残す |
| `Remark~\ref{sec:trigger}`（何が de-reservation を起こすか） | 1,245字 | PA-ODR と TA-DA の対比の要。削ると Prototype 第3読みの伏線が消える |
| `Remark~\ref{rem:hall}`（Hall 条件による障害の同定） | 704字 | Conclusion が参照しているので同時修正が必要 |

1つ目を採ると1回で解消する。**推奨は1つ目**（PA-ODR の非最小性は Conclusion の open question に1文で残せる）。

- [ ] 投稿パッケージから `Example.tex` / `Example.pdf`（テンプレート付属の見本）を除外する
- [ ] LaTeX 処理系のある環境でコンパイルし、実ページ数と実文字数を確認する
      （このリポジトリの作業環境には latexmk/pdflatex が入っていない）

---

## 完了済み（2026-08-18）

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
