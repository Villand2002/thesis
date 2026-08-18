"""Empirical check of the swap-stability claims (Lemma 3, Props. 5, 9 of main.tex).

Reproduces the three prototype families of Section "Prototype" and counts blocking
swaps for each mechanism, both within reserves and across all categories.
"""
from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from algorithms import blocking_swaps, pa_odr, spse, threshold_adjusting_da
from scripts.benchmark_admissions import make_problem

FAMILIES = {
    1: dict(students=200, reserved_categories=6, open_capacity=30, reserved_capacity=15),
    2: dict(students=500, reserved_categories=8, open_capacity=70, reserved_capacity=35),
    3: dict(students=60, reserved_categories=6, open_capacity=30, reserved_capacity=15),
}

MECHANISMS = (("SPSE", spse), ("TA-DA", threshold_adjusting_da), ("PA-ODR", pa_odr))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", type=int, choices=sorted(FAMILIES), action="append")
    parser.add_argument("--runs", type=int, default=100)
    parser.add_argument("--seed", type=int, default=100)
    args = parser.parse_args()

    for family in args.family or sorted(FAMILIES):
        rng = random.Random(args.seed)
        problems = [
            make_problem(
                **FAMILIES[family],
                overlap_probability=0.45,
                bonus=15.0,
                delta=8.0,
                messy=True,
                rng=rng,
                common_bonus=True,
            )
            for _ in range(args.runs)
        ]
        print(f"family {family}: {FAMILIES[family]}  ({args.runs} instances, seed {args.seed})")
        for name, mechanism in MECHANISMS:
            stable_reserves = stable_all = 0
            swaps_all = 0
            for problem in problems:
                result = mechanism(problem)
                within = blocking_swaps(problem, result, reserves_only=True)
                across = blocking_swaps(problem, result, reserves_only=False)
                stable_reserves += not within
                stable_all += not across
                swaps_all += len(across)
            print(
                f"  {name:<7} swap stable within reserves: {stable_reserves:>3}/{args.runs}"
                f"   all categories: {stable_all:>3}/{args.runs}"
                f"   (total blocking swaps: {swaps_all})"
            )


if __name__ == "__main__":
    main()
