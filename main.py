import sqlite3
from scrape import intra_day_data
def stocks_data(ticker, howlonggo):

    if howlonggo == '5D':
        howlonggo = 5

    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM stock_data WHERE ticker = ?", (ticker,))
    count = cursor.fetchone()[0]

    cursor.execute("SELECT IFNULL(MAX(date), 'No data') FROM stock_data WHERE ticker = ?", (ticker,))
    latest_date_sql = cursor.fetchone()[0]

    stock_data, latest_date_url = intra_day_data(ticker, howlonggo)

    if latest_date_url > latest_date_sql:
        for data in stock_data[::-1]:
            date = data[0].split()[0]
            time = data[0].split()[1]
            stock_open, high, low, close, volume = data[1:6]

            cursor.execute(
                "INSERT INTO stock_data (ticker, date, time, open, high, low, close, volume) "
                "SELECT ?, ?, ?, ?, ?, ?, ?, ? "
                "WHERE NOT EXISTS "
                "(SELECT 1 FROM stock_data WHERE ticker = ? AND date = ? AND time = ?)",
                (ticker, date, time, stock_open, high, low, close, volume, ticker, latest_date_url, time)
            )

        cursor.execute("SELECT * FROM stock_data WHERE ticker = ? AND date = ?", (ticker, latest_date_url))
        data = cursor.fetchall()

    elif count > 0:
        cursor.execute("SELECT * FROM stock_data WHERE ticker = ? AND date = ?", (ticker, latest_date_url))
        data = cursor.fetchall()

    else:
        for data in stock_data[::-1]:
            date = data[0].split()[0]
            time = data[0].split()[1]
            stock_open, high, low, close, volume = data[1:6]

            # Check if the same data already exists in the table, if not then then perform insertion
            cursor.execute(
                "INSERT INTO stock_data (ticker, date, time, open, high, low, close, volume) "
                "SELECT ?, ?, ?, ?, ?, ?, ?, ? "
                "WHERE NOT EXISTS "
                "(SELECT 1 FROM stock_data WHERE ticker = ? AND date = ? AND time = ?)",
                (ticker, date, time, stock_open, high, low, close, volume, ticker, date, time)
            )

        cursor.execute("SELECT * FROM stock_data WHERE ticker = ?", (ticker,))
        data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data