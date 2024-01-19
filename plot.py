
import matplotlib.pyplot as plt
import os

def create_scatter_plot(data):

    plt.plot(data[0], data[1], color='orange', marker='o', linestyle='-')

    # Add labels and title
    plt.xlabel(data[2])
    plt.ylabel(data[3])
    plt.title(data[4])

    # Save the plot as an image
    if not os.path.exists('graphs'):
            os.makedirs('graphs')
    os.chdir('graphs')

    plt.savefig(data[5])
    plt.show()

    return "Plotted Sucsessfully"

if __name__ == "__main__":

    data = [
        ["1/3/2023", "1/4/2023", "1/5/2023", "1/6/2023", "1/9/2023", "1/10/2023", "1/11/2023", "1/12/2023", "1/16/2023", "1/9/2024", "1/10/2024", "1/11/2024", "1/12/2024", "1/16/2024"],
        ["$1,184,967.73", "$1,177,249.45", "$1,169,722.32", "$1,180,115.08", "$1,188,183.54", "$1,200,769.00", "$1,206,638.01", "$1,215,356.74", "$1,193,096.68", "$1,209,930.45", "$1,200,769.00", "$1,206,638.01", "$1,215,356.74", "$1,193,096.68"],
        "Date",
        "COINS Portfolio Value in USD",
        "Spread of COINS Portfolio",
        "spread_of_coins_portfolio.png"
    ]

    create_scatter_plot(data)