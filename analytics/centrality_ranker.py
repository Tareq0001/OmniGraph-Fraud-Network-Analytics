import networkx as nx
import pandas as pd

class GraphRiskCentralityRanker:
    @staticmethod
    def compute_entity_risk(G: nx.DiGraph) -> pd.DataFrame:
        pagerank = nx.pagerank(G, weight="weight")
        betweenness = nx.betweenness_centrality(G, weight="weight")
        in_degree = dict(G.in_degree(weight="weight"))
        out_degree = dict(G.out_degree(weight="weight"))

        entities = list(G.nodes())
        records = []
        for node in entities:
            in_val = in_degree.get(node, 0.0)
            out_val = out_degree.get(node, 0.0)
            ratio = (out_val / in_val) if in_val > 0 else 0.0

            risk_score = (
                (pagerank.get(node, 0.0) * 40.0) +
                (betweenness.get(node, 0.0) * 40.0) +
                (10.0 if (in_val > 10000 and out_val > 10000 and 0.8 <= ratio <= 1.2) else 0.0)
            )

            records.append({
                "entity_id": node,
                "pagerank": round(pagerank.get(node, 0.0), 5),
                "betweenness": round(betweenness.get(node, 0.0), 5),
                "inflow": round(in_val, 2),
                "outflow": round(out_val, 2),
                "flow_ratio": round(ratio, 2),
                "composite_risk_score": round(min(risk_score * 10.0, 100.0), 2)
            })

        df = pd.DataFrame(records)
        return df.sort_values(by="composite_risk_score", ascending=False).reset_index(drop=True)
