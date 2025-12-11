"""
Yahoo Finance MCP Server - Streamlit App for Databricks
Interactive UI to test all MCP tools
"""

import asyncio
import json
import streamlit as st
import pandas as pd
from datetime import datetime
from server import (
    get_historical_stock_prices,
    get_stock_info,
    get_yahoo_finance_news,
    get_stock_actions,
    get_financial_statement,
    get_holder_info,
    get_option_expiration_dates,
    get_option_chain,
    get_recommendations
)

# Page configuration
st.set_page_config(
    page_title="Yahoo Finance MCP Server",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        opacity: 0.9;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to run async functions
def run_async(coro):
    """Run async function in sync context"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

# Main header
st.title("📈 Yahoo Finance MCP Server")
st.markdown("### Custom MCP Server on Databricks - Test Your Financial Data Tools")
st.markdown("---")

# Sidebar for tool selection
st.sidebar.title("🛠️ Available Tools")
st.sidebar.markdown("Select a tool to test:")

tool_options = {
    "📊 Historical Stock Prices": "get_historical_stock_prices",
    "💼 Stock Information": "get_stock_info",
    "📰 Yahoo Finance News": "get_yahoo_finance_news",
    "💰 Stock Actions (Dividends/Splits)": "get_stock_actions",
    "📑 Financial Statements": "get_financial_statement",
    "👥 Holder Information": "get_holder_info",
    "📅 Option Expiration Dates": "get_option_expiration_dates",
    "📈 Option Chain": "get_option_chain",
    "⭐ Analyst Recommendations": "get_recommendations"
}

selected_tool_name = st.sidebar.selectbox(
    "Choose a tool:",
    list(tool_options.keys())
)

selected_tool = tool_options[selected_tool_name]

# Tool descriptions
tool_descriptions = {
    "get_historical_stock_prices": "Get historical OHLCV (Open, High, Low, Close, Volume) data for any stock with customizable time periods and intervals.",
    "get_stock_info": "Get comprehensive stock information including current price, market cap, financial metrics, company details, and more.",
    "get_yahoo_finance_news": "Fetch the latest news articles related to a specific stock from Yahoo Finance.",
    "get_stock_actions": "Retrieve historical dividend payments and stock split information.",
    "get_financial_statement": "Access detailed financial statements including income statements, balance sheets, and cash flow statements (annual or quarterly).",
    "get_holder_info": "Get information about major holders, institutional investors, mutual funds, and insider transactions.",
    "get_option_expiration_dates": "Fetch all available options expiration dates for a given stock.",
    "get_option_chain": "Get detailed option chain data for calls or puts with a specific expiration date.",
    "get_recommendations": "View analyst recommendations, upgrades, and downgrades for stocks."
}

st.sidebar.markdown("---")
st.sidebar.info(tool_descriptions[selected_tool])

# Main content area
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("🔧 Parameters")
    
    # Common parameter: Ticker
    ticker = st.text_input("Stock Ticker Symbol", value="AAPL", help="Enter a valid stock ticker symbol (e.g., AAPL, TSLA, MSFT)")
    
    # Tool-specific parameters
    if selected_tool == "get_historical_stock_prices":
        period = st.selectbox(
            "Time Period",
            ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
            index=2
        )
        interval = st.selectbox(
            "Interval",
            ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"],
            index=8
        )
    
    elif selected_tool == "get_financial_statement":
        financial_type = st.selectbox(
            "Financial Statement Type",
            ["income_stmt", "quarterly_income_stmt", "balance_sheet", "quarterly_balance_sheet", "cashflow", "quarterly_cashflow"]
        )
    
    elif selected_tool == "get_holder_info":
        holder_type = st.selectbox(
            "Holder Type",
            ["major_holders", "institutional_holders", "mutualfund_holders", "insider_transactions", "insider_purchases", "insider_roster_holders"]
        )
    
    elif selected_tool == "get_option_chain":
        expiration_date = st.text_input(
            "Expiration Date (YYYY-MM-DD)",
            value="2025-12-19",
            help="First use 'Option Expiration Dates' tool to get valid dates"
        )
        option_type = st.selectbox("Option Type", ["calls", "puts"])
    
    elif selected_tool == "get_recommendations":
        recommendation_type = st.selectbox(
            "Recommendation Type",
            ["recommendations", "upgrades_downgrades"]
        )
        months_back = st.number_input("Months Back", min_value=1, max_value=60, value=12)
    
    st.markdown("---")
    execute_button = st.button("🚀 Execute Tool", use_container_width=True)

with col2:
    st.subheader("📊 Results")
    
    if execute_button:
        with st.spinner(f"Fetching data for {ticker}..."):
            try:
                result = None
                
                # Execute the selected tool
                if selected_tool == "get_historical_stock_prices":
                    result = run_async(get_historical_stock_prices(ticker, period, interval))
                
                elif selected_tool == "get_stock_info":
                    result = run_async(get_stock_info(ticker))
                
                elif selected_tool == "get_yahoo_finance_news":
                    result = run_async(get_yahoo_finance_news(ticker))
                
                elif selected_tool == "get_stock_actions":
                    result = run_async(get_stock_actions(ticker))
                
                elif selected_tool == "get_financial_statement":
                    result = run_async(get_financial_statement(ticker, financial_type))
                
                elif selected_tool == "get_holder_info":
                    result = run_async(get_holder_info(ticker, holder_type))
                
                elif selected_tool == "get_option_expiration_dates":
                    result = run_async(get_option_expiration_dates(ticker))
                
                elif selected_tool == "get_option_chain":
                    result = run_async(get_option_chain(ticker, expiration_date, option_type))
                
                elif selected_tool == "get_recommendations":
                    result = run_async(get_recommendations(ticker, recommendation_type, int(months_back)))
                
                # Display results
                if result:
                    st.success(f"✅ Successfully retrieved data for {ticker}")
                    
                    # Try to parse and display as formatted data
                    try:
                        if isinstance(result, str) and result.startswith('[') or result.startswith('{'):
                            data = json.loads(result)
                            
                            # Display as DataFrame if it's a list of dicts
                            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                                df = pd.DataFrame(data)
                                st.dataframe(df, use_container_width=True, height=400)
                                
                                # Download button
                                csv = df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download CSV",
                                    data=csv,
                                    file_name=f"{ticker}_{selected_tool}_{datetime.now().strftime('%Y%m%d')}.csv",
                                    mime="text/csv"
                                )
                            else:
                                # Display as JSON
                                st.json(data)
                        else:
                            # Display as text (e.g., news)
                            st.text_area("Result", result, height=400)
                    
                    except json.JSONDecodeError:
                        # If not JSON, display as text
                        st.text_area("Result", result, height=400)
                    
                    # Show raw JSON
                    with st.expander("📄 View Raw JSON"):
                        st.code(result, language="json")
                
                else:
                    st.warning("No data returned")
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.code(str(e))

# Footer with stats
st.markdown("---")
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.metric("Available Tools", "9")

with col_b:
    st.metric("Data Source", "Yahoo Finance")

with col_c:
    st.metric("Status", "🟢 Active")

# Information section
with st.expander("ℹ️ About This App"):
    st.markdown("""
    ### Yahoo Finance MCP Server
    
    This is a Model Context Protocol (MCP) server that provides comprehensive financial data from Yahoo Finance.
    
    **Available Data:**
    - 📊 Historical stock prices with multiple timeframes
    - 💼 Real-time stock information and metrics
    - 📰 Latest financial news
    - 💰 Dividend and split history
    - 📑 Financial statements (income, balance sheet, cash flow)
    - 👥 Institutional and insider holdings
    - 📈 Options data and chains
    - ⭐ Analyst recommendations and ratings
    
    **Tech Stack:**
    - Backend: FastMCP + yfinance
    - UI: Streamlit
    - Deployment: Databricks Apps
    
    **Note:** Data is provided by Yahoo Finance and is subject to their terms of service and rate limits.
    """)

# Quick tips
with st.expander("💡 Quick Tips"):
    st.markdown("""
    1. **Try different tickers**: AAPL, MSFT, GOOGL, TSLA, AMZN, META, NVDA, etc.
    2. **For option chains**: First use "Option Expiration Dates" to find valid dates
    3. **Financial statements**: Use quarterly versions for more recent data
    4. **Historical data**: Shorter periods allow for finer intervals (1m, 5m, etc.)
    5. **News**: Some tickers may have limited news availability
    """)

