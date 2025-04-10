from simulation.simulator import simulate, SimulationResult
from simulation.roulette import RouletteType
from simulation.strategies import BettingStrategy
from typing import List

def monte_carlo(
    roulette_type: RouletteType,
    strategy: BettingStrategy,
    initial_bankroll: float,
    max_spins: int,
    num_simulations: int
) -> List[SimulationResult]:
    return [
        simulate(roulette_type, strategy, initial_bankroll, max_spins)
        for _ in range(num_simulations)
    ]