# MCP Server

A production-ready repository that connects to Model Context Protocol (MCP) servers showcasing real-world integrations with financial data APIs and vector databases.

## 🚀 Overview

This project contains 2 distinct MCP servers that demonstrate different types of integrations:

1. **Share Price MCP Server** - Real-time financial data and market analysis
2. **Pinecone Vector Database MCP Server** - Vector storage and semantic search capabilities

## 📁 Project Structure

```
mcp-server-demo/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # Configuration management
│   └── mcp_servers/
│       ├── __init__.py
│       ├── share_price_server.py    # Share price MCP server
│       └── pinecone_server.py       # Pinecone MCP server
├── tests/                        # Test files
├── docs/                         # Documentation
├── main.py                       # Main entry point
├── run_share_price.py           # Share price server launcher
├── run_pinecone.py              # Pinecone server launcher
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project configuration
├── Dockerfile                   # Docker configuration
├── docker-compose.yml          # Docker Compose setup
├── deploy.sh                    # Production deployment script
└── setup_dev.sh                # Development setup script
```

## 📋 Prerequisites

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager (for development)
- Docker and Docker Compose (for production)
- API keys for external services (see Configuration section)

## 🛠️ Quick Start

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd mcp-server-demo-test
   ```

2. **Run the development setup:**
   ```bash
   ./setup_dev.sh
   ```

3. **Configure environment variables:**
   ```bash
   # Edit .env file with your API keys
   nano .env
   ```

4. **Run individual servers:**
   ```bash
   # Share Price Server
   python run_share_price.py
   
   # Pinecone Server
   python run_pinecone.py
   
   # Or use the main launcher
   python main.py share-price
   python main.py pinecone
   ```

### Production Deployment

1. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your production API keys
   ```

2. **Deploy with Docker:**
   ```bash
   ./deploy.sh
   ```

3. **Or manually with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

## 🔧 Configuration

All configuration is managed through environment variables. Copy `.env.example` to `.env` and configure your settings:

### Environment Variables

```bash
# BB Finance API Configuration
BB_FINANCE_API_KEY=your_bb_finance_api_key_here
BB_FINANCE_BASE_URL=https://bb-finance.p.rapidapi.com/market/get-compact
BB_FINANCE_CHART_URL=https://bb-finance.p.rapidapi.com/market/get-price-chart

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_DEFAULT_INDEX=mcp-vectors
PINECONE_DEFAULT_DIMENSION=384
PINECONE_DEFAULT_METRIC=cosine
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1

# Embedding Model Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Logging Configuration
LOG_LEVEL=INFO

# Server Configuration
SERVER_HOST=localhost
SERVER_PORT=8000
```

### Share Price Server
Uses BB Finance API with configurable endpoints and API keys.

### Pinecone Server
Requires a Pinecone API key with configurable index settings and cloud region.

## 🚀 Running the Servers

### Development Mode

#### Share Price MCP Server
```bash
# Using individual launcher
python run_share_price.py

# Using main launcher
python main.py share-price
```

#### Pinecone MCP Server
```bash
# Using individual launcher
python run_pinecone.py

# Using main launcher
python main.py pinecone
```

### Production Mode

#### Using Docker Compose
```bash
# Start both servers
docker-compose up -d

# Start individual servers
docker-compose up -d share-price-server
docker-compose up -d pinecone-server
```

#### Using Docker
```bash
# Build and run individual containers
docker build -t mcp-server .
docker run -p 8001:8000 --env-file .env mcp-server python run_share_price.py
docker run -p 8002:8000 --env-file .env mcp-server python run_pinecone.py
```

### 1. Share Price MCP Server

**Architecture**
<img width="1009" height="647" alt="image" src="https://github.com/user-attachments/assets/7df7f35c-209b-4d1a-9046-210069e67efa" />


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

### 2. Pinecone Vector Database MCP Server
```bash
# Development
python run_pinecone.py

# Production
docker-compose up -d pinecone-server
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

## 🚀 Production Deployment

### Docker Deployment

The project includes Docker and Docker Compose configurations for easy production deployment:

```bash
# Quick deployment
./deploy.sh

# Manual deployment
docker-compose up -d
```

### Environment Setup

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Configure your API keys:**
   ```bash
   nano .env
   ```

3. **Deploy:**
   ```bash
   ./deploy.sh
   ```

### Monitoring

- **Logs:** `docker-compose logs -f`
- **Status:** `docker-compose ps`
- **Restart:** `docker-compose restart`

### Scaling

To run multiple instances:

```bash
# Scale share price server
docker-compose up -d --scale share-price-server=3

# Scale pinecone server
docker-compose up -d --scale pinecone-server=2
```

## 📝 Dependencies

- `httpx>=0.28.1` - HTTP client for API requests
- `mcp[cli]>=1.15.0` - Model Context Protocol framework
- `pinecone>=7.3.0` - Pinecone vector database client
- `psycopg2-binary>=2.9.10` - PostgreSQL adapter
- `sentence-transformers>=5.1.1` - Text embedding models
- `torch>=2.8.0` - PyTorch for ML models
- `transformers>=4.56.2` - Hugging Face transformers
- `python-dotenv>=1.0.0` - Environment variable management


## 🔄 Updates

- **v0.1.0**: Initial release with Share Price API, and Pinecone MCP servers
- Features real-time financial data, vector database operations, and database integration
- Supports multiple time intervals for financial analysis
- Includes comprehensive error handling and logging

## 🔄 Demo Video
[![Watch the video](https://img.youtube.com/vi/bFzy1jA4Ucs/0.jpg)](https://youtu.be/bFzy1jA4Ucs)
