import json
import os
import random
from dataclasses import dataclass, asdict, field
from typing import List, Dict

SAVE_FILE = "portfolio.json"

#data Structures

@dataclass
class Holding:
    symbol: str
    quantity: int
    avg_price: float

@dataclass
class Portfolio:
    cash: float = 10000.0
    holdings: Dict[str, Holding] = field(default_factory=dict)
    history: List[str] = field(default_factory=list)
    day: int = 1
    prices: Dict[str, float] = field(default_factory=dict)

#market simulation +/- 5% change

def init_prices() -> Dict[str, float]:
    return {"AAPL": 240.0, "TSLA": 340.0, "BTC": 150000.0, "ETH": 5600.0}

def update_prices(prices: Dict[str, float]) -> Dict[str, float]:
    new_prices = {}
    for sym, price in prices.items():
        change = random.uniform(-0.05, 0.05)
        new_prices[sym] = round(price * (1 + change), 2)
    return new_prices

#save/load

def save_portfolio(p: Portfolio):
    with open(SAVE_FILE, "w") as f:
        json.dump(asdict(p), f, indent=4)
    print("Portfolio Saved")

def load_portfolio() -> Portfolio:
    if not os.path.exists(SAVE_FILE):
        print("No saved portfolio found.")
        return None
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
    holdings = {s: Holding(**h) for s, h in data["holdings"].items()}
    return Portfolio(
        cash=data["cash"],
        holdings=holdings,
        history=data["history"],
        day=data["day"],
        prices=data["prices"]
    )

#display menus

def display_main_menu():
    print(""" Portfolio Manager
          (N)ew portfolio
          (L)oad saved portfolio
          (Q)uit """)

def display_portfolio_menu():
    print("""\n Portfolio Manager
          (B)uy
          (S)ell
          (E)dit existing details
          (A)dd new symbol
          (H)oldings
          (U)pdate day
          (M)arket prices
          (R)eport summary
          (V)iew history
          (F)ilesave
          (C)ash edit
          (Q)uit to main menu""")

#functions

#buy
def buy_stock(p: Portfolio):
    symbol = input("Enter symbol to buy: ").upper()
    if symbol not in p.prices:
        print("Symbol not available in market.")
        return
    qty = int(input("Enter quantity: "))
    price = p.prices[symbol]
    cost = qty * price
    if cost > p.cash:
        print("Not enough money.")
        return
    if symbol in p.holdings:
        h = p.holdings[symbol]
        total_cost = h.avg_price * h.quantity + cost
        h.quantity += qty
        h.avg_price = total_cost / h.quantity
    else:
        p.holdings[symbol] = Holding(symbol, qty, price)
    p.cash -= cost
    p.history.append(f"Day {p.day}: Bought {qty} {symbol} @ {price}")
    print(f"Bought {qty} {symbol} for ${cost:.2f}")

#sell
def sell_stock(p: Portfolio):
    symbol = input("Enter symbol to sell: ").upper()
    if symbol not in p.holdings:
        print("You do not own this symbol.")
        return
    qty = int(input("Enter quantity: "))
    h = p.holdings[symbol]
    if qty > h.quantity:
        print("Not enough shares to sell.")
        return
    price = p.prices[symbol]
    revenue = qty * price
    h.quantity -= qty
    if h.quantity == 0:
        del p.holdings[symbol]
    p.cash += revenue
    p.history.append(f"Day {p.day}: Sold {qty} {symbol} @ {price}")
    print(f"Sold {qty} {symbol} for ${revenue:.2f}")

#edit holdings
def edit_holdings(p: Portfolio):
    symbol = input("Enter symbol to edit: ").upper()
    if symbol not in p.holdings:
        print("Holding not found.")
        return
    h = p.holdings[symbol]
    qty = int(input(f"Enter new quantity (current {h.quantity}): "))
    avg_price = float(input(f"Enter new avg price (current {h.avg_price}): "))
    h.quantity = qty
    h.avg_price = avg_price
    p.history.append(f"Day {p.day}: Edited {symbol} to {qty} shares @ {avg_price}")

#edit cash
def edit_cash(p: Portfolio):
    print(f"Current cash: ${p.cash:.2f}")
    new_cash = float(input("Enter new cash amount: "))
    p.cash = new_cash
    p.history.append(f"Day {p.day}: Cash edited to ${new_cash:.2f}")
    print(f"Cash updated to ${new_cash:.2f}")

#add symbol
def add_symbol(p: Portfolio):
    symbol = input("Enter new symbol: ").upper()
    price = float(input("Enter initial price: "))
    p.prices[symbol] = price
    print(f"Added {symbol} to market at price ${price:.2f}")

#view holdings
def view_holdings(p: Portfolio):
    print("\nYour holdings")
    if not p.holdings:
        print("No holdings")
    for h in p.holdings.values():
        market_value = h.quantity * p.prices[h.symbol]
        print(f"{h.symbol}: {h.quantity} shares @ {h.avg_price} (Value: ${market_value:.2f})")
    print(f"Cash: ${p.cash:.2f}")

#update day
def update_day(p: Portfolio):
    p.day += 1
    p.prices = update_prices(p.prices)
    p.history.append(f"Day {p.day}: Prices updated")
    print(f"Day {p.day} updated.")

#view prices
def view_prices(p: Portfolio):
    print("\nMarket Prices")
    for sym, price in p.prices.items():
        print(f"{sym}: ${price:.2f}")

#report summary
def report_summary(p: Portfolio):
    total_value = p.cash
    for h in p.holdings.values():
        total_value += h.quantity * p.prices[h.symbol]
    print("\nPortfolio summary")
    print(f"Day: {p.day}")
    print(f"Cash: ${p.cash:.2f}")
    print(f"Total Value: ${total_value:.2f}")

#history
def view_history(p: Portfolio):
    print("\nHistory")
    if not p.history:
        print("No history recorded")
    for entry in p.history:
        print(entry)

#main loop
def main():
    portfolio = None
    while True:
        if portfolio is None:
            display_main_menu()
            choice = input("Choice: ").upper()
            if choice == "N":
                portfolio = Portfolio(prices=init_prices())
                print("New portfolio created")
            elif choice == "L":
                portfolio = load_portfolio()
            elif choice == "Q":
                break

        else:
            display_portfolio_menu()
            choice = input("Choice: ").upper()
            if choice == "B": buy_stock(portfolio)
            elif choice == "S": sell_stock(portfolio)
            elif choice == "E": edit_holdings(portfolio)
            elif choice == "A": add_symbol(portfolio)
            elif choice == "H": view_holdings(portfolio)
            elif choice == "U": update_day(portfolio)
            elif choice == "M": view_prices(portfolio)
            elif choice == "R": report_summary(portfolio)
            elif choice == "V": view_history(portfolio)
            elif choice == "F": save_portfolio(portfolio)
            elif choice == "C": edit_cash(portfolio)
            elif choice == "Q": portfolio = None

if __name__ == "__main__":
    main()
