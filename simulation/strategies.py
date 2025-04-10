from typing import Any  # Optional but good practice
from abc import ABC, abstractmethod

class BettingStrategy(ABC):
    def __init__(self, base_bet: float):
        self.base_bet = base_bet
        self.current_bet = base_bet

    @abstractmethod
    def update(self, win: bool):
        pass

    def reset(self):
        self.current_bet = self.base_bet

class Martingale(BettingStrategy):
    def update(self, win: bool):
        self.current_bet = (
            self.base_bet if win else self.current_bet * 2
        )

class Fibonacci(BettingStrategy):
    def __init__(self, base_bet: float):
        super().__init__(base_bet)
        self.fib = [1, 1]
        self.loss_streak = 0

    def update(self, win: bool):
        if win:
            self.loss_streak = 0
            self.current_bet = self.base_bet
        else:
            self.loss_streak += 1
            if self.loss_streak >= len(self.fib):
                self.fib.append(self.fib[-1] + self.fib[-2])
            self.current_bet = self.base_bet * self.fib[self.loss_streak]

class DAlambert(BettingStrategy):
    def update(self, win: bool):
        self.current_bet = (
            max(self.base_bet, self.current_bet - self.base_bet) if win else
            self.current_bet + self.base_bet
        )