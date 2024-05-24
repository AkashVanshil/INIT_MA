import pandas as pd

class StockTradingBot:
    def __init__(self,short_window, long_window, initial_cash):
        self.short_window = short_window
        self.long_window = long_window
        self.cash = initial_cash
        self.stock_balance = 0
        self.history = []

    def get_stock_data(self, file_path):
        # Read the CSV file
        data = pd.read_csv(file_path, index_col=0, parse_dates=True)

        # Print column names to verify
        print("Columns in CSV file:", data.columns)

        # Strip leading/trailing spaces from column names
        data.columns = data.columns.str.strip()

        return data

    def calculate_sma(self, data, window):
        return data['close'].rolling(window=window).mean()

    def buy(self, price, amount):
        total_cost = price * amount
        if self.cash >= total_cost:
            self.cash -= total_cost
            self.stock_balance += amount
            self.history.append(f"Bought {amount} shares at ${price:.2f} each")
            print(f"Bought {amount} shares at ₹{price:.2f} each")

    def sell(self, price, amount):
        if self.stock_balance >= amount:
            total_sale = price * amount
            self.cash += total_sale
            self.stock_balance -= amount
            self.history.append(f"Sold {amount} shares at ₹ {price:.2f} each")
            print(f"Sold {amount} shares at ₹ {price:.2f} each")

    def execute_strategy(self, data):
        short_sma = self.calculate_sma(data, self.short_window)
        long_sma = self.calculate_sma(data, self.long_window)
        for i in range(self.long_window, len(data)):
            if short_sma.iloc[i] > long_sma.iloc[i]:
                # Buy signal: Short-term SMA crosses above Long-term SMA
                self.buy(data['close'].iloc[i], 10)  # Example: Buy 10 shares
            elif short_sma.iloc[i] < long_sma.iloc[i]:
                # Sell signal: Short-term SMA crosses below Long-term SMA
                self.sell(data['close'].iloc[i], 10)  # Example: Sell 10 shares

    def run(self, file_path):
        data = self.get_stock_data(file_path)  # Adjust file path as needed
        self.execute_strategy(data)
        self.display_portfolio(data)

    def display_portfolio(self, data):
        print(f"Portfolio Summary:")
        print(f"Cash: ₹ {self.cash:.2f}")
        print(f"Stock Balance: {self.stock_balance} shares")
        print(f"Portfolio Value:₹  {(self.cash + self.stock_balance * data['close'].iloc[-1]):.2f}")
    def display_closevalue(self,data):
        data['close'].plot()


if __name__ == "__main__":
    bot = StockTradingBot( short_window=50, long_window=109, initial_cash=120000)
    bot.run(r'data\Quote-Equity-ICICIBANK-EQ-23-05-2023-to-23-05-2024_processed.csv') 