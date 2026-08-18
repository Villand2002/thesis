import unittest

from algorithms.admissions import (
    AdmissionProblem,
    OPEN_CATEGORY,
    Student,
    blocking_swaps,
    is_feasible,
    is_score_feasible,
    pa_odr,
    shared_category_constrained_replacement_fairness,
    spse,
    swap_stability,
    threshold_adjusting_da,
    within_category_fairness,
)


class AdmissionsTest(unittest.TestCase):
    def test_spse_can_violate_score_feasibility(self) -> None:
        problem = AdmissionProblem(
            students=(
                Student("i1", 100, tuple(), (OPEN_CATEGORY,)),
                Student("i2", 95, ("t1", "t2"), ("t1", "t2", OPEN_CATEGORY)),
                Student("i3", 82, ("t2",), ("t2", OPEN_CATEGORY)),
            ),
            capacities={OPEN_CATEGORY: 1, "t1": 1, "t2": 1},
            bonuses={"t1": 5, "t2": 5},
            delta=10,
        )

        result = spse(problem)
        self.assertEqual(result.assignments[OPEN_CATEGORY], ("i1",))
        self.assertEqual(result.assignments["t1"], ("i2",))
        self.assertEqual(result.assignments["t2"], ("i3",))
        self.assertTrue(is_feasible(problem, result))
        self.assertTrue(within_category_fairness(problem, result))
        self.assertFalse(is_score_feasible(problem, result))

    def test_pa_odr_example_is_score_feasible(self) -> None:
        problem = AdmissionProblem(
            students=(
                Student("A", 100, tuple(), (OPEN_CATEGORY,)),
                Student("B", 86, ("t1", "t2"), ("t2", "t1", OPEN_CATEGORY)),
                Student("C", 84, ("t1",), ("t1", OPEN_CATEGORY)),
                Student("D", 82, ("t2",), ("t2", OPEN_CATEGORY)),
            ),
            capacities={OPEN_CATEGORY: 1, "t1": 1, "t2": 1},
            bonuses={"t1": 5, "t2": 10},
            delta=10,
        )

        result = pa_odr(problem)
        self.assertEqual(result.assignments[OPEN_CATEGORY], ("A",))
        self.assertEqual(result.assignments["t1"], ("B",))
        self.assertEqual(result.assignments["t2"], ("D",))
        self.assertTrue(is_feasible(problem, result, result.effective_capacities))
        self.assertTrue(is_score_feasible(problem, result, result.effective_capacities))
        self.assertTrue(within_category_fairness(problem, result))
        self.assertTrue(shared_category_constrained_replacement_fairness(problem, result))

    def test_threshold_adjusting_da_is_not_cardinality_maximal(self) -> None:
        problem = AdmissionProblem(
            students=(
                Student("A", 100, tuple(), (OPEN_CATEGORY,)),
                Student("B", 86, ("t1", "t2"), ("t2", "t1", OPEN_CATEGORY)),
                Student("D", 82, ("t2",), ("t2", OPEN_CATEGORY)),
            ),
            capacities={OPEN_CATEGORY: 1, "t1": 1, "t2": 1},
            bonuses={"t1": 5, "t2": 10},
            delta=10,
        )

        result = threshold_adjusting_da(problem)
        self.assertEqual(len(result.matched_students()), 2)
        self.assertEqual(result.assignments["t1"], tuple())
        self.assertEqual(result.assignments["t2"], ("B",))
        self.assertTrue(is_score_feasible(problem, result))

    def test_threshold_adjusting_da_is_feasible_and_within_fair(self) -> None:
        problem = AdmissionProblem(
            students=(
                Student("A", 100, tuple(), (OPEN_CATEGORY,)),
                Student("B", 92, ("t1",), ("t1", OPEN_CATEGORY)),
                Student("C", 80, ("t2",), ("t2", OPEN_CATEGORY)),
                Student("D", 78, ("t1", "t2"), ("t2", "t1", OPEN_CATEGORY)),
            ),
            capacities={OPEN_CATEGORY: 1, "t1": 1, "t2": 1},
            bonuses={"t1": 5, "t2": 5},
            delta=10,
        )

        result = threshold_adjusting_da(problem)
        self.assertTrue(is_feasible(problem, result))
        self.assertTrue(is_score_feasible(problem, result))
        self.assertTrue(within_category_fairness(problem, result))

    def test_pa_odr_admits_a_blocking_swap_across_the_open_category(self) -> None:
        # Example "PA-ODR admits justified envy" in main.tex, with i2 ranking o first:
        # PA-ODR fills o by raw score, so the two students hold each other's preferred route.
        problem = AdmissionProblem(
            students=(
                Student("i1", 100, ("t1",), ("t1", OPEN_CATEGORY)),
                Student("i2", 90, ("t1",), (OPEN_CATEGORY, "t1")),
            ),
            capacities={OPEN_CATEGORY: 1, "t1": 1},
            bonuses={"t1": 5},
            delta=10,
        )

        result = pa_odr(problem)
        self.assertEqual(result.assignments[OPEN_CATEGORY], ("i1",))
        self.assertEqual(result.assignments["t1"], ("i2",))
        self.assertTrue(is_score_feasible(problem, result, result.effective_capacities))
        self.assertTrue(swap_stability(problem, result, reserves_only=True))
        self.assertEqual(blocking_swaps(problem, result), [("i1", OPEN_CATEGORY, "i2", "t1")])

    def test_spse_and_tada_are_swap_stable(self) -> None:
        problem = AdmissionProblem(
            students=(
                Student("i1", 100, tuple(), (OPEN_CATEGORY,)),
                Student("i2", 95, ("t1", "t2"), ("t1", "t2", OPEN_CATEGORY)),
                Student("i3", 82, ("t2",), ("t2", OPEN_CATEGORY)),
                Student("i4", 80, ("t1", "t2"), (OPEN_CATEGORY, "t2", "t1")),
            ),
            capacities={OPEN_CATEGORY: 2, "t1": 1, "t2": 1},
            bonuses={"t1": 5, "t2": 5},
            delta=10,
        )

        for mechanism in (spse, threshold_adjusting_da):
            with self.subTest(mechanism=mechanism.__name__):
                result = mechanism(problem)
                self.assertTrue(swap_stability(problem, result, reserves_only=True))
                self.assertTrue(swap_stability(problem, result))


if __name__ == "__main__":
    unittest.main()
