"""CLI for budgetmap."""
import sys, json, argparse
from .core import Budgetmap

def main():
    parser = argparse.ArgumentParser(description="BudgetMap — Government Budget Visualizer. Interactive visualization of government spending with AI analysis.")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "run", "info"])
    parser.add_argument("--input", "-i", default="")
    args = parser.parse_args()
    instance = Budgetmap()
    if args.command == "status":
        print(json.dumps(instance.get_stats(), indent=2))
    elif args.command == "run":
        print(json.dumps(instance.process(input=args.input or "test"), indent=2, default=str))
    elif args.command == "info":
        print(f"budgetmap v0.1.0 — BudgetMap — Government Budget Visualizer. Interactive visualization of government spending with AI analysis.")

if __name__ == "__main__":
    main()
