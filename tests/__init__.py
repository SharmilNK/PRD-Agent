import os

# Tests use fake Claude replies with fixed token counts, so the real $2 default budget would skip
# steps unpredictably. Budget behaviour has its own tests that pass an explicit budget.
os.environ["PRD_AGENT_MAX_COST_USD"] = "none"
