#!/usr/bin/env python3
"""
FastMCP Server for Pinecone Vector Database Operations
Provides semantic search, vector storage, and embedding management capabilities
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional, Union
import uuid
from datetime import datetime

# Third-party imports
import httpx
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# FastMCP imports
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pinecone-fastmcp-server")

# Create FastMCP server instance
mcp = FastMCP("Pinecone Vector Database Server")

# Global variables for Pinecone setup
pinecone_client = None
embedding_model = None
default_index_name = "mcp-vectors"
default_dimension = 384

def initialize_pinecone():
    """Initialize Pinecone client and embedding model"""
    global pinecone_client, embedding_model
    
    # Initialize Pinecone client
    pinecone_api_key = ""
    if not pinecone_api_key:
        logger.error("PINECONE_API_KEY environment variable not set")
        raise ValueError("PINECONE_API_KEY is required")
    
    pinecone_client = Pinecone(api_key=pinecone_api_key)
    
    # Initialize embedding model
    embedding_model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    try:
        embedding_model = SentenceTransformer(embedding_model_name)
        logger.info(f"Loaded embedding model: {embedding_model_name}")
    except Exception as e:
        logger.error(f"Failed to load embedding model: {e}")
        embedding_model = None

# Initialize on import
initialize_pinecone()

@mcp.resource("pinecone://indexes")
async def list_indexes_resource() -> str:
    """List all Pinecone indexes"""
    try:
        indexes = pinecone_client.list_indexes()
        return json.dumps([{
            "name": idx.name,
            "dimension": idx.dimension,
            "metric": idx.metric,
            "spec": str(idx.spec)
        } for idx in indexes], indent=2)
    except Exception as e:
        logger.error(f"Error listing indexes: {e}")
        return f"Error: {str(e)}"

@mcp.resource("pinecone://index/{index_name}")
async def get_index_stats_resource(index_name: str) -> str:
    """Get statistics for a specific index"""
    try:
        if index_name in [idx.name for idx in pinecone_client.list_indexes()]:
            index = pinecone_client.Index(index_name)
            stats = index.describe_index_stats()
            return json.dumps(stats, indent=2, default=str)
        else:
            return f"Index '{index_name}' not found"
    except Exception as e:
        logger.error(f"Error reading index {index_name}: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def create_index(name: str, dimension: int = 384, metric: str = "cosine") -> str:
    """Create a new Pinecone index
    
    Args:
        name: Index name
        dimension: Vector dimension (default: 384)
        metric: Distance metric (cosine, euclidean, dotproduct)
    """
    try:
        # Check if index already exists
        existing_indexes = [idx.name for idx in pinecone_client.list_indexes()]
        if name in existing_indexes:
            return f"Index '{name}' already exists"
        
        # Create index with serverless spec
        pinecone_client.create_index(
            name=name,
            dimension=dimension,
            metric=metric,
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        
        return f"✅ Successfully created index '{name}' with dimension {dimension} and metric '{metric}'"
        
    except Exception as e:
        return f"Error creating index: {str(e)}"

@mcp.tool()
async def delete_index(name: str) -> str:
    """Delete a Pinecone index
    
    Args:
        name: Index name to delete
    """
    try:
        # Check if index exists
        existing_indexes = [idx.name for idx in pinecone_client.list_indexes()]
        if name not in existing_indexes:
            return f"Index '{name}' does not exist"
        
        pinecone_client.delete_index(name)
        return f"🗑️ Successfully deleted index '{name}'"
        
    except Exception as e:
        return f"Error deleting index: {str(e)}"

@mcp.tool()
async def list_indexes() -> str:
    """List all Pinecone indexes"""
    try:
        indexes = pinecone_client.list_indexes()
        
        if not indexes:
            return "No indexes found"
        
        result = "📊 **PINECONE INDEXES**\n"
        result += "=" * 50 + "\n\n"
        
        for idx in indexes:
            result += f"📁 **{idx.name}**\n"
            result += f"   Dimension: {idx.dimension}\n"
            result += f"   Metric: {idx.metric}\n"
            result += f"   Spec: {idx.spec}\n\n"
        
        return result
        
    except Exception as e:
        return f"Error listing indexes: {str(e)}"

@mcp.tool()
async def upsert_vectors(index_name: str, texts: List[str], metadata: Optional[List[Dict]] = None, ids: Optional[List[str]] = None) -> str:
    """Insert or update vectors in an index
    
    Args:
        index_name: Target index name
        texts: Text content to embed and store
        metadata: Optional metadata for each text (same length as texts)
        ids: Optional custom IDs (auto-generated if not provided)
    """
    try:
        if not texts:
            return "Error: No texts provided"
        
        if not embedding_model:
            return "Error: Embedding model not available"
        
        # Get index
        index = pinecone_client.Index(index_name)
        
        # Generate embeddings
        embeddings = embedding_model.encode(texts).tolist()
        
        # Prepare vectors for upsert
        vectors = []
        metadata_list = metadata or []
        custom_ids = ids or []
        
        for i, (text, embedding) in enumerate(zip(texts, embeddings)):
            # Generate ID if not provided
            vector_id = custom_ids[i] if i < len(custom_ids) else str(uuid.uuid4())
            
            # Prepare metadata
            vector_metadata = metadata_list[i] if i < len(metadata_list) else {}
            vector_metadata.update({
                "text": text,
                "timestamp": datetime.now().isoformat()
            })
            
            vectors.append({
                "id": vector_id,
                "values": embedding,
                "metadata": vector_metadata
            })
        
        # Upsert vectors
        upsert_response = index.upsert(vectors=vectors)
        
        result = f"✅ Successfully upserted {len(vectors)} vectors to index '{index_name}'\n"
        result += f"Upserted count: {upsert_response.upserted_count}"
        
        return result
        
    except Exception as e:
        return f"Error upserting vectors: {str(e)}"

@mcp.tool()
async def semantic_search(index_name: str, query: str, top_k: int = 5, filter: Optional[Dict] = None, include_metadata: bool = True) -> str:
    """Perform semantic search in an index
    
    Args:
        index_name: Index to search in
        query: Search query text
        top_k: Number of results to return (default: 5)
        filter: Optional metadata filter
        include_metadata: Include metadata in results (default: true)
    """
    try:
        if not embedding_model:
            return "Error: Embedding model not available"
        
        # Get index
        index = pinecone_client.Index(index_name)
        
        # Generate query embedding
        query_embedding = embedding_model.encode([query]).tolist()[0]
        
        # Perform search
        search_results = index.query(
            vector=query_embedding,
            top_k=top_k,
            filter=filter,
            include_metadata=include_metadata
        )
        
        # Format results
        result = f"🔍 **SEMANTIC SEARCH RESULTS**\n"
        result += f"Query: '{query}'\n"
        result += "=" * 50 + "\n\n"
        
        if not search_results.matches:
            result += "No matches found."
        else:
            for i, match in enumerate(search_results.matches, 1):
                result += f"**Result {i}** (Score: {match.score:.4f})\n"
                result += f"ID: {match.id}\n"
                
                if include_metadata and match.metadata:
                    text = match.metadata.get("text", "N/A")
                    result += f"Text: {text}\n"
                    
                    # Add other metadata
                    other_metadata = {k: v for k, v in match.metadata.items() if k != "text"}
                    if other_metadata:
                        result += f"Metadata: {json.dumps(other_metadata, indent=2)}\n"
                
                result += "\n"
        
        return result
        
    except Exception as e:
        return f"Error performing search: {str(e)}"

@mcp.tool()
async def get_vectors(index_name: str, ids: List[str], include_metadata: bool = True) -> str:
    """Retrieve specific vectors by ID
    
    Args:
        index_name: Index name
        ids: Vector IDs to retrieve
        include_metadata: Include metadata (default: true)
    """
    try:
        if not ids:
            return "Error: No IDs provided"
        
        # Get index
        index = pinecone_client.Index(index_name)
        
        # Fetch vectors
        fetch_response = index.fetch(ids=ids, include_metadata=include_metadata)
        
        # Format results
        result = f"📋 **RETRIEVED VECTORS**\n"
        result += f"Index: {index_name}\n"
        result += "=" * 50 + "\n\n"
        
        if not fetch_response.vectors:
            result += "No vectors found for the provided IDs."
        else:
            for vector_id, vector_data in fetch_response.vectors.items():
                result += f"**ID: {vector_id}**\n"
                
                if include_metadata and vector_data.metadata:
                    text = vector_data.metadata.get("text", "N/A")
                    result += f"Text: {text}\n"
                    
                    other_metadata = {k: v for k, v in vector_data.metadata.items() if k != "text"}
                    if other_metadata:
                        result += f"Metadata: {json.dumps(other_metadata, indent=2)}\n"
                
                result += f"Vector dimension: {len(vector_data.values) if vector_data.values else 0}\n\n"
        
        return result
        
    except Exception as e:
        return f"Error retrieving vectors: {str(e)}"

@mcp.tool()
async def delete_vectors(index_name: str, ids: Optional[List[str]] = None, filter: Optional[Dict] = None, delete_all: bool = False) -> str:
    """Delete vectors by ID or filter
    
    Args:
        index_name: Index name
        ids: Vector IDs to delete
        filter: Metadata filter for deletion
        delete_all: Delete all vectors in index (use with caution)
    """
    try:
        # Get index
        index = pinecone_client.Index(index_name)
        
        if delete_all:
            # Delete all vectors
            index.delete(delete_all=True)
            result = f"🗑️ Successfully deleted ALL vectors from index '{index_name}'"
        elif ids:
            # Delete specific IDs
            index.delete(ids=ids)
            result = f"🗑️ Successfully deleted {len(ids)} vectors from index '{index_name}'"
        elif filter:
            # Delete by filter
            index.delete(filter=filter)
            result = f"🗑️ Successfully deleted vectors matching filter from index '{index_name}'"
        else:
            return "Error: Must provide ids, filter, or set delete_all=true"
        
        return result
        
    except Exception as e:
        return f"Error deleting vectors: {str(e)}"

@mcp.tool()
async def index_stats(index_name: str) -> str:
    """Get index statistics and information
    
    Args:
        index_name: Index name
    """
    try:
        # Get index
        index = pinecone_client.Index(index_name)
        
        # Get stats
        stats = index.describe_index_stats()
        
        # Format results
        result = f"📊 **INDEX STATISTICS**\n"
        result += f"Index: {index_name}\n"
        result += "=" * 50 + "\n\n"
        result += f"Total vector count: {stats.total_vector_count}\n"
        result += f"Dimension: {stats.dimension}\n"
        result += f"Index fullness: {stats.index_fullness}\n\n"
        
        if stats.namespaces:
            result += "**Namespaces:**\n"
            for namespace, namespace_stats in stats.namespaces.items():
                result += f"  {namespace}: {namespace_stats.vector_count} vectors\n"
        
        return result
        
    except Exception as e:
        return f"Error getting index stats: {str(e)}"

if __name__ == "__main__":
    mcp.run()
