# Deployment Guide

## Production Deployment

### Prerequisites

- Docker and Docker Compose installed
- API keys for BB Finance and Pinecone
- Environment variables configured

### Quick Start

1. **Clone and configure:**
   ```bash
   git clone <repository-url>
   cd mcp-server-demo-test
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Deploy:**
   ```bash
   ./deploy.sh
   ```

### Manual Deployment

1. **Build images:**
   ```bash
   docker-compose build
   ```

2. **Start services:**
   ```bash
   docker-compose up -d
   ```

3. **Check status:**
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

### Environment Variables

Required environment variables:

- `BB_FINANCE_API_KEY`: Your BB Finance API key
- `PINECONE_API_KEY`: Your Pinecone API key

Optional environment variables:

- `LOG_LEVEL`: Logging level (default: INFO)
- `PINECONE_DEFAULT_INDEX`: Default index name (default: mcp-vectors)
- `EMBEDDING_MODEL`: Embedding model name (default: all-MiniLM-L6-v2)

### Scaling

To scale individual services:

```bash
# Scale share price server to 3 instances
docker-compose up -d --scale share-price-server=3

# Scale pinecone server to 2 instances
docker-compose up -d --scale pinecone-server=2
```

### Monitoring

- **View logs:** `docker-compose logs -f [service-name]`
- **Check status:** `docker-compose ps`
- **Restart service:** `docker-compose restart [service-name]`
- **Stop all:** `docker-compose down`

### Troubleshooting

1. **Check logs for errors:**
   ```bash
   docker-compose logs [service-name]
   ```

2. **Verify environment variables:**
   ```bash
   docker-compose config
   ```

3. **Restart services:**
   ```bash
   docker-compose restart
   ```
