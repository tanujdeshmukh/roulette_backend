from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import sys

# Get absolute path to project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Now use absolute imports
from server.simulation.roulette import RouletteType
from server.simulation.strategies import Martingale, Fibonacci, DAlambert
from server.simulation.montecarlo import monte_carlo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class SimulationRequest(BaseModel):
    roulette_type: str
    strategy: str
    initial_bet: float
    bankroll: float
    max_spins: int
    simulations: int

@app.post("/simulate")
async def run_simulation(request: SimulationRequest):
    strategies = {
        "martingale": Martingale,
        "fibonacci": Fibonacci,
        "dalambert": DAlambert
    }
    
    results = monte_carlo(
        RouletteType(request.roulette_type),
        strategies[request.strategy](request.initial_bet),
        request.bankroll,
        request.max_spins,
        request.simulations
    )
    
    padded_histories = []
    for r in results:
        history = r.history
        desired_length = request.max_spins + 1
        if len(history) < desired_length:
            last_value = history[-1]
            padding = [last_value] * (desired_length - len(history))
            history = history + padding
        padded_histories.append(history)

    return {
        "histories": padded_histories,
        "bankruptcies": [r.bankrupt for r in results]
    }

@app.get("/")
async def health_check():
    return {"status": "running", "message": "Roulette Simulator API"}

class SpinRequest(BaseModel):
    roulette_type: str
    bet_number: int
    bet_amount: float
    bankroll: float

@app.post("/spin")
async def single_spin(request: SpinRequest):
    try:
        rt = RouletteType(request.roulette_type.lower())
        roulette = Roulette(rt)

        result = roulette.spin()
        spun_number = str(result['number'])      # e.g., '17' or '00'
        spun_color = result['color']             # red/black/green
        user_bet = str(request.bet_number)

        win = spun_number == user_bet
        new_bankroll = request.bankroll + request.bet_amount if win else request.bankroll - request.bet_amount
        earned = request.bet_amount if win else -request.bet_amount

        print(f"📥 [DEBUG] Request: Bet={user_bet}, Amount={request.bet_amount}, Bankroll={request.bankroll}")
        print(f"🎯 [DEBUG] Spun: {spun_number} ({spun_color}) | Win: {win}")
        print(f"💰 [DEBUG] New Bankroll: {new_bankroll}, Earned: {earned}\n")

        return {
            "spun_number": spun_number,
            "spun_color": spun_color,
            "win": win,
            "bankroll": new_bankroll,
            "earned": earned
        }

    except Exception as e:
        traceback.print_exc()  # Print full error to terminal
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/compare_strategies")
async def compare_strategies(request: SimulationRequest):
    strategies = {
        "martingale": Martingale,
        "fibonacci": Fibonacci,
        "dalambert": DAlambert
    }

    result_summary = {}

    for name, StrategyClass in strategies.items():
        runs = monte_carlo(
            RouletteType(request.roulette_type),
            StrategyClass(request.initial_bet),
            request.bankroll,
            request.max_spins,
            request.simulations
        )
        max_len = max(len(r.history) for r in runs)
        padded = [r.history + [r.history[-1]] * (max_len - len(r.history)) for r in runs]
        avg = [sum(x) / len(x) for x in zip(*padded)]
        result_summary[name] = avg

    return result_summary
    
def start_server():
    print("Starting FastAPI server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_server()