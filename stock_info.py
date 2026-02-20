import yfinance as yf
import sys

def get_stock_info(ticker_symbol):
    try:
        # Create a ticker object
        ticker = yf.Ticker(ticker_symbol)
        
        # Get info
        info = ticker.info
        
        # Check if we got valid info (ticker.info can return a dict with few keys if not found)
        if 'regularMarketPrice' not in info and 'currentPrice' not in info:
            # Fallback check for valid symbol
            history = ticker.history(period="1d")
            if history.empty:
                print(f"Error: Could not find data for ticker '{ticker_symbol}'.")
                return
        
        # Extraction
        name = info.get('longName', ticker_symbol)
        price = info.get('currentPrice') or info.get('regularMarketPrice')
        currency = info.get('currency', 'USD')
        prev_close = info.get('regularMarketPreviousClose')
        
        print("\n" + "="*40)
        print(f" STOCK INFORMATION: {ticker_symbol.upper()} ")
        print("="*40)
        print(f"Company:  {name}")
        print(f"Price:    {price} {currency}")
        
        if price and prev_close:
            change = price - prev_close
            change_percent = (change / prev_close) * 100
            diff_str = f"{change:+.2f} ({change_percent:+.2f}%)"
            print(f"Change:   {diff_str}")
        
        print("="*40 + "\n")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("--- Stock Price Extractor ---")
    while True:
        symbol = input("Enter Stock Ticker (or 'q' to quit): ").strip().upper()
        if symbol == 'Q':
            break
        if not symbol:
            continue
        get_stock_info(symbol)
