"""
Test configuration loading
"""
import os
import sys
import unittest
from unittest.mock import patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.config import settings

class TestConfig(unittest.TestCase):
    """Test configuration management"""
    
    def test_settings_loaded(self):
        """Test that settings are loaded"""
        self.assertIsNotNone(settings)
        self.assertIsNotNone(settings.BB_FINANCE_API_KEY)
        self.assertIsNotNone(settings.PINECONE_API_KEY)
    
    def test_default_values(self):
        """Test default values"""
        self.assertEqual(settings.PINECONE_DEFAULT_DIMENSION, 384)
        self.assertEqual(settings.PINECONE_DEFAULT_METRIC, "cosine")
        self.assertEqual(settings.EMBEDDING_MODEL, "all-MiniLM-L6-v2")

if __name__ == "__main__":
    unittest.main()
