# Filename: tests/test_quantumfuse_blockchain.py
import pytest
from src.quantumfuse_blockchain import QuantumFuseBlockchain, Transaction

@pytest.fixture
def blockchain():
    """Fixture to initialize a QuantumFuseBlockchain instance for tests."""
    return QuantumFuseBlockchain(num_shards=3, difficulty=4)

def test_initial_blockchain_state(blockchain):
    """Verify initial blockchain state."""
    assert blockchain.chain == []
    assert blockchain.pending_transactions == []

def test_add_transaction(blockchain):
    """Test adding a transaction to the blockchain."""
    transaction = Transaction(sender="Alice", recipient="Bob", amount=10)
    blockchain.add_transaction(transaction)
    assert transaction in blockchain.pending_transactions

def test_mine_block(blockchain):
    """Test block mining with transactions."""
    transaction = Transaction(sender="Alice", recipient="Bob", amount=10)
    blockchain.add_transaction(transaction)
    block = blockchain.mine_block(miner_address="miner1")
    assert block is not None
    assert len(block.transactions) > 0
