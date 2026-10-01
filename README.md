# OmniGraph: Graph Analytics & Circular Fraud Detection Engine 🕸️🛡️

A production-grade network topology and graph analytics system designed to uncover money laundering rings, smurfing cycles, and high-centrality illicit money mule networks.

## Core Graph Algorithms Implemented
1. **Elementary Cycle Finding (Smurfing Ring Detection):**
   - Employs Johnson's cycle detection algorithm $O((V + E)(c + 1))$ to uncover closed loops of fund movement ($A \to B \to C \to A$).
2. **Centrality Matrix for Nexus Accounts:**
   - **PageRank**: Identifies high-prestige transaction accumulators.
   - **Betweenness Centrality**: Pinpoints intermediary laundering bridges:
     $$C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$
   - **In/Out Degree Asymmetry**: Detects fan-in (aggregation) and fan-out (layering) fraud behavior.
3. **Graph Density & Anomaly Scoring:**
   - Multi-metric composite risk heuristic integrating transaction volume velocity and cycle membership.
