"""Property checks for A-STDA (Section "An Adaptive Variant" of main.tex).

score_feasible() and non_wasteful() implement Definitions 3 and 4 of the paper
directly; note that algorithms.admissions.is_score_feasible() short-circuits to
True whenever the open category is non-empty but underfilled, which Definition 3
does not do.
"""
import random, sys
from math import inf
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parents[1]))
from algorithms.admissions import (AdmissionProblem, Student, OPEN_CATEGORY, adjusted_score,
    adaptive_score_threshold_da, threshold_adjusting_da, spse, pa_odr, build_result,
    open_cutoff, reserved_cutoff, within_category_fairness, blocking_swaps)
from scripts.benchmark_admissions import make_problem

def score_feasible(problem, result, caps=None):
    eo = open_cutoff(problem, result)          # inf if empty
    if not result.assignments[OPEN_CATEGORY]:
        return True
    for t in problem.reserved_categories:
        if not result.assignments[t]:
            continue
        if eo - reserved_cutoff(problem, result, t) > problem.delta + 1e-9:
            return False
    return True

def non_wasteful(problem, result, caps=None):
    """Definition: no unmatched i and c in V_i whose addition is feasible AND score-feasible."""
    caps = caps or result.effective_capacities
    matched = set(result.matched_students())
    for st in problem.students:
        if st.student_id in matched:
            continue
        for c in problem.categories:
            if not st.can_apply(c):
                continue
            if len(result.assignments[c]) >= caps[c]:
                continue
            new = {k: list(v) for k, v in result.assignments.items()}
            new[c].append(st.student_id)
            cand = build_result(problem, new, caps, {})
            if score_feasible(problem, cand):
                return False
    return True

def run(n_inst, students, cats, qo, qt, seed, delta=8.0, bonus=15.0, overlap=0.45):
    rng = random.Random(seed)
    probs = [make_problem(students=students, reserved_categories=cats, open_capacity=qo,
                          reserved_capacity=qt, overlap_probability=overlap, bonus=bonus,
                          delta=delta, messy=True, rng=rng, common_bonus=True) for _ in range(n_inst)]
    stats = dict(fixed_point_eq=0, sf=0, wcf=0, nw=0, swap=0, swap_res=0, iters=[], matched=[],
                 matched_tada=[], same_as_tada=0, tada_nw=0)
    for p in probs:
        r = adaptive_score_threshold_da(p)
        tau = r.metadata['threshold']
        eo = open_cutoff(p, r)
        if not r.assignments[OPEN_CATEGORY]:
            eo = -inf
        stats['fixed_point_eq'] += (eo == tau)
        stats['sf'] += score_feasible(p, r)
        stats['wcf'] += within_category_fairness(p, r)
        stats['nw'] += non_wasteful(p, r, p.capacities)
        stats['swap'] += not blocking_swaps(p, r)
        stats['swap_res'] += not blocking_swaps(p, r, reserves_only=True)
        stats['iters'].append(len(r.metadata['history']))
        stats['matched'].append(len(r.matched_students()))
        t = threshold_adjusting_da(p)
        stats['matched_tada'].append(len(t.matched_students()))
        stats['same_as_tada'] += (r.assignments == t.assignments)
        stats['tada_nw'] += non_wasteful(p, t, p.capacities)
    n = len(probs)
    print(f"n={n} |I|={students} |T|={cats} seed={seed}")
    for k in ('fixed_point_eq','sf','wcf','nw','swap','swap_res','same_as_tada','tada_nw'):
        print(f"   {k:<15} {stats[k]}/{n}")
    print(f"   iterations   max={max(stats['iters'])} mean={sum(stats['iters'])/n:.2f}")
    print(f"   matched      A-STDA mean={sum(stats['matched'])/n:.2f}  TA-DA mean={sum(stats['matched_tada'])/n:.2f}")

if __name__ == '__main__':
    run(200, 20, 4, 6, 3, seed=1)
    run(100, 60, 6, 30, 15, seed=100)
    run(50, 200, 6, 30, 15, seed=100)
