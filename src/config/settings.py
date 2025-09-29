"""
Configuration management for MCP servers
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables"""
    
    # BB Finance API Configuration
    BB_FINANCE_API_KEY: str = os.getenv("BB_FINANCE_API_KEY", "")
    BB_FINANCE_BASE_URL: str = os.getenv("BB_FINANCE_BASE_URL", "https://bb-finance.p.rapidapi.com/market/get-compact")
    BB_FINANCE_CHART_URL: str = os.getenv("BB_FINANCE_CHART_URL", "https://bb-finance.p.rapidapi.com/market/get-price-chart")
    
    # Pinecone Configuration
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_DEFAULT_INDEX: str = os.getenv("PINECONE_DEFAULT_INDEX", "mcp-vectors")
    PINECONE_DEFAULT_DIMENSION: int = int(os.getenv("PINECONE_DEFAULT_DIMENSION", "384"))
    PINECONE_DEFAULT_METRIC: str = os.getenv("PINECONE_DEFAULT_METRIC", "cosine")
    PINECONE_CLOUD: str = os.getenv("PINECONE_CLOUD", "aws")
    PINECONE_REGION: str = os.getenv("PINECONE_REGION", "us-east-1")
    
    # Embedding Model Configuration
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Server Configuration
    SERVER_HOST: str = os.getenv("SERVER_HOST", "localhost")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required environment variables are set"""
        required_vars = [
            ("BB_FINANCE_API_KEY", cls.BB_FINANCE_API_KEY),
            ("PINECONE_API_KEY", cls.PINECONE_API_KEY),
        ]
        
        missing_vars = []
        for var_name, var_value in required_vars:
            if not var_value:
                missing_vars.append(var_name)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True

# Global settings instance
settings = Settings()
