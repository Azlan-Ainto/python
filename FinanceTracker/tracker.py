import json
import os
from dataclasses import asdict, dataclass, asdict
from datetime import datetime
from typing import List

@dataclass
class Transaction:
    date: str
    category: str
    description: str
    amount: float # Positive for income, negative for expenses


class FinanceTracker:

    def __init__(self, filename: str ="data.json"):

        self.filename = filename
        self.transactions: List[Transaction] = self._load_data()

    #----lädt Daten aus der JSON-Datei ----

    def _load_data(self) -> List[Transaction]: 

        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as file:
            data = json.load(file)
            return [Transaction(**item) for item in data]


    def add_transaction(self, category: str, description: str, amount: float):

        neueTransaction = Transaction(
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            category = category,
            description = description,
            amount = amount
        )
        self.transactions.append(neueTransaction)
        self._save_data()


    def _save_data(self):

        with open(self.filename, 'w') as file:

            json.dump([asdict(tx) for tx in tx_list], file, indent=4)

            json.dump([asdict(tx) for tx in self.transactions], file, indent=4)



    def get_balance(self) -> float:

        return sum(tx.amount for tx in self.transactions)


    # --- Testen ----

    if __name__ == "__main__":

        tracker = FinanceTracker()
        tracker.add_transaction("Gehalt", "Monatsgehalt", 3000.00)
        tracker.add_transaction("Miete", "Wohnungsmiete", -1200.00)
        tracker.add_transaction("Lebensmittel", "Einkauf im Supermarkt", -300.00)
        print(f"Aktueller Kontostand: {tracker.get_balance():.2f} EUR")


     
        