from __future__ import annotations

import argparse
import random
import statistics
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Sequence

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from algorithms import (
    AdmissionProblem,
    Student,
    idle_odr,
    is_feasible,
    is_score_feasible,
    pa_odr,
    spse,
    threshold_adjusting_da,
    within_category_fairness,
)
from algorithms.admissions import OPEN_CATEGORY


Algorithm = Callable[[AdmissionProblem], object]


@dataclass(frozen=True)
class BenchmarkRow:
    algorithm: str
    runs: int
    mean_ms: float
    median_ms: float
    min_ms: float
    max_ms: float
    feasible: int
    score_feasible: int
    within_fair: int
    matched_mean: float
    matched_min: int
    matched_max: int
    de_reserved_mean: float
    de_reserved_max: int
    final_open_capacity_mean: float
    final_reserved_capacity_mean: float


def make_problem(
    *,
    students: int,
    reserved_categories: int,
    open_capacity: int,
    reserved_capacity: int,
    overlap_probability: float,
    bonus: float,
    delta: float,
    messy: bool,
    rng: random.Random,
    common_bonus: bool = False,
) -> AdmissionProblem:
    categories = tuple(f"t{i + 1}" for i in range(reserved_categories))
    generated: List[Student] = []

    for index in range(students):
        eligible = [category for category in categories if rng.random() < overlap_probability]
        if not eligible:
            eligible = [rng.choice(categories)]
        rng.shuffle(eligible)
        preferences = list(eligible + [OPEN_CATEGORY])
        if messy:
            rng.shuffle(preferences)
        raw_score = rng.uniform(0, 100) if messy else float(students * 10 - index * 3 + rng.random())
        generated.append(
            Student(
                student_id=f"s{index + 1}",
                raw_score=raw_score,
                eligible_categories=tuple(eligible),
                preferences=tuple(preferences),
            )
        )

    if messy:
        capacities = {OPEN_CATEGORY: rng.randint(1, open_capacity)}
        capacities.update({category: rng.randint(1, reserved_capacity) for category in categories})
        if common_bonus:
            # One bonus shared by every category, as the common-bonus model assumes.
            shared = rng.uniform(0, bonus)
            bonuses = {category: shared for category in categories}
        else:
            bonuses = {category: rng.uniform(0, bonus) for category in categories}
    else:
        capacities = {OPEN_CATEGORY: open_capacity}
        capacities.update({category: reserved_capacity for category in categories})
        bonuses = {category: bonus for category in categories}
    return AdmissionProblem(
        students=tuple(generated),
        capacities=capacities,
        bonuses=bonuses,
        delta=delta,
    )


def time_algorithm(algorithm: Algorithm, problem: AdmissionProblem) -> tuple[float, object | None, Exception | None]:
    start = time.perf_counter()
    try:
        result = algorithm(problem)
    except Exception as exc:  # pragma: no cover - reported in benchmark output
        elapsed = time.perf_counter() - start
        return elapsed, None, exc
    elapsed = time.perf_counter() - start
    return elapsed, result, None


def summarize(
    name: str,
    algorithm: Algorithm,
    problems: Sequence[AdmissionProblem],
) -> BenchmarkRow:
    timings: List[float] = []
    feasible = 0
    score_feasible = 0
    within_fair = 0
    matched_counts: List[int] = []
    de_reserved_counts: List[int] = []
    final_open_capacities: List[int] = []
    final_reserved_capacities: List[int] = []

    for problem in problems:
        elapsed, result, error = time_algorithm(algorithm, problem)
        timings.append(elapsed * 1000)
        if error is not None or result is None:
            continue
        matched_counts.append(len(result.matched_students()))
        de_reserved_counts.append(
            sum(
                problem.capacities[category] - result.effective_capacities[category]
                for category in problem.reserved_categories
            )
        )
        final_open_capacities.append(result.effective_capacities[OPEN_CATEGORY])
        final_reserved_capacities.append(
            sum(result.effective_capacities[category] for category in problem.reserved_categories)
        )
        if is_feasible(problem, result, result.effective_capacities):
            feasible += 1
        if is_score_feasible(problem, result, result.effective_capacities):
            score_feasible += 1
        if within_category_fairness(problem, result):
            within_fair += 1

    return BenchmarkRow(
        algorithm=name,
        runs=len(problems),
        mean_ms=statistics.mean(timings),
        median_ms=statistics.median(timings),
        min_ms=min(timings),
        max_ms=max(timings),
        feasible=feasible,
        score_feasible=score_feasible,
        within_fair=within_fair,
        matched_mean=statistics.mean(matched_counts) if matched_counts else 0.0,
        matched_min=min(matched_counts) if matched_counts else 0,
        matched_max=max(matched_counts) if matched_counts else 0,
        de_reserved_mean=statistics.mean(de_reserved_counts) if de_reserved_counts else 0.0,
        de_reserved_max=max(de_reserved_counts) if de_reserved_counts else 0,
        final_open_capacity_mean=statistics.mean(final_open_capacities) if final_open_capacities else 0.0,
        final_reserved_capacity_mean=statistics.mean(final_reserved_capacities) if final_reserved_capacities else 0.0,
    )


def print_rows(rows: Iterable[BenchmarkRow]) -> None:
    header = (
        "algorithm",
        "runs",
        "mean_ms",
        "median_ms",
        "min_ms",
        "max_ms",
        "feasible",
        "score_feasible",
        "within_fair",
        "matched_mean",
        "matched_min",
        "matched_max",
        "de_reserved_mean",
        "de_reserved_max",
        "final_open_capacity_mean",
        "final_reserved_capacity_mean",
    )
    print(",".join(header))
    for row in rows:
        print(
            ",".join(
                (
                    row.algorithm,
                    str(row.runs),
                    f"{row.mean_ms:.3f}",
                    f"{row.median_ms:.3f}",
                    f"{row.min_ms:.3f}",
                    f"{row.max_ms:.3f}",
                    str(row.feasible),
                    str(row.score_feasible),
                    str(row.within_fair),
                    f"{row.matched_mean:.3f}",
                    str(row.matched_min),
                    str(row.matched_max),
                    f"{row.de_reserved_mean:.3f}",
                    str(row.de_reserved_max),
                    f"{row.final_open_capacity_mean:.3f}",
                    f"{row.final_reserved_capacity_mean:.3f}",
                )
            )
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark admissions algorithms on random instances.")
    parser.add_argument("--students", type=int, default=10)
    parser.add_argument("--reserved-categories", type=int, default=3)
    parser.add_argument("--open-capacity", type=int, default=3)
    parser.add_argument("--reserved-capacity", type=int, default=2)
    parser.add_argument("--overlap-probability", type=float, default=0.5)
    parser.add_argument("--bonus", type=float, default=5.0)
    parser.add_argument("--delta", type=float, default=10.0)
    parser.add_argument("--runs", type=int, default=20)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--messy",
        action="store_true",
        help="Randomize raw scores, preference orders, capacities up to the given maxima, and bonuses up to --bonus.",
    )
    parser.add_argument(
        "--common-bonus",
        action="store_true",
        help="With --messy, draw a single bonus per instance and share it across categories (the common-bonus model).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)
    problems = [
        make_problem(
            students=args.students,
            reserved_categories=args.reserved_categories,
            open_capacity=args.open_capacity,
            reserved_capacity=args.reserved_capacity,
            overlap_probability=args.overlap_probability,
            bonus=args.bonus,
            delta=args.delta,
            messy=args.messy,
            rng=rng,
            common_bonus=args.common_bonus,
        )
        for _ in range(args.runs)
    ]

    rows = [
        summarize("spse", spse, problems),
        summarize("idle_odr", idle_odr, problems),
        summarize("pa_odr", pa_odr, problems),
        summarize("threshold_adjusting_da", threshold_adjusting_da, problems),
    ]
    print_rows(rows)


if __name__ == "__main__":
    main()


#   python3 scripts/benchmark_admissions.py \
#     --students 30 \
#     --reserved-categories 10 \
#     --open-capacity 20 \
#     --reserved-capacity 10 \
#     --runs 3 \
#     --seed 100
