#!/usr/bin/env python3
"""
Share Price MCP Server Launcher
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.mcp_servers.share_price_server import run_server

if __name__ == "__main__":
    run_server()
