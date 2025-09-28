#!/usr/bin/env python3
"""
MCP Server for fetching share price data from BB Finance API using FastMCP
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
import httpx

# FastMCP imports
try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    print(f"FastMCP import error: {e}")
    print("Please install MCP with: uv add mcp")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("share-price-server")

# API configuration
API_KEY = "bb83738c78msh922834f4b8a9336p1a9e66jsna220fb24400d"
BASE_URL = "https://bb-finance.p.rapidapi.com/market/get-compact"
CHART_URL = "https://bb-finance.p.rapidapi.com/market/get-price-chart"
HEADERS = {
    'x-rapidapi-host': 'bb-finance.p.rapidapi.com',
    'x-rapidapi-key': API_KEY
}

# Create FastMCP server instance
mcp = FastMCP("Share Price Server")

async def fetch_share_price(symbol: str) -> Optional[Dict[str, Any]]:
    """Fetch share price data from BB Finance API"""
    try:
        async with httpx.AsyncClient() as client:
            params = {"id": symbol}
            response = await client.get(
                BASE_URL,
                params=params,
                headers=HEADERS,
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                result = data.get("result", {})
                
                # Get the first (and usually only) stock data
                for key, stock_data in result.items():
                    return stock_data
                
                return None
            else:
                logger.error(f"API request failed with status {response.status_code}: {response.text}")
                return None
                
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {str(e)}")
        return None

async def fetch_price_chart(symbol: str, interval: str = "m3") -> Optional[Dict[str, Any]]:
    """
    Fetch price chart data from BB Finance API
    
    Args:
        symbol: Stock symbol (e.g., 'aapl:us')
        interval: Time interval (d1|d3|ytd|m1|m3|m6|y1|y5)
    
    Returns:
        Chart data with ticks, highs, lows, etc.
    """
    try:
        async with httpx.AsyncClient() as client:
            params = {
                "id": symbol,
                "interval": interval
            }
            response = await client.get(
                CHART_URL,
                params=params,
                headers=HEADERS,
                timeout=15.0
            )
            
            if response.status_code == 200:
                data = response.json()
                result = data.get("result", {})
                
                # Get the first (and usually only) stock data
                for key, stock_data in result.items():
                    return stock_data
                
                return None
            else:
                logger.error(f"Chart API request failed with status {response.status_code}: {response.text}")
                return None
                
    except Exception as e:
        logger.error(f"Error fetching chart data for {symbol}: {str(e)}")
        return None

def format_share_data(data: Dict[str, Any], symbol: str) -> str:
    """Format share price data into readable text"""
    try:
        name = data.get("name", "Unknown")
        last_price = data.get("last", "N/A")
        currency = data.get("currency", "USD")
        net_change = data.get("netChange", "N/A")
        pct_change = data.get("pctChange", "N/A")
        day_high = data.get("dayHigh", "N/A")
        day_low = data.get("dayLow", "N/A")
        year_high = data.get("yearHigh", "N/A")
        year_low = data.get("yearLow", "N/A")
        volume = data.get("volume", "N/A")
        exchange = data.get("exchange", "N/A")
        
        # Format volume with commas
        if isinstance(volume, (int, float)):
            volume = f"{volume:,}"
        
        formatted = f"""
🔸 **{name} ({symbol.upper()})**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **Current Price:** {currency} {last_price}
📈 **Change:** {net_change} ({pct_change}%)
🔄 **Exchange:** {exchange}

📅 **Day Trading Range:**
   • High: {currency} {day_high}
   • Low:  {currency} {day_low}

📆 **52-Week Range:**
   • High: {currency} {year_high}
   • Low:  {currency} {year_low}

📊 **Volume:** {volume}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """.strip()
        
        return formatted
        
    except Exception as e:
        return f"Error formatting data for {symbol}: {str(e)}"

def analyze_price_trend(ticks: List[Dict], symbol: str, interval: str) -> Dict[str, Any]:
    """Analyze price trend from chart data"""
    if not ticks or len(ticks) < 2:
        return {"error": "Insufficient data for trend analysis"}
    
    # Extract closing prices
    prices = [float(tick["close"]) for tick in ticks]
    times = [tick["time"] for tick in ticks]
    
    # Basic statistics
    first_price = prices[0]
    last_price = prices[-1]
    min_price = min(prices)
    max_price = max(prices)
    
    # Calculate returns
    total_return = ((last_price - first_price) / first_price) * 100
    
    # Calculate volatility (standard deviation of returns)
    returns = []
    for i in range(1, len(prices)):
        daily_return = ((prices[i] - prices[i-1]) / prices[i-1]) * 100
        returns.append(daily_return)
    
    volatility = sum((r - (sum(returns) / len(returns))) ** 2 for r in returns) / len(returns)
    volatility = (volatility ** 0.5)
    
    # Determine trend
    trend = "neutral"
    if total_return > 2:
        trend = "uptrend"
    elif total_return < -2:
        trend = "downtrend"
    
    # Calculate support and resistance levels
    price_range = max_price - min_price
    support_level = min_price + (price_range * 0.2)
    resistance_level = max_price - (price_range * 0.2)
    
    return {
        "symbol": symbol,
        "interval": interval,
        "total_return": round(total_return, 2),
        "volatility": round(volatility, 2),
        "trend": trend,
        "first_price": round(first_price, 2),
        "last_price": round(last_price, 2),
        "min_price": round(min_price, 2),
        "max_price": round(max_price, 2),
        "support_level": round(support_level, 2),
        "resistance_level": round(resistance_level, 2),
        "data_points": len(ticks),
        "price_range": round(price_range, 2)
    }

def format_chart_analysis(analysis: Dict[str, Any], symbol: str) -> str:
    """Format chart analysis into readable text"""
    if "error" in analysis:
        return f"❌ {analysis['error']}"
    
    # Map intervals to readable names
    interval_names = {
        "d1": "1 Day", "d3": "3 Days", "m1": "1 Month", 
        "m3": "3 Months", "m6": "6 Months", "ytd": "Year-to-Date",
        "y1": "1 Year", "y5": "5 Years"
    }
    
    interval_name = interval_names.get(analysis["interval"], analysis["interval"])
    
    # Determine trend emoji
    trend_emoji = {
        "uptrend": "📈", "downtrend": "📉", "neutral": "➡️"
    }
    
    trend_icon = trend_emoji.get(analysis["trend"], "➡️")
    return_color = "🟢" if analysis["total_return"] >= 0 else "🔴"
    
    formatted = f"""
{trend_icon} **{symbol.upper()} - {interval_name} Chart Analysis**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **Performance Summary:**
{return_color} Total Return: {analysis['total_return']}%
📉 Volatility: {analysis['volatility']}%
📈 Trend: {analysis['trend'].title()}

💰 **Price Levels:**
🔵 Current: ${analysis['last_price']}
🟢 High: ${analysis['max_price']}
🔴 Low: ${analysis['min_price']}
📏 Range: ${analysis['price_range']}

🎯 **Key Levels:**
🛡️ Support: ${analysis['support_level']}
⚡ Resistance: ${analysis['resistance_level']}

📈 **Data Points:** {analysis['data_points']} price observations

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """.strip()
    
    return formatted

def compare_performance(analyses: List[Dict[str, Any]]) -> str:
    """Compare performance between multiple stocks"""
    if len(analyses) < 2:
        return "Need at least 2 stocks for comparison"
    
    formatted = "📊 **PERFORMANCE COMPARISON**\n"
    formatted += "━" * 60 + "\n\n"
    
    # Sort by total return
    sorted_analyses = sorted(analyses, key=lambda x: x.get("total_return", 0), reverse=True)
    
    for i, analysis in enumerate(sorted_analyses, 1):
        return_color = "🟢" if analysis["total_return"] >= 0 else "🔴"
        trend_emoji = {"uptrend": "📈", "downtrend": "📉", "neutral": "➡️"}
        trend_icon = trend_emoji.get(analysis["trend"], "➡️")
        
        formatted += f"{i}. {return_color} **{analysis['symbol'].upper()}**\n"
        formatted += f"   Return: {analysis['total_return']}% | Volatility: {analysis['volatility']}% {trend_icon}\n"
        formatted += f"   Range: ${analysis['min_price']} - ${analysis['max_price']}\n\n"
    
    return formatted
    """Format comparison data for multiple stocks"""
    try:
        formatted = "📊 **STOCK COMPARISON**\n"
        formatted += "━" * 60 + "\n\n"
        
        for symbol, data in comparison_data:
            name = data.get("name", "Unknown")
            last_price = data.get("last", "N/A")
            currency = data.get("currency", "USD")
            pct_change = data.get("pctChange", "N/A")
            
            # Determine if change is positive or negative
            change_indicator = "🔴" if str(pct_change).startswith("-") else "🟢"
            
            formatted += f"{change_indicator} **{name} ({symbol.upper()})**\n"
            formatted += f"   Price: {currency} {last_price} ({pct_change}%)\n\n"
        
        return formatted
        
    except Exception as e:
        return f"Error formatting comparison: {str(e)}"

def format_market_summary(summary_data: List[tuple]) -> str:
    """Format market summary for multiple stocks"""
    try:
        formatted = "📈 **MARKET SUMMARY**\n"
        formatted += "━" * 50 + "\n\n"
        
        gainers = []
        losers = []
        
        for symbol, data in summary_data:
            name = data.get("name", "Unknown")
            last_price = data.get("last", "N/A")
            currency = data.get("currency", "USD")
            pct_change = data.get("pctChange", "N/A")
            net_change = data.get("netChange", "N/A")
            
            stock_info = {
                "symbol": symbol.upper(),
                "name": name,
                "price": f"{currency} {last_price}",
                "change": f"{net_change} ({pct_change}%)"
            }
            
            if str(pct_change).startswith("-"):
                losers.append(stock_info)
            else:
                gainers.append(stock_info)
        
        if gainers:
            formatted += "🟢 **TOP GAINERS:**\n"
            for stock in gainers:
                formatted += f"   • {stock['name']} ({stock['symbol']}): {stock['price']} | +{stock['change']}\n"
            formatted += "\n"
        
        if losers:
            formatted += "🔴 **DECLINERS:**\n"
            for stock in losers:
                formatted += f"   • {stock['name']} ({stock['symbol']}): {stock['price']} | {stock['change']}\n"
            formatted += "\n"
        
        return formatted
        
    except Exception as e:
        return f"Error formatting market summary: {str(e)}"

# Register tools using FastMCP decorators
@mcp.tool()
async def get_share_price(symbol: str) -> str:
    """
    Get real-time share price and market data for a stock
    
    Args:
        symbol: Stock symbol (e.g., 'aapl:us', 'tsla:us', 'msft:us')
    
    Returns:
        Formatted share price information
    """
    if not symbol:
        return "Error: Symbol is required"
    
    data = await fetch_share_price(symbol.lower())
    if data:
        return format_share_data(data, symbol)
    else:
        return f"Error: Could not fetch data for symbol {symbol}"

@mcp.tool()
async def get_price_chart_analysis(symbol: str, interval: str = "m3") -> str:
    """
    Get price chart analysis with trend, volatility, and key levels
    
    Args:
        symbol: Stock symbol (e.g., 'aapl:us', 'tsla:us', 'msft:us')
        interval: Time period (d1|d3|ytd|m1|m3|m6|y1|y5) - defaults to 3 months
    
    Returns:
        Detailed chart analysis with trend, volatility, support/resistance levels
    """
    valid_intervals = ["d1", "d3", "ytd", "m1", "m3", "m6", "y1", "y5"]
    if interval not in valid_intervals:
        return f"Error: Invalid interval. Use one of: {', '.join(valid_intervals)}"
    
    chart_data = await fetch_price_chart(symbol.lower(), interval)
    if not chart_data:
        return f"Error: Could not fetch chart data for {symbol}"
    
    ticks = chart_data.get("ticks", [])
    if not ticks:
        return f"Error: No chart data available for {symbol}"
    
    analysis = analyze_price_trend(ticks, symbol, interval)
    return format_chart_analysis(analysis, symbol)

@mcp.tool()
async def compare_stock_performance(symbols: List[str], interval: str = "m3") -> str:
    """
    Compare performance of multiple stocks over a specified time period
    
    Args:
        symbols: List of stock symbols to compare (e.g., ['aapl:us', 'tsla:us'])
        interval: Time period (d1|d3|ytd|m1|m3|m6|y1|y5) - defaults to 3 months
    
    Returns:
        Comparative analysis showing relative performance, volatility, and trends
    """
    if not symbols or len(symbols) < 2:
        return "Error: Need at least 2 symbols for comparison"
    
    valid_intervals = ["d1", "d3", "ytd", "m1", "m3", "m6", "y1", "y5"]
    if interval not in valid_intervals:
        return f"Error: Invalid interval. Use one of: {', '.join(valid_intervals)}"
    
    analyses = []
    for symbol in symbols:
        chart_data = await fetch_price_chart(symbol.lower(), interval)
        if chart_data and chart_data.get("ticks"):
            analysis = analyze_price_trend(chart_data["ticks"], symbol, interval)
            if "error" not in analysis:
                analyses.append(analysis)
    
    if not analyses:
        return "Error: Could not fetch chart data for any of the provided symbols"
    
    return compare_performance(analyses)

@mcp.tool()
async def analyze_stock_volatility(symbol: str, interval: str = "m1") -> str:
    """
    Analyze stock volatility and price swings over a specified period
    
    Args:
        symbol: Stock symbol (e.g., 'aapl:us', 'tsla:us')
        interval: Time period (d1|d3|ytd|m1|m3|m6|y1|y5) - defaults to 1 month
    
    Returns:
        Detailed volatility analysis with price swings and risk metrics
    """
    valid_intervals = ["d1", "d3", "ytd", "m1", "m3", "m6", "y1", "y5"]
    if interval not in valid_intervals:
        return f"Error: Invalid interval. Use one of: {', '.join(valid_intervals)}"
    
    chart_data = await fetch_price_chart(symbol.lower(), interval)
    if not chart_data:
        return f"Error: Could not fetch chart data for {symbol}"
    
    ticks = chart_data.get("ticks", [])
    if not ticks:
        return f"Error: No chart data available for {symbol}"
    
    analysis = analyze_price_trend(ticks, symbol, interval)
    
    if "error" in analysis:
        return f"❌ {analysis['error']}"
    
    # Additional volatility insights
    prices = [float(tick["close"]) for tick in ticks]
    
    # Calculate largest single-day moves
    daily_changes = []
    for i in range(1, len(prices)):
        change_pct = ((prices[i] - prices[i-1]) / prices[i-1]) * 100
        daily_changes.append(abs(change_pct))
    
    max_daily_change = max(daily_changes) if daily_changes else 0
    avg_daily_change = sum(daily_changes) / len(daily_changes) if daily_changes else 0
    
    # Volatility classification
    vol_level = "Low"
    if analysis["volatility"] > 5:
        vol_level = "High"
    elif analysis["volatility"] > 2:
        vol_level = "Moderate"
    
    interval_names = {
        "d1": "1 Day", "d3": "3 Days", "m1": "1 Month", 
        "m3": "3 Months", "m6": "6 Months", "ytd": "Year-to-Date",
        "y1": "1 Year", "y5": "5 Years"
    }
    
    interval_name = interval_names.get(interval, interval)
    
    formatted = f"""
⚡ **{symbol.upper()} - Volatility Analysis ({interval_name})**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **Volatility Metrics:**
🎯 Overall Volatility: {analysis['volatility']}% ({vol_level})
📈 Largest Single Move: {max_daily_change:.2f}%
📊 Average Daily Move: {avg_daily_change:.2f}%

💰 **Price Range Analysis:**
🔴 Lowest: ${analysis['min_price']}
🟢 Highest: ${analysis['max_price']}
📏 Total Range: {((analysis['max_price'] - analysis['min_price']) / analysis['min_price'] * 100):.1f}%

🎯 **Risk Assessment:**
{'🟢 Low Risk' if vol_level == 'Low' else '🟡 Moderate Risk' if vol_level == 'Moderate' else '🔴 High Risk'} - {vol_level} volatility stock

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """.strip()
    
    return formatted

@mcp.tool()
async def compare_stocks(symbols: List[str]) -> str:
    """
    Compare multiple stocks side by side
    
    Args:
        symbols: Array of stock symbols to compare (e.g., ['aapl:us', 'tsla:us'])
    
    Returns:
        Formatted comparison of multiple stocks
    """
    if not symbols:
        return "Error: At least one symbol is required"
    
    comparison_data = []
    for symbol in symbols:
        data = await fetch_share_price(symbol.lower())
        if data:
            comparison_data.append((symbol, data))
    
    if comparison_data:
        return format_comparison(comparison_data)
    else:
        return "Error: Could not fetch data for any of the provided symbols"

@mcp.tool()
async def get_market_summary(stocks: Optional[List[str]] = None) -> str:
    """
    Get market summary for popular stocks
    
    Args:
        stocks: Optional list of specific stocks, defaults to popular stocks
    
    Returns:
        Formatted market summary with gainers and losers
    """
    if stocks is None:
        stocks = ["aapl:us", "tsla:us", "msft:us", "googl:us"]
    
    summary_data = []
    for stock in stocks:
        data = await fetch_share_price(stock.lower())
        if data:
            summary_data.append((stock, data))
    
    if summary_data:
        return format_market_summary(summary_data)
    else:
        return "Error: Could not fetch market summary data"

# Add a resource
@mcp.resource("share://price-data")
async def get_price_data_resource() -> str:
    """Real-time share price information from BB Finance API"""
    return """
    Available share price data resource.
    
    Tools available:
    - get_share_price(symbol): Get detailed price data for a stock
    - compare_stocks(symbols): Compare multiple stocks
    - get_market_summary(stocks): Get market overview
    
    Example symbols: aapl:us, tsla:us, msft:us, googl:us
    """

if __name__ == "__main__":
    # Run the server
    mcp.run()