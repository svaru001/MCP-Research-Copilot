#!/usr/bin/env python3
"""
Main entry point for MCP servers
"""

import argparse
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.mcp_servers.share_price_server import run_server as run_share_price_server
from src.mcp_servers.pinecone_server import run_server as run_pinecone_server

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="MCP Server Launcher")
    parser.add_argument(
        "server",
        choices=["share-price", "pinecone", "both"],
        help="Which server to run"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host to bind to (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    
    args = parser.parse_args()
    
    if args.server == "share-price":
        print("Starting Share Price MCP Server...")
        run_share_price_server()
    elif args.server == "pinecone":
        print("Starting Pinecone MCP Server...")
        run_pinecone_server()
    elif args.server == "both":
        print("Starting both MCP servers...")
        print("Note: Running both servers simultaneously requires separate processes")
        print("Please run each server in a separate terminal:")
        print("  python main.py share-price")
        print("  python main.py pinecone")

if __name__ == "__main__":
    main()
