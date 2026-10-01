import pandas as pd
import numpy as np
from analytics.graph_builder import FinancialGraphBuilder
from analytics.circular_flow import CircularFraudDetector
from analytics.centrality_ranker import GraphRiskCentralityRanker

def generate_synthetic_transaction_network():
    np.random.seed(999)
    tx_list = []
    normal_users = [f"ACC_{i:03d}" for i in range(1, 30)]
    
    for _ in range(120):
        u, v = np.random.choice(normal_users, size=2, replace=False)
        tx_list.append({
            "sender": u,
            "receiver": v,
            "amount": round(float(np.random.exponential(scale=500) + 20), 2)
        })

    mules_ring_1 = ["MULE_ALPHA", "MULE_BETA", "MULE_GAMMA", "MULE_DELTA"]
    for i in range(len(mules_ring_1)):
        u = mules_ring_1[i]
        v = mules_ring_1[(i + 1) % len(mules_ring_1)]
        tx_list.append({"sender": u, "receiver": v, "amount": 25000.00})

    mules_ring_2 = ["MULE_X", "MULE_Y", "MULE_Z"]
    for i in range(len(mules_ring_2)):
        u = mules_ring_2[i]
        v = mules_ring_2[(i + 1) % len(mules_ring_2)]
        tx_list.append({"sender": u, "receiver": v, "amount": 42000.00})

    tx_list.append({"sender": "MULE_DELTA", "receiver": "NEXUS_LAUNDERER", "amount": 24500.00})
    tx_list.append({"sender": "NEXUS_LAUNDERER", "receiver": "OFFSHORE_ACC", "amount": 24000.00})

    return pd.DataFrame(tx_list)

def run_fraud_analytics():
    print("=" * 64)
    print("   OMNIGRAPH: ADVANCED GRAPH ANALYTICS & FRAUD DETECTION        ")
    print("=" * 64)

    tx_df = generate_synthetic_transaction_network()
    print(f"[OK] Ingested {len(tx_df)} financial network transactions.")

    G = FinancialGraphBuilder.build_directed_graph(tx_df)
    print(f"--> Built Directed Network: {G.number_of_nodes()} Nodes, {G.number_of_edges()} Edges")

    print("\n[1] Detecting Circular Smurfing Loops (Cycles)...")
    detector = CircularFraudDetector(max_cycle_length=5)
    suspicious_cycles = detector.find_suspicious_cycles(G)

    print(f"Discovered {len(suspicious_cycles)} circular fraud loops:")
    for idx, c in enumerate(suspicious_cycles, 1):
        print(f"  Cycle #{idx} ({c['hop_count']} Hops | Total Volume: ${c['total_cycle_volume']:,.2f}):")
        print(f"    Path: {c['cycle_path']}")

    print("\n[2] Computing Topological Risk & Betweenness Centrality...")
    ranker = GraphRiskCentralityRanker()
    risk_df = ranker.compute_entity_risk(G)
    
    print("\nTop High-Risk Suspicious Nexus Entities:")
    print(risk_df.head(8)[["entity_id", "pagerank", "betweenness", "inflow", "outflow", "composite_risk_score"]])

    print("\n" + "=" * 64)
    print("            GRAPH ANALYTICS AUDIT COMPLETED SUCCESSFULLY        ")
    print("=" * 64)

if __name__ == "__main__":
    run_fraud_analytics()
