# MCP Server 

A comprehensive demonstration of Model Context Protocol (MCP) servers showcasing real-world integrations with PostgreSQL, financial data APIs, and vector databases.

## 🚀 Overview

This project contains 2 distinct MCP servers that demonstrate different types of integrations:

1. **Share Price MCP Server** - Real-time financial data and market analysis
2. **Pinecone Vector Database MCP Server** - Vector storage and semantic search capabilities

## 📋 Prerequisites

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- API keys for external services (see Configuration section)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd mcp-server-demo-test
   ```

2. **Install dependencies using uv:**
   ```bash
   uv sync
   ```

3. **Set up environment variables:**
   ```bash
   # For Pinecone integration
   export PINECONE_API_KEY="your_pinecone_api_key"
   
   # For embedding model (optional, defaults to all-MiniLM-L6-v2)
   export EMBEDDING_MODEL="all-MiniLM-L6-v2"
   ```

## 🔧 Configuration


### Share Price Server
Uses BB Finance API with the following configuration:
- API Key: ``
- Base URL: `https://bb-finance.p.rapidapi.com/market/get-compact`
- Chart URL: `https://bb-finance.p.rapidapi.com/market/get-price-chart`

### Pinecone Server
Requires a Pinecone API key and uses the following defaults:
- Default Index: `mcp-vectors`
- Default Dimension: `384`
- Default Metric: `cosine`
- Cloud: `AWS us-east-1`

## 🚀 Running the Servers

### 1. PostgreSQL MCP Server
```bash
python main.py
```

**Available Tools:**
- `query_postgres(sql: str)` - Execute SQL queries on PostgreSQL database

**Example Usage:**
```python
# Get all accounts
query_postgres("SELECT * FROM accounts LIMIT 5;")
```

### 2. Share Price MCP Server
```bash
python mcp_share_price_server.py
```

**Available Tools:**

#### `get_share_price(symbol: str)`
Get real-time share price and market data for a stock.

**Parameters:**
- `symbol`: Stock symbol (e.g., 'aapl:us', 'tsla:us', 'msft:us')

**Example:**
```python
get_share_price("aapl:us")
```

#### `get_price_chart_analysis(symbol: str, interval: str = "m3")`
Get detailed price chart analysis with trend, volatility, and key levels.

**Parameters:**
- `symbol`: Stock symbol
- `interval`: Time period (d1|d3|ytd|m1|m3|m6|y1|y5)

**Example:**
```python
get_price_chart_analysis("tsla:us", "m6")
```

#### `compare_stock_performance(symbols: List[str], interval: str = "m3")`
Compare performance of multiple stocks over a specified time period.

**Parameters:**
- `symbols`: List of stock symbols to compare
- `interval`: Time period for comparison

**Example:**
```python
compare_stock_performance(["aapl:us", "tsla:us", "msft:us"], "m3")
```

#### `analyze_stock_volatility(symbol: str, interval: str = "m1")`
Analyze stock volatility and price swings over a specified period.

**Parameters:**
- `symbol`: Stock symbol
- `interval`: Time period for analysis

**Example:**
```python
analyze_stock_volatility("aapl:us", "m1")
```

#### `compare_stocks(symbols: List[str])`
Compare multiple stocks side by side.

**Parameters:**
- `symbols`: Array of stock symbols to compare

**Example:**
```python
compare_stocks(["aapl:us", "tsla:us", "googl:us"])
```

#### `get_market_summary(stocks: Optional[List[str]] = None)`
Get market summary for popular stocks.

**Parameters:**
- `stocks`: Optional list of specific stocks (defaults to popular stocks)

**Example:**
```python
get_market_summary(["aapl:us", "tsla:us", "msft:us", "googl:us"])
```

**Available Resources:**
- `share://price-data` - Real-time share price information resource

### 3. Pinecone Vector Database MCP Server
```bash
python pinecone-connect.py
```

**Available Tools:**

#### `list_indexes()`
List all Pinecone indexes.

**Example:**
```python
list_indexes()
```

#### `upsert_vectors(index_name: str, texts: List[str], metadata: Optional[List[Dict]] = None, ids: Optional[List[str]] = None)`
Insert or update vectors in an index.

**Parameters:**
- `index_name`: Target index name
- `texts`: Text content to embed and store
- `metadata`: Optional metadata for each text
- `ids`: Optional custom IDs (auto-generated if not provided)

**Example:**
```python
upsert_vectors(
    "my-vectors",
    ["Machine learning is fascinating", "AI will change the world"],
    [{"category": "tech"}, {"category": "future"}],
    ["doc1", "doc2"]
)
```

#### `semantic_search(index_name: str, query: str, top_k: int = 5, filter: Optional[Dict] = None, include_metadata: bool = True)`
Perform semantic search in an index.

**Parameters:**
- `index_name`: Index to search in
- `query`: Search query text
- `top_k`: Number of results to return
- `filter`: Optional metadata filter
- `include_metadata`: Include metadata in results

**Example:**
```python
semantic_search("my-vectors", "artificial intelligence", 3)
```

#### `get_vectors(index_name: str, ids: List[str], include_metadata: bool = True)`
Retrieve specific vectors by ID.

**Parameters:**
- `index_name`: Index name
- `ids`: Vector IDs to retrieve
- `include_metadata`: Include metadata

**Example:**
```python
get_vectors("my-vectors", ["doc1", "doc2"])
```
#### `index_stats(index_name: str)`
Get index statistics and information.

**Parameters:**
- `index_name`: Index name

**Example:**
```python
index_stats("my-vectors")
```

**Available Resources:**
- `pinecone://indexes` - List all Pinecone indexes
- `pinecone://index/{index_name}` - Get statistics for a specific index

## 📊 Use Cases

### Financial Analysis
- **Real-time Market Data**: Get current stock prices, volume, and market metrics
- **Technical Analysis**: Analyze price trends, volatility, and support/resistance levels
- **Portfolio Comparison**: Compare performance across multiple stocks
- **Risk Assessment**: Evaluate stock volatility and risk metrics

### Vector Database Operations
- **Semantic Search**: Find similar content using natural language queries
- **Document Storage**: Store and retrieve text documents with metadata
- **Knowledge Management**: Build searchable knowledge bases
- **Recommendation Systems**: Create content recommendation engines

### Database Integration
- **Data Querying**: Execute SQL queries on PostgreSQL databases
- **Data Analysis**: Perform complex database operations
- **Reporting**: Generate reports from database data

## 🔍 Example Workflows

### 1. Stock Market Analysis Workflow
```python
# Get current price
price_data = get_share_price("aapl:us")

# Analyze 3-month performance
chart_analysis = get_price_chart_analysis("aapl:us", "m3")

# Compare with competitors
comparison = compare_stock_performance(["aapl:us", "msft:us", "googl:us"], "m3")

# Check volatility
volatility = analyze_stock_volatility("aapl:us", "m1")
```

### 2. Vector Database Workflow
```python
# Create an index
create_index("documents", 384, "cosine")

# Add documents
upsert_vectors(
    "documents",
    ["Python is a programming language", "Machine learning uses algorithms"],
    [{"type": "programming"}, {"type": "ai"}]
)

# Search for similar content
results = semantic_search("documents", "programming languages", 3)

# Get statistics
stats = index_stats("documents")
```

## 🛡️ Security Notes

- **API Keys**: The project contains hardcoded API keys for demonstration purposes. In production, use environment variables or secure key management.
- **Database Credentials**: PostgreSQL credentials are hardcoded and should be moved to environment variables.
- **Rate Limiting**: Be aware of API rate limits when using external services.

## 📝 Dependencies

- `httpx>=0.28.1` - HTTP client for API requests
- `mcp[cli]>=1.15.0` - Model Context Protocol framework
- `pinecone>=7.3.0` - Pinecone vector database client
- `psycopg2-binary>=2.9.10` - PostgreSQL adapter
- `sentence-transformers>=5.1.1` - Text embedding models
- `torch>=2.8.0` - PyTorch for ML models
- `transformers>=4.56.2` - Hugging Face transformers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for demonstration purposes. Please ensure you have appropriate licenses for any external services used.

## 🆘 Support

For issues and questions:
1. Check the existing issues
2. Create a new issue with detailed description
3. Include error logs and system information

## 🔄 Updates

- **v0.1.0**: Initial release with PostgreSQL, Share Price, and Pinecone MCP servers
- Features real-time financial data, vector database operations, and database integration
- Supports multiple time intervals for financial analysis
- Includes comprehensive error handling and logging
