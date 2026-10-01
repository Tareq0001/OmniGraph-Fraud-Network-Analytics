import networkx as nx
from typing import List, Dict

class CircularFraudDetector:
    def __init__(self, max_cycle_length: int = 5):
        self.max_cycle = max_cycle_length

    def find_suspicious_cycles(self, G: nx.DiGraph) -> List[Dict]:
        cycles = list(nx.simple_cycles(G))
        suspicious = []

        for cycle in cycles:
            length = len(cycle)
            if 3 <= length <= self.max_cycle:
                cycle_edges = list(zip(cycle, cycle[1:] + [cycle[0]]))
                weights = [G[u][v]["weight"] for u, v in cycle_edges if G.has_edge(u, v)]
                min_flow = min(weights) if weights else 0.0
                total_flow = sum(weights)

                suspicious.append({
                    "cycle_path": " -> ".join(cycle) + f" -> {cycle[0]}",
                    "hop_count": length,
                    "bottleneck_flow": min_flow,
                    "total_cycle_volume": total_flow
                })

        return sorted(suspicious, key=lambda x: x["total_cycle_volume"], reverse=True)
