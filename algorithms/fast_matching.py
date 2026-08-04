"""Polynomial-time PrefLexMaxMatching.

The brute-force enumerator in :mod:`algorithms.admissions` walks every
capacity-feasible reserve assignment, which is exponential and caps usable
instances at a few dozen students.  This module implements the route the paper
describes instead:

* criteria 1--2 (maximum cardinality, then lexicographically maximal sorted
  vector of elevated scores) select the admitted set by matroid greedy over the
  transversal matroid of the feasibility graph, scanning students in decreasing
  elevated score and keeping one whenever the current matching can be augmented;
* criteria 3--4 (lexicographically minimal sorted vector of preference ranks,
  then the ``2^p`` tie-break) distribute that admitted set over the categories,
  encoded as one min-cost assignment with cost ``C3 * B**rank + 2**p``.

``B`` exceeds the number of admissible pairs, so summing ``B**rank`` compares
sorted rank vectors without carrying, and ``C3`` dominates every possible sum of
``2**p`` terms, so the tie-break never overrides criterion 3.
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple


def _augment(sid: str, adj: Dict[str, List[str]], caps: Dict[str, int],
             holders: Dict[str, List[str]], visited: set) -> bool:
    """Kuhn augmenting step against categories with capacity ``caps``."""
    for category in adj[sid]:
        if category in visited:
            continue
        visited.add(category)
        if len(holders[category]) < caps[category]:
            holders[category].append(sid)
            return True
        for slot, occupant in enumerate(holders[category]):
            if _augment(occupant, adj, caps, holders, visited):
                holders[category][slot] = sid
                return True
    return False


def admitted_set(students_by_score: Sequence[str], adj: Dict[str, List[str]],
                 caps: Dict[str, int]) -> List[str]:
    """Criteria 1--2: the unique lexicographically score-maximal basis.

    Scanning in decreasing elevated score and keeping a student exactly when the
    current maximum matching can be augmented is the matroid greedy, so the
    result is independent of how ties inside the matching are resolved.
    """
    holders: Dict[str, List[str]] = {category: [] for category in caps}
    admitted: List[str] = []
    for sid in students_by_score:
        if _augment(sid, adj, caps, holders, set()):
            admitted.append(sid)
    return admitted


def _min_cost_assignment(admitted: Sequence[str], adj: Dict[str, List[str]],
                         caps: Dict[str, int],
                         cost: Dict[Tuple[str, str], int]) -> Dict[str, Tuple[str, ...]]:
    """Successive shortest paths on the unit-supply assignment network.

    Nodes are ``source``, one per admitted student, one per category, ``sink``.
    Costs are exact Python integers, so the ``B**rank`` encoding of criterion 3
    is compared without rounding.
    """
    categories = list(caps)
    source, sink = "#src", "#snk"
    nodes = [source, sink] + list(admitted) + categories
    graph: Dict[str, Dict[str, List[int]]] = {n: {} for n in nodes}

    def add_edge(u: str, v: str, capacity: int, edge_cost: int) -> None:
        graph[u][v] = [capacity, edge_cost]
        graph[v].setdefault(u, [0, -edge_cost])

    for sid in admitted:
        add_edge(source, sid, 1, 0)
        for category in adj[sid]:
            add_edge(sid, category, 1, cost[(sid, category)])
    for category in categories:
        add_edge(category, sink, caps[category], 0)

    flow_needed = len(admitted)
    while flow_needed > 0:
        # Bellman-Ford: residual costs are non-negative here, but negative
        # reverse arcs appear once flow is pushed, so we do not use Dijkstra.
        dist: Dict[str, object] = {n: None for n in nodes}
        dist[source] = 0
        parent: Dict[str, str] = {}
        for _ in range(len(nodes)):
            changed = False
            for u in nodes:
                du = dist[u]
                if du is None:
                    continue
                for v, (capacity, edge_cost) in graph[u].items():
                    if capacity <= 0:
                        continue
                    nd = du + edge_cost
                    if dist[v] is None or nd < dist[v]:
                        dist[v] = nd
                        parent[v] = u
                        changed = True
            if not changed:
                break
        if dist[sink] is None:
            break  # admitted set was not fully matchable; should not happen

        path = []
        v = sink
        while v != source:
            u = parent[v]
            path.append((u, v))
            v = u
        push = min(graph[u][v][0] for u, v in path)
        for u, v in path:
            graph[u][v][0] -= push
            graph[v][u][0] += push
        flow_needed -= push

    result: Dict[str, List[str]] = {category: [] for category in categories}
    for sid in admitted:
        for category in adj[sid]:
            # residual capacity 0 on a forward unit arc means it carries flow
            if graph[sid][category][0] == 0 and graph[category][sid][0] > 0:
                result[category].append(sid)
                break
    return {category: tuple(assignees) for category, assignees in result.items()}


def pref_lex_max_matching(students_by_score: Sequence[str], adj: Dict[str, List[str]],
                          caps: Dict[str, int],
                          rank: Dict[Tuple[str, str], int],
                          pair_index: Dict[Tuple[str, str], int]) -> Dict[str, Tuple[str, ...]]:
    """Full four-criteria selection.

    ``students_by_score`` must be ordered by decreasing elevated score, ``adj``
    lists the admissible categories of each student, ``rank`` gives ``r_i(t)``
    and ``pair_index`` the injective index ``p(i,t)`` of the paper.
    """
    admitted = admitted_set(students_by_score, adj, caps)
    if not admitted:
        return {category: tuple() for category in caps}

    pairs = len(pair_index)
    base = pairs + 1
    dominating = 1 << (pairs + 1)  # exceeds any sum of the 2**p terms
    cost = {
        pair: dominating * base ** rank[pair] + (1 << pair_index[pair])
        for pair in pair_index
    }
    return _min_cost_assignment(admitted, adj, caps, cost)
