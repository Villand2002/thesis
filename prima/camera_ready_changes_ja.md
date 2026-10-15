# PRIMA camera-ready 対応メモ

## 全体方針

採択済みなので、大きな主張の差し替えではなく、査読者が共通して気にしていた点を camera-ready で明示的に処理した。特に、PA-ODR の実用上の弱点を隠さず、代替案との比較によって「何を得て何を失うか」を本文と appendix で整理した。

## Reviewer #1 への対応

- Novelty の懸念:
  - Introduction で、score-elevated mechanism が cutoff rule を破ること自体は既知であり、本稿の新規性は overlap による routing 問題と joint-versus-individual fillability obstruction にある、と明示した。
  - Proposition 5 後の remark で Hall-type obstruction として位置づけ、個別 fillability と joint fillability の差が overlap から来ることを説明した。

- Soundness の懸念:
  - Section 4.2 の非最小性の主張を、任意の順序で非最小と読めないように修正した。
  - Table 2 の最後の列を `De-reserved reserve seats` に変更し、categories ではなく seats を数えていることを明確化した。
  - 実験の capacity distribution を明記した。
  - prototype は average-case evidence ではなく sanity check/trade-off check だと弱めて書いた。

- Clarity の指摘:
  - `miniality`, `categor`, `The check is not an evidence` などの誤字・不自然表現を修正した。
  - open cutoff は raw score、reserve cutoff は adjusted score であることを model section で補足した。

- Significance の懸念:
  - Reviewer が最も強く勧めていた idle-category alternative との比較を追加した。
  - 本文の conclusion では要点だけ述べ、詳細な表と説明は Appendix に移した。

## Reviewer #2 への対応

- Contribution が standard DA に近いという懸念:
  - SPSE は DA 的性質を持つが score-feasibility を保証しない、という位置づけを明確にした。
  - 本稿の中心を SPSE そのものではなく、overlap が引き起こす routing/fillability obstruction と score-feasible de-reservation の trade-off に寄せた。

- Proposition 5 が Hall condition に見えるという懸念:
  - Hall-type failure であることを隠さず明示し、むしろ overlap によって singleton condition と subset condition が乖離する点として説明した。

- PA-ODR の限界:
  - Order dependence、non-minimality、strategy-proofness/no-justified-envy の喪失を本文で明示した。
  - MinDeres は bounded number of categories で polynomial とし、unbounded case は open problem として整理した。

## Reviewer #3 への対応

- PA-ODR が de-reserve しすぎる可能性:
  - Idle-ODR comparator を実装し、Appendix の prototype table に追加した。
  - 結果として、Idle-ODR は reserve seats を全て保持し score-feasible だが、matched students が大きく減ることを示した。
  - これにより PA-ODR は「score-feasibility と coverage を維持する代わりに reserve seats を失う」機構である、と trade-off を明確化した。

- Category order の正当化:
  - PA-ODR の order dependence を欠点として明示し、Example で異なる order が異なる de-reservation を生むことを示した。
  - Order は mechanism specification の一部であり、policy choice が必要だと読めるようにした。

- 実験が限定的という懸念:
  - Appendix に prototype check を移し、過度な empirical claim にならないようにした。
  - 同時に、Reviewer が求めた idle-category comparison は追加した。

## 今回追加した実装

- `algorithms/admissions.py`
  - `idle_odr(problem)` を追加。
  - PA-ODR と同じ open-first cutoff と reserve-side preference-aware matching を使う。
  - ただし reserve capacity を open に移さず、埋まらない reserve seats は空席のまま残す。

- `scripts/paper_table.py`
  - PRIMA LNCS の prototype table 再現用に整理。
  - `SPSE`, `Idle-ODR`, `PA-ODR` のみを出力するようにした。

- `tests/test_admissions.py`
  - Idle-ODR が score-feasible なまま unfillable reserve capacity を idle にする例を追加。

## 主要な数値

| family | mechanism | score-feasible | matched | de-reserved reserve seats |
| --- | --- | ---: | ---: | ---: |
| 200 students, 6 reserve categories | SPSE | 54/100 | 62.97 | 0.00 |
| 200 students, 6 reserve categories | Idle-ODR | 100/100 | 44.57 | 0.00 |
| 200 students, 6 reserve categories | PA-ODR | 100/100 | 62.97 | 18.57 |
| 500 students, 8 reserve categories | SPSE | 52/100 | 187.33 | 0.00 |
| 500 students, 8 reserve categories | Idle-ODR | 100/100 | 114.10 | 0.00 |
| 500 students, 8 reserve categories | PA-ODR | 100/100 | 187.33 | 73.24 |

## 使える一文

The camera-ready version clarifies that the idle-category alternative preserves reserve seats and score-feasibility, but at a substantial coverage cost in the prototype instances. PA-ODR instead preserves the number of admitted students relative to SPSE while enforcing score-feasibility, at the cost of de-reserving reserve seats.
