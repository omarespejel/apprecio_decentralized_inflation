""" @dev Functions that calculate the Consumer Price Index (CPI) for a basket
    of curated goods and the inflation rate between two CPIs.

    The get_inflation() function synthesizes all the other functions.
"""

from typing import Dict, List, Optional
from numpy import nanmedian, array, sum, around


def aggregate_prices_median(prices: Dict) -> List:
    """@dev Returns a list with the median values of a dictionary containing
    several prices for each item. Example of the input:

      {'carne': [87, 45, 87],
      'lacteos': [54, 23, 65, 232, 54],
      'manzanas': [1, 1, 2, 3, 4, 3],
      'peras': [8, 9, 8, 9, 7]}

    The returned list would be:

      [2.5, 8.0, 87.0, 54.0]
    """
    prices_median = []

    for article in prices.values():
        median = nanmedian(array(article))
        prices_median.append(median.item())

    return prices_median


def calculate_simple_CPI(
    base_prices: List, period_prices: List, decimals: int = 2
) -> float:
    """@dev Returns the CPI for a determined period.

    Inputs: a basket prices for:
        - base_prices: List of floats containing the prices for the base period.
        - period_prices: List of floats containing the prices for the period's CPI we are looking for.
        - decimals: int with the number of decimals the CPI will have.

    The order of the prices is not relevant. However, the items in the
    basket should not change, otherwise, the comparing periods would not
    be comparable.
    """
    base_prices_np, period_prices_np = array(base_prices), array(period_prices)
    base, period = sum(base_prices_np), sum(period_prices_np)
    period_cpi = (period / base) * 100
    return around(period_cpi, decimals=decimals).item()


def calculate_inflation_rate(
    period_1: float, period_2: float, decimals: float = 2
) -> float:
    """@dev Returns the inflation rate between two periods."""
    rate = ((period_2 - period_1) / period_1) * 100
    return float(format(rate, f".{decimals}f"))


def get_aggregated_prices_and_inflation(
    base_prices: Dict,
    period_2_prices: Dict,
    period_1_prices: Optional[Dict] = None,
    inflation_against_base: bool = False,
) -> Dict:
    """@dev For a certain period (period_2_prices)returns (1) the inflation rate and (2) the median aggregated prices.

    Requires prices for a base period, a first period to compare (optional) and the period of interest.
    Example of the dictionaries required:

      {'carne': [87, 45, 87],
      'lacteos': [54, 23, 65, 232, 54],
      'manzanas': [1, 1, 2, 3, 4, 3],
      'peras': [8, 9, 8, 9, 7]}

    Returns a dictionary with keys: inflation: float, aggregated_prices: List[float], CPI: float
    """

    base_prices = aggregate_prices_median(base_prices)
    base_CPI = calculate_simple_CPI(base_prices, base_prices)  # must always be 100

    if inflation_against_base == False and period_1_prices != None:
        period_1_prices = aggregate_prices_median(period_1_prices)
        period_2_prices = aggregate_prices_median(period_2_prices)

        period_1_CPI = calculate_simple_CPI(base_prices, period_1_prices)
        period_2_CPI = calculate_simple_CPI(base_prices, period_2_prices)

        print(
            f"Calculating inflation rate between CPIs: {period_1_CPI} and {period_2_CPI}."
        )
        inflation = calculate_inflation_rate(period_1_CPI, period_2_CPI)

    else:
        period_2_prices = aggregate_prices_median(period_2_prices)

        period_2_CPI = calculate_simple_CPI(base_prices, period_2_prices)

        print(f"Calculating inflation rate between base period and CPI {period_2_CPI}.")
        inflation = calculate_inflation_rate(base_CPI, period_2_CPI)

    return dict(
        inflation=inflation, aggregated_prices=period_2_prices, CPI=period_2_CPI
    )
