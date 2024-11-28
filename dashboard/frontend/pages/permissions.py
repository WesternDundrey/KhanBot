from st_pages import Page, Section


def main_page():
    return [Page("main.py", "KhanBot Dashboard", "📊")]


def public_pages():
    return [
        Section("Backtest/Config", "🎛️"),
        Page("frontend/pages/config/grid_strike/app.py", "Grid Strike", "🎳"),
        Page("frontend/pages/config/pmm_simple/app.py", "Pure Market Maker", "🪙"),
        Page("frontend/pages/config/pmm_dynamic/app.py", "Dynamic Market Maker", "💵"),
        Page("frontend/pages/config/dman_maker_v2/app.py", "Prime Market Maker", "🤑"),
        Page("frontend/pages/config/bollinger_v1/app.py", "Bollinger", "📈"),
        Page("frontend/pages/config/macd_bb_v1/app.py", "MACD_BB V1", "📊"),
        Page("frontend/pages/config/supertrend_v1/app.py", "SuperTrend V1", "👨‍🔬"),
        Page("frontend/pages/config/xemm_controller/app.py", "XEMM Controller", "⚡️"),
        Section("Data", "💾"),
        Page("frontend/pages/data/download_candles/app.py", "Download Candles", "💹"),
    ]
