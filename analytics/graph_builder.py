import pandas as pd
import networkx as nx

class FinancialGraphBuilder:
    @staticmethod
    def build_directed_graph(transactions_df: pd.DataFrame) -> nx.DiGraph:
        G = nx.DiGraph()
        for _, row in transactions_df.iterrows():
            sender = str(row["sender"])
            receiver = str(row["receiver"])
            amt = float(row["amount"])

            if G.has_edge(sender, receiver):
                G[sender][receiver]["weight"] += amt
                G[sender][receiver]["tx_count"] += 1
            else:
                G.add_edge(sender, receiver, weight=amt, tx_count=1)

        return G
