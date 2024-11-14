// tests/test_quantumfuse_blockchain.py

import pytest
from quantumfuse_blockchain import EnhancedQuantumFuseBlockchain, Transaction, Block

@pytest.fixture
def blockchain():
    return EnhancedQuantumFuseBlockchain(num_shards=3, difficulty=4)

def test_create_genesis_block(blockchain):
    genesis_block = blockchain.create_genesis_block()
    assert isinstance(genesis_block, Block)
    assert genesis_block.index == 0
    assert genesis_block.previous_hash == "0"

def test_add_transaction(blockchain):
    tx = Transaction("Alice", "Bob", 100, "QFC")
    result = blockchain.add_transaction(tx)
    assert result == True

def test_mine_block(blockchain):
    tx = Transaction("Alice", "Bob", 100, "QFC")
    blockchain.add_transaction(tx)
    mined_block = blockchain.mine_block("MinerAddress")
    assert isinstance(mined_block, Block)
    assert len(mined_block.transactions) > 0

def test_get_qfc_balance(blockchain):
    blockchain.assets["QFC"]["balances"]["Alice"] = 1000
    balance = blockchain.get_qfc_balance("Alice")
    assert balance == 1000

def test_update_qfc_balances(blockchain):
    tx = Transaction("Alice", "Bob", 100, "QFC")
    blockchain.assets["QFC"]["balances"]["Alice"] = 1000
    blockchain.update_qfc_balances(tx)
    assert blockchain.get_qfc_balance("Alice") == 900
    assert blockchain.get_qfc_balance("Bob") == 100
