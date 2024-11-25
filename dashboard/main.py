import streamlit as st

from frontend.st_utils import auth_system


def main():
    # readme section
    st.markdown("# Welcome to KhanBot!")
    st.markdown("Welcome to KhanBot - Your All-in-One Trading Strategy Development Platform! KhanBot simplifies the complex world of algorithmic trading by providing an intuitive interface for designing, testing, and deploying trading strategies. Whether you're new to algorithmic trading or an experienced quant, our platform offers comprehensive backtesting capabilities that let you validate your strategies against historical data before risking real capital. With support for multiple technical indicators like MACD, Bollinger Bands, and SuperTrend, along with versatile market making strategies, KhanBot empowers traders to transform their trading ideas into well-tested, data-driven strategies. Our user-friendly dashboard provides clear visualizations of performance metrics, risk analytics, and detailed trade breakdowns, making it easier than ever to refine your trading approach.")


auth_system()
main()
