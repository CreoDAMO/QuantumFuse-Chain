import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from quantumfuse_blockchain import EnhancedQuantumFuseBlockchain, Transaction

def test_blockchain_initialization():
    blockchain = EnhancedQuantumFuseBlockchain(num_shards=3, difficulty=4)
    assert len(blockchain.shards) == 3
    assert blockchain.difficulty == 4

def test_add_transaction():
    blockchain = EnhancedQuantumFuseBlockchain(num_shards=3, difficulty=4)
    tx = Transaction("Alice", "Bob", 100, "QFC")
    result = blockchain.add_transaction(tx)
    assert result == True
