# config/pricing_config.py

# Base cost in USD for each analysis type (based on estimated API usage, compute time, etc.)
BASE_PRICES = {
    "Analyze Data": 0.015,           # base OpenAI-like cost per token (approx.)
    "Analyze Feedback": 0.020,
    "Chat With Document": 0.010,
}

# Estimated token usage for each analysis task (adjust as needed)
ESTIMATED_TOKEN_USAGE = {
    "Analyze Data": 1500,
    "Analyze Feedback": 2000,
    "Chat With Document": 1000,
}

# Your markup multiplier (e.g., 2.0 means 100% profit margin)
MARKUP_MULTIPLIER = 4.0


def calculate_price(analysis_type: str) -> float:
    """
    Calculate final price for the given analysis type based on estimated token usage and markup.
    """
    base_cost_per_token = BASE_PRICES.get(analysis_type, 0.015)
    estimated_tokens = ESTIMATED_TOKEN_USAGE.get(analysis_type, 1000)

    raw_cost = base_cost_per_token * estimated_tokens / 1000  # convert to per-token cost
    final_price = round(raw_cost * MARKUP_MULTIPLIER, 2)

    return final_price
