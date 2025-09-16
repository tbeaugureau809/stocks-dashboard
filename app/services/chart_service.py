from indicators_service import get_history_with_sma, get_fast_info
import matplotlib.pyplot as plt

def plot_history_with_sma(df, symbol:str):

    plt.figure(figsize=(10,5))

    plt.plot(df.index, df["Close"], label="Close", color="black")
    plt.plot(df.index, df["SMA20"], label="SMA20", color="blue")
    plt.plot(df.index, df["SMA50"], label="SMA50", color="red")

    plt.title(f"{symbol} - Close with SMA20 & SMA50")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()

    plt.savefig("chart.png")
    print("Chart saved to chart.png")
    plt.show()

def main():
    df = get_history_with_sma("AAPL")
    plot_history_with_sma(df, "AAPL")

    facts = get_fast_info("AAPL")
    print("Fast Info", facts)


if __name__ == "__main__":
    main()
