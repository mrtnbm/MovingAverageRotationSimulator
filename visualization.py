import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors

class InvestmentGrowthGraph:
    def __init__(self, title, log_scale=True):
        plt.xlabel('Years')
        plt.ylabel('Invested Sum')
        plt.title('Non-Leveraged vs Leveraged Investment Over Time')
        if log_scale:
            plt.yscale('log',base=10)
        plt.gca().xaxis.set_major_locator(mdates.YearLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        plt.grid()
    
    def add_curve(self, dates, values, label):
        curve = plt.plot(dates, values, label=label)
        mplcursors.cursor(curve)

    def show(self):
        plt.legend()
        plt.show()
