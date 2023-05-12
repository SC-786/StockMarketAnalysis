import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
from main import stocks_data
import time

app = Flask(__name__, template_folder='templates', static_folder='static')

#
# @app.route("/stockprice/")
# def index():
#   return render_template("index.html", relative_to=".")

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        time_range = request.form.get('time_range')

        # Generate the stock data and graph
        data = stocks_data(symbol, time_range)

        ticker = data[0][0]
        date = data[0][1]
        start = data[0][3]
        end = data[-1][6]

        # Generate the graph
        stock = []
        time_list = []
        for i in data:
            if i[2] >= '09:30:00' and i[2] <= '16:00:00':
                open_price = i[3]
                close_price = i[6]
                t = time.strptime(i[2], "%H:%M:%S")
                timevalue_12hour = time.strftime("%I:%M %p", time.strptime(i[2], "%H:%M:%S"))
                time_list.append(timevalue_12hour)
                avg = round((open_price + close_price) / 2, 2)
                stock.append(avg)

        plt.plot(time_list, stock)

        step = len(time_list) // 5
        x_ticks = time_list[::step]
        plt.xticks(x_ticks)

        plt.xlabel('Time of the Day')
        plt.ylabel('Stock Price')
        plt.title(ticker.upper())

        plt.ylim(min(stock) - 2, max(stock) + 2)
        graph_file = 'static/images/chart.png'  # Specify the path where you want to save the graph
        plt.savefig(graph_file)

        return render_template("graph.html", graph_file=graph_file)

    return render_template("index.html", relative_to=".")


@app.route('/about')
def about():
    return 'The about page'
