// tests/test_quantum_node_main.py

import pytest
from unittest.mock import MagicMock, patch
from main import QuantumFuseNode, QFCOnRamp

@pytest.fixture
def mock_blockchain():
    return MagicMock()

@pytest.fixture
def node(mock_blockchain):
    return QuantumFuseNode('localhost', 5000, stake=0.8)

def test_generate_rsa_keys(node):
    private_key, public_key = node.generate_rsa_keys()
    assert private_key is not None
    assert public_key is not None

def test_add_transaction(node):
    transaction = MagicMock()
    node.verify_transaction = MagicMock(return_value=True)
    node.add_transaction(transaction)
    assert transaction in node.pending_transactions

def test_create_block(node):
    node.is_validator = MagicMock(return_value=True)
    node.blockchain.mine_block = MagicMock(return_value=MagicMock())
    node.broadcast_block = MagicMock()
    node.create_block()
    assert node.blockchain.mine_block.called
    assert node.broadcast_block.called

@pytest.fixture
def on_ramp(mock_blockchain):
    return QFCOnRamp(mock_blockchain)

def test_buy_qfc(on_ramp):
    on_ramp._process_payment = MagicMock(return_value=True)
    result = on_ramp.buy_qfc("Alice", 100, "USD")
    assert result == True
    assert on_ramp.blockchain.assets["QFC"]["balances"]["Alice"] == 100

def test_buy_qfc_unsupported_currency(on_ramp):
    result = on_ramp.buy_qfc("Alice", 100, "GBP")
    assert result == False

def test_process_payment(on_ramp):
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        result = on_ramp._process_payment("Alice", 100, "USD")
        assert result == True

        mock_post.return_value.status_code = 400
        result = on_ramp._process_payment("Alice", 100, "USD")
        assert result == False
