# import matplotlib.pyplot as plt
# from main import stocks_data
# import time
#
# data = stocks_data()
#
# ticker = data[0][0]
# date = data[0][1]
# start = data[0][3]
# end = data[-1][6]
#
# stock = []
# time_list = []
# for i in data:
#     if i[2] >= '09:30:00' and i[2] <= '16:00:00':
#         open = (i[3])
#         close = (i[6])
#         t = time.strptime(i[2], "%H:%M:%S")
#         timevalue_12hour = time.strftime("%I:%M %p", time.strptime(i[2], "%H:%M:%S"))
#         time_list.append(timevalue_12hour)
#         avg = round((open+close) / 2, 2)
#         stock.append(avg)
#
# plt.plot(time_list, stock)
#
# step = len(time_list) // 5
# x_ticks = time_list[::step]
# plt.xticks(x_ticks)
#
# plt.xlabel('Time of the Day')
# plt.ylabel('Stock Price')
# plt.title(ticker)
#
# plt.ylim(min(stock) - 2, max(stock) + 2)
# graph_file = 'static/images/chart.png'  # Specify the path where you want to save the graph
# plt.savefig(graph_file)
# plt.show()