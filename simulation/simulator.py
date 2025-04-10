from typing import List, Dict, Any
from .roulette import Roulette, RouletteType
from .strategies import BettingStrategy

class SimulationResult:
    def __init__(self, history: List[float], bankrupt: bool):
        self.history = history
        self.bankrupt = bankrupt

def simulate(
    roulette_type: RouletteType,
    strategy: BettingStrategy,
    initial_bankroll: float,
    max_spins: int
) -> SimulationResult:
    roulette = Roulette(roulette_type)
    strategy.reset()
    bankroll = initial_bankroll
    history = [bankroll]
    
    for _ in range(max_spins):
        if bankroll <= 0:
            return SimulationResult(history, True)
        
        bet = min(strategy.current_bet, bankroll)
        result = roulette.spin()
        win = result["color"] == "red"
        
        bankroll += bet if win else -bet
        history.append(bankroll)
        strategy.update(win)
    
    return SimulationResult(history, bankroll <= 0)