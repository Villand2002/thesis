from __future__ import annotations

from dataclasses import dataclass
from math import inf
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from .fast_matching import pref_lex_max_matching


OPEN_CATEGORY = "o"


@dataclass(frozen=True)
class Student:
    student_id: str
    raw_score: float
    eligible_categories: Tuple[str, ...]
    preferences: Tuple[str, ...]

    def can_apply(self, category: str) -> bool:
        return category == OPEN_CATEGORY or category in self.eligible_categories


@dataclass(frozen=True)
class AdmissionProblem:
    students: Tuple[Student, ...]
    capacities: Dict[str, int]
    bonuses: Dict[str, float]
    delta: float

    @property
    def categories(self) -> Tuple[str, ...]:
        reserved = tuple(sorted(c for c in self.capacities if c != OPEN_CATEGORY))
        return (OPEN_CATEGORY,) + reserved

    @property
    def reserved_categories(self) -> Tuple[str, ...]:
        return tuple(c for c in self.categories if c != OPEN_CATEGORY)

    def student_map(self) -> Dict[str, Student]:
        return {student.student_id: student for student in self.students}


@dataclass
class AdmissionResult:
    assignments: Dict[str, Tuple[str, ...]]
    effective_capacities: Dict[str, int]
    metadata: Dict[str, object]

    def matched_students(self) -> Tuple[str, ...]:
        seen: List[str] = []
        for category in self.assignments:
            seen.extend(self.assignments[category])
        return tuple(seen)

    def category_of(self, student_id: str) -> Optional[str]:
        for category, assignees in self.assignments.items():
            if student_id in assignees:
                return category
        return None


def adjusted_score(problem: AdmissionProblem, student: Student, category: str) -> float:
    if category == OPEN_CATEGORY:
        return student.raw_score
    return student.raw_score + (problem.bonuses.get(category, 0.0) if category in student.eligible_categories else 0.0)


def category_priority_key(problem: AdmissionProblem, student: Student, category: str) -> Tuple[float, float, str]:
    return (adjusted_score(problem, student, category), student.raw_score, student.student_id)


def sorted_students_by_open_merit(problem: AdmissionProblem, student_ids: Iterable[str]) -> List[str]:
    student_map = problem.student_map()
    return sorted(
        student_ids,
        key=lambda sid: (student_map[sid].raw_score, sid),
        reverse=True,
    )


def build_result(
    problem: AdmissionProblem,
    assignments: Dict[str, Sequence[str]],
    effective_capacities: Optional[Dict[str, int]] = None,
    metadata: Optional[Dict[str, object]] = None,
) -> AdmissionResult:
    normalized = {category: tuple(assignments.get(category, ())) for category in problem.categories}
    return AdmissionResult(
        assignments=normalized,
        effective_capacities=dict(problem.capacities if effective_capacities is None else effective_capacities),
        metadata={} if metadata is None else metadata,
    )


def open_cutoff(problem: AdmissionProblem, result: AdmissionResult) -> float:
    open_assignees = result.assignments[OPEN_CATEGORY]
    if not open_assignees:
        return inf
    student_map = problem.student_map()
    return min(student_map[sid].raw_score for sid in open_assignees)


def reserved_cutoff(problem: AdmissionProblem, result: AdmissionResult, category: str) -> float:
    assignees = result.assignments[category]
    if not assignees:
        return inf
    student_map = problem.student_map()
    return min(adjusted_score(problem, student_map[sid], category) for sid in assignees)


def is_feasible(problem: AdmissionProblem, result: AdmissionResult, capacities: Optional[Dict[str, int]] = None) -> bool:
    caps = problem.capacities if capacities is None else capacities
    seen = set()
    for category in problem.categories:
        assignees = result.assignments.get(category, ())
        if len(assignees) > caps[category]:
            return False
        for sid in assignees:
            if sid in seen:
                return False
            seen.add(sid)
    return True


def is_score_feasible(problem: AdmissionProblem, result: AdmissionResult, capacities: Optional[Dict[str, int]] = None) -> bool:
    caps = problem.capacities if capacities is None else capacities
    if len(result.assignments[OPEN_CATEGORY]) < caps[OPEN_CATEGORY]:
        return True
    e_open = open_cutoff(problem, result)
    for category in problem.reserved_categories:
        assignees = result.assignments[category]
        if not assignees:
            continue
        if e_open - reserved_cutoff(problem, result, category) > problem.delta:
            return False
    return True


def within_category_fairness(problem: AdmissionProblem, result: AdmissionResult) -> bool:
    student_map = problem.student_map()
    matched = set(result.matched_students())
    for category in problem.reserved_categories:
        assignees = result.assignments[category]
        for sid_j in assignees:
            student_j = student_map[sid_j]
            for sid_i, student_i in student_map.items():
                if sid_i in matched:
                    continue
                if category not in student_i.eligible_categories or category not in student_j.eligible_categories:
                    continue
                if student_i.raw_score > student_j.raw_score:
                    return False
    return True


def shared_category_constrained_replacement_fairness(problem: AdmissionProblem, result: AdmissionResult) -> bool:
    student_map = problem.student_map()
    matched = set(result.matched_students())
    for sid_i, student_i in student_map.items():
        if sid_i in matched:
            continue
        for category in problem.categories:
            if not student_i.can_apply(category):
                continue
            for sid_j in result.assignments[category]:
                student_j = student_map[sid_j]
                if not student_j.can_apply(category):
                    continue
                if adjusted_score(problem, student_i, category) <= adjusted_score(problem, student_j, category):
                    continue
                new_assignments = {c: list(result.assignments[c]) for c in problem.categories}
                new_assignments[category].remove(sid_j)
                new_assignments[category].append(sid_i)
                candidate = build_result(problem, new_assignments, result.effective_capacities, result.metadata)
                if is_feasible(problem, candidate, result.effective_capacities) and is_score_feasible(
                    problem, candidate, result.effective_capacities
                ):
                    return False
    return True


def filtered_preferences(student: Student, allowed_categories: Iterable[str]) -> Tuple[str, ...]:
    allowed = set(allowed_categories)
    ordered = [category for category in student.preferences if category in allowed]
    return tuple(ordered)


def student_proposing_da(
    problem: AdmissionProblem,
    application_sets: Dict[str, Iterable[str]],
    capacities: Optional[Dict[str, int]] = None,
) -> AdmissionResult:
    caps = problem.capacities if capacities is None else capacities
    student_map = problem.student_map()
    held: Dict[str, List[str]] = {category: [] for category in problem.categories}
    queues: Dict[str, List[str]] = {}
    next_index: Dict[str, int] = {}

    for student in problem.students:
        options = filtered_preferences(student, application_sets.get(student.student_id, ()))
        queues[student.student_id] = list(options)
        next_index[student.student_id] = 0

    free = [student.student_id for student in problem.students]
    while free:
        sid = free.pop(0)
        prefs = queues[sid]
        idx = next_index[sid]
        if idx >= len(prefs):
            continue
        category = prefs[idx]
        next_index[sid] += 1
        held[category].append(sid)

        ranked = sorted(
            held[category],
            key=lambda candidate_sid: category_priority_key(problem, student_map[candidate_sid], category),
            reverse=True,
        )
        kept = ranked[: caps[category]]
        rejected = ranked[caps[category] :]
        held[category] = kept
        for rejected_sid in rejected:
            free.append(rejected_sid)

    return build_result(problem, held, capacities, {"mechanism": "da"})


def spse(problem: AdmissionProblem) -> AdmissionResult:
    application_sets = {
        student.student_id: (OPEN_CATEGORY,) + tuple(student.eligible_categories)
        for student in problem.students
    }
    return student_proposing_da(problem, application_sets)


def _enumerate_reserved_matchings(
    problem: AdmissionProblem,
    available_students: Sequence[str],
    capacities: Dict[str, int],
    threshold: float,
) -> List[Dict[str, Tuple[str, ...]]]:
    student_map = problem.student_map()
    categories = list(problem.reserved_categories)
    available = list(available_students)
    results: List[Dict[str, Tuple[str, ...]]] = []

    def can_assign(sid: str, category: str) -> bool:
        student = student_map[sid]
        return category in student.eligible_categories and adjusted_score(problem, student, category) >= threshold - problem.delta

    def backtrack(index: int, current: Dict[str, List[str]]) -> None:
        if index == len(available):
            results.append({category: tuple(current[category]) for category in categories})
            return
        sid = available[index]
        backtrack(index + 1, current)
        for category in categories:
            if len(current[category]) >= capacities[category]:
                continue
            if not can_assign(sid, category):
                continue
            current[category].append(sid)
            backtrack(index + 1, current)
            current[category].pop()

    backtrack(0, {category: [] for category in categories})
    return results


def _pref_rank(student: Student, category: str) -> int:
    return student.preferences.index(category) + 1


def _matching_objective(problem: AdmissionProblem, matching: Dict[str, Tuple[str, ...]]) -> Tuple:
    student_map = problem.student_map()
    assignments: List[Tuple[str, str]] = []
    for category, assignees in matching.items():
        for sid in assignees:
            assignments.append((sid, category))
    cardinality = len(assignments)
    elevated = sorted(
        (adjusted_score(problem, student_map[sid], category) for sid, category in assignments),
        reverse=True,
    )
    ranked_assignments = sorted(
        assignments,
        key=lambda item: (
            adjusted_score(problem, student_map[item[0]], item[1]),
            student_map[item[0]].raw_score,
            item[0],
        ),
        reverse=True,
    )
    preference_vector = tuple(_pref_rank(student_map[sid], category) for sid, category in ranked_assignments)
    elevated_tuple = tuple(elevated)
    neg_pref = tuple(-value for value in preference_vector)
    return cardinality, elevated_tuple, neg_pref


def reference_reserved_matching(
    problem: AdmissionProblem,
    available_students: Sequence[str],
    capacities: Dict[str, int],
    threshold: float,
) -> Dict[str, Tuple[str, ...]]:
    """Exponential reference implementation, kept to validate the fast path.

    Enumerates every capacity-feasible reserve assignment. Criteria 1 and 2 agree
    with :func:`_best_reserved_matching`; the tie-breaking below them differs, so
    only the admitted set is comparable.
    """
    candidates = _enumerate_reserved_matchings(problem, available_students, capacities, threshold)
    if not candidates:
        return {category: tuple() for category in problem.reserved_categories}
    return max(candidates, key=lambda candidate: _matching_objective(problem, candidate))


def _feasibility_graph(
    problem: AdmissionProblem,
    available_students: Sequence[str],
    threshold: float,
) -> Tuple[List[str], Dict[str, List[str]], Dict[Tuple[str, str], int], Dict[Tuple[str, str], int]]:
    """G(e): admissible pairs, students ordered by decreasing elevated score."""
    student_map = problem.student_map()
    categories = list(problem.reserved_categories)
    adj: Dict[str, List[str]] = {}
    for sid in available_students:
        student = student_map[sid]
        admissible = [
            category
            for category in categories
            if category in student.eligible_categories
            and adjusted_score(problem, student, category) >= threshold - problem.delta
        ]
        if admissible:
            adj[sid] = admissible

    def elevated(sid: str) -> float:
        student = student_map[sid]
        return max(adjusted_score(problem, student, category) for category in adj[sid])

    ordered = sorted(adj, key=lambda sid: (elevated(sid), student_map[sid].raw_score, sid), reverse=True)

    rank: Dict[Tuple[str, str], int] = {}
    pair_index: Dict[Tuple[str, str], int] = {}
    for index, (sid, category) in enumerate(
        (sid, category) for sid in sorted(adj) for category in sorted(adj[sid])
    ):
        rank[(sid, category)] = student_map[sid].preferences.index(category) + 1
        pair_index[(sid, category)] = index
    return ordered, adj, rank, pair_index


def _best_reserved_matching(
    problem: AdmissionProblem,
    available_students: Sequence[str],
    capacities: Dict[str, int],
    threshold: float,
) -> Dict[str, Tuple[str, ...]]:
    empty = {category: tuple() for category in problem.reserved_categories}
    ordered, adj, rank, pair_index = _feasibility_graph(problem, available_students, threshold)
    if not ordered:
        return empty
    caps = {category: capacities[category] for category in problem.reserved_categories}
    matching = pref_lex_max_matching(ordered, adj, caps, rank, pair_index)
    return {category: matching.get(category, ()) for category in problem.reserved_categories}


def pa_odr(problem: AdmissionProblem) -> AdmissionResult:
    capacities = dict(problem.capacities)
    student_map = problem.student_map()
    history: List[Dict[str, object]] = []

    while True:
        ordered_students = sorted_students_by_open_merit(problem, student_map.keys())
        open_assignees = ordered_students[: min(capacities[OPEN_CATEGORY], len(ordered_students))]
        threshold = min((student_map[sid].raw_score for sid in open_assignees), default=inf)
        remaining = [sid for sid in ordered_students if sid not in set(open_assignees)]
        reserved_matching = _best_reserved_matching(problem, remaining, capacities, threshold)

        history.append(
            {
                "effective_capacities": dict(capacities),
                "open_cutoff": threshold,
                "open_assignees": tuple(open_assignees),
                "reserved_matching": reserved_matching,
            }
        )

        underfilled = [category for category in problem.reserved_categories if len(reserved_matching[category]) < capacities[category]]
        if not underfilled:
            assignments = {OPEN_CATEGORY: tuple(open_assignees)}
            assignments.update(reserved_matching)
            return build_result(problem, assignments, capacities, {"mechanism": "pa_odr", "history": history})

        category = underfilled[0]
        capacities[category] -= 1
        capacities[OPEN_CATEGORY] += 1


def threshold_adjusting_da(problem: AdmissionProblem) -> AdmissionResult:
    thresholds = sorted({student.raw_score for student in problem.students}, reverse=True)
    scored_results: List[Tuple[int, float, AdmissionResult]] = []

    for threshold in thresholds:
        application_sets = {}
        for student in problem.students:
            allowed = [OPEN_CATEGORY]
            for category in student.eligible_categories:
                if adjusted_score(problem, student, category) >= threshold - problem.delta:
                    allowed.append(category)
            application_sets[student.student_id] = tuple(allowed)
        result = student_proposing_da(problem, application_sets)
        if is_score_feasible(problem, result):
            scored_results.append((len(result.matched_students()), threshold, result))

    if not scored_results:
        raise ValueError("No score-feasible threshold found.")

    _, threshold, chosen = max(scored_results, key=lambda item: (item[0], item[1]))
    chosen.metadata.update({"mechanism": "threshold_adjusting_da", "threshold": threshold})
    return chosen
