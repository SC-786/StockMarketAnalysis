import sqlite3
from scrape import intra_day_data

def stocks_data():
    ticker = input("Enter a stock symbol name (e.g., AAPL): ").upper()
    howlonggo = input("How long ago do you want to view the stock price (e.g., 1D, 5D, 1M): ").upper()

    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM stock_data WHERE ticker = ?", (ticker,))
    count = cursor.fetchone()[0]

    cursor.execute("SELECT IFNULL(MAX(date), 'No data') FROM stock_data WHERE ticker = ?", (ticker,))
    latest_date_sql = cursor.fetchone()[0]
    stock_data, latest_date_url = intra_day_data(ticker)

    insert_data = []
    for data in stock_data[::-1]:
        date, time = data[0].split()
        stock_open, high, low, close, volume = data[1:6]
        insert_data.append((ticker, date, time, stock_open, high, low, close, volume))

    if latest_date_url > latest_date_sql:
        cursor.executemany(
            "INSERT INTO stock_data (ticker, date, time, open, high, low, close, volume) "
            "SELECT ?, ?, ?, ?, ?, ?, ?, ? "
            "WHERE NOT EXISTS "
            "(SELECT 1 FROM stock_data WHERE ticker = ? AND date = ? AND time = ?)",
            insert_data
        )

    if count > 0 or latest_date_url > latest_date_sql:
        cursor.execute("SELECT * FROM stock_data WHERE ticker = ? AND date = ?", (ticker, latest_date_url))
        data = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM stock_data WHERE ticker = ?", (ticker,))
        data = cursor.fetchall()

    conn.commit()
    conn.close()
    return data

