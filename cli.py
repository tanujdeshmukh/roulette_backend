import click
import matplotlib.pyplot as plt
import numpy as np
# Absolute import (recommended)
from server.simulation.roulette import RouletteType
from server.simulation.strategies import Martingale, Fibonacci, DAlambert
from server.simulation.montecarlo import monte_carlo

STRATEGIES = {
    "martingale": Martingale,
    "fibonacci": Fibonacci,
    "dalambert": DAlambert,
}

@click.command()
@click.option("--type", type=click.Choice([t.value for t in RouletteType]), prompt=True)
@click.option("--strategy", type=click.Choice(list(STRATEGIES.keys())), prompt=True)
@click.option("--initial-bet", type=float, prompt=True)
@click.option("--bankroll", type=float, prompt=True)
@click.option("--max-spins", type=int, default=100)
@click.option("--simulations", type=int, default=1000)
def main(type, strategy, initial_bet, bankroll, max_spins, simulations):
    results = monte_carlo(
        RouletteType(type),
        STRATEGIES[strategy](initial_bet),
        bankroll,
        max_spins,
        simulations
    )
    
    # Visualization
    plt.figure(figsize=(12, 6))
    for res in results:
        plt.plot(res.history, alpha=0.1, color="blue")
    
    # Plot median trajectory
    max_length = max(len(r.history) for r in results)
    padded = [r.history + [r.history[-1]]*(max_length - len(r.history)) for r in results]
    median = np.median(padded, axis=0)
    plt.plot(median, color="red", linewidth=2, label="Median")
    
    plt.title("Monte Carlo Simulation Results")
    plt.xlabel("Spin Number")
    plt.ylabel("Bankroll ($)")
    plt.grid(True)
    plt.legend()
    plt.savefig("results.png")
    plt.show()

if __name__ == "__main__":
    main()
