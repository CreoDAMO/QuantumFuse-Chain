import pytest
from src.quantumfuse_blockchain import QuantumFuseBlockchain, Transaction

def test_blockchain_initialization():
    blockchain = QuantumFuseBlockchain(num_shards=3, difficulty=4)
    assert blockchain.num_shards == 3
    assert blockchain.difficulty == 4

def test_transaction_creation():
    tx = Transaction(sender="Alice", recipient="Bob", amount=100)
    assert tx.sender == "Alice"
    assert tx.recipient == "Bob"
    assert tx.amount == 100
