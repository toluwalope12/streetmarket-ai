
### `docs/architecture.md`
```markdown
# System Architecture

STREETMARKET AI uses six specialized agents coordinated by an Orchestrator with a 0.8 quality gate.

## Agents
- **Scout Agent**: Parses unstructured vendor messages.
- **Price Prophet Agent**: Uses ES|QL ENRICH to detect price arbitrage.
- **Credit Architect Agent**: Calculates alternative credit scores from transaction history.
- **Trust Verifier Agent**: Uses vector search for counterfeit detection.
- **Logistics Guard Agent**: Geo-search for protest-aware routing.
- **Market Intel Agent**: Analyzes foot traffic for optimal selling locations.
- **Orchestrator Agent**: Coordinates all agents and implements self-healing loops.

## Workflow
1. Vendor message → Scout Agent → structured data
2. Orchestrator calls Price Prophet and Credit Architect
3. Responses combined, passed to Verification Agent
4. If quality score < 0.8, refine (max 3 iterations)
5. Final response sent to vendor

## Data Flow