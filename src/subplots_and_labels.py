import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from constants.constants import *

pio.renderers.default = "browser"


def get_candlestick_plot(
    df: pd.DataFrame, ma1: int, ma2: int, ma3: int, ma4: int, ticker: str
) -> go.Figure:

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=(f"{ticker} Stock Price", "Volume Chart"),
        row_width=[0.3, 0.7],
    )

    fig.add_trace(
        go.Candlestick(
            x=df["date"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="Candlestick chart",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Line(x=df["date"], y=df[f"{ma1}_ma"], name=f"{ma1} SMA"),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Line(x=df["date"], y=df[f"{ma2}_ma"], name=f"{ma2} SMA"),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Line(x=df["date"], y=df[f"{ma3}_ma"], name=f"{ma3} SMA"),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Line(x=df["date"], y=df[f"{ma4}_ma"], name=f"{ma4} SMA"),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(x=df["date"], y=df["Volume BTC"], name="Volume BTC"),
        row=2,
        col=1,
    )

    fig["layout"]["xaxis2"]["title"] = "Date"
    fig["layout"]["yaxis"]["title"] = "Price"
    fig["layout"]["yaxis2"]["title"] = "Volume"

    fig.update_xaxes(
        rangebreaks=[{"bounds": ["sat", "mon"]}],
        rangeslider_visible=False,
    )

    return fig


if __name__ == "__main__":
    df = pd.read_csv(
        BINANCE_BTCUSDT_DAY,
        usecols=["date", "symbol", "open", "high", "low", "close", "Volume BTC"],
        skiprows=1,
    )

    df["10_ma"] = df["close"].rolling(10).mean()
    df["20_ma"] = df["close"].rolling(20).mean()
    df["50_ma"] = df["close"].rolling(50).mean()
    df["100_ma"] = df["close"].rolling(100).mean()

    # reverse the data
    df = df[::-1]

    fig = get_candlestick_plot(df[-120:], 10, 20, 50, 100, BINANCE_BTCUSDT_DAY)
    fig.show()
