"""Regenerate the prototype table of the ICAART paper.

Reproduces the three instance families of Section "Prototype" (seed 100) and
reports every property the paper claims, including the across-category
fairness notion introduced after the 2026-08-26 meeting.

    python3 scripts/paper_table.py
"""

from __future__ import annotations

import random
import statistics
import sys
import time
from pathlib import Path
from typing import Callable, Dict, List, Sequence

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from algorithms.admissions import (
    OPEN_CATEGORY,
    AdmissionProblem,
    across_category_fairness,
    adaptive_score_threshold_da,
    effectively_score_feasible,
    is_feasible,
    no_justified_envy,
    non_wasteful,
    non_wasteful_plain,
    pa_odr,
    realized_score_feasible,
    spse,
    swap_stability,
    threshold_adjusting_da,
    within_category_fairness,
    within_category_fairness_strong,
)
from scripts.benchmark_admissions import make_problem

FAMILIES = (
    ("|I|=200, |T|=6", dict(students=200, reserved_categories=6, open_capacity=30, reserved_capacity=15)),
    ("|I|=500, |T|=8", dict(students=500, reserved_categories=8, open_capacity=70, reserved_capacity=35)),
    ("|I|=60, |T|=6", dict(students=60, reserved_categories=6, open_capacity=30, reserved_capacity=15)),
)

MECHANISMS: Sequence[tuple[str, Callable]] = (
    ("SPSE", spse),
    ("TA-DA", threshold_adjusting_da),
    ("A-STDA", adaptive_score_threshold_da),
    ("PA-ODR", pa_odr),
)

CHECKS = (
    ("feas", lambda p, r: is_feasible(p, r, r.effective_capacities)),
    ("sf", realized_score_feasible),
    ("sf-eff", effectively_score_feasible),
    ("nw", non_wasteful),
    ("nw-plain", non_wasteful_plain),
    ("within-unm", within_category_fairness),
    ("within", within_category_fairness_strong),
    ("across", across_category_fairness),
    ("nje", no_justified_envy),
    ("swap", lambda p, r: swap_stability(p, r, reserves_only=False)),
    ("swap-res", lambda p, r: swap_stability(p, r, reserves_only=True)),
)


def build_family(spec: Dict[str, int], *, delta: float, overlap: float, runs: int, seed: int):
    rng = random.Random(seed)
    return [
        make_problem(
            overlap_probability=overlap,
            bonus=15.0,
            delta=delta,
            messy=True,
            rng=rng,
            common_bonus=True,
            **spec,
        )
        for _ in range(runs)
    ]


def run(delta: float = 8.0, overlap: float = 0.45, runs: int = 100, seed: int = 100) -> None:
    header = ["family", "mechanism", "med_ms"] + [name for name, _ in CHECKS] + ["matched", "dereserved", "%res"]
    print(",".join(header))
    for family_name, spec in FAMILIES:
        problems = build_family(spec, delta=delta, overlap=overlap, runs=runs, seed=seed)
        reserve_seats = statistics.mean(
            sum(p.capacities[c] for c in p.reserved_categories) for p in problems
        )
        for mech_name, mechanism in MECHANISMS:
            timings: List[float] = []
            counts = {name: 0 for name, _ in CHECKS}
            matched: List[int] = []
            dereserved: List[int] = []
            for problem in problems:
                start = time.perf_counter()
                result = mechanism(problem)
                timings.append((time.perf_counter() - start) * 1000)
                matched.append(len(result.matched_students()))
                dereserved.append(
                    sum(
                        problem.capacities[c] - result.effective_capacities[c]
                        for c in problem.reserved_categories
                    )
                )
                for name, check in CHECKS:
                    if check(problem, result):
                        counts[name] += 1
            row = [
                f"{family_name} (res={reserve_seats:.2f})",
                mech_name,
                f"{statistics.median(timings):.2f}",
            ]
            row += [str(counts[name]) for name, _ in CHECKS]
            row += [
                f"{statistics.mean(matched):.2f}",
                f"{statistics.mean(dereserved):.2f}",
                f"{100 * statistics.mean(dereserved) / reserve_seats:.0f}",
            ]
            print(",".join(row))


if __name__ == "__main__":
    run()
