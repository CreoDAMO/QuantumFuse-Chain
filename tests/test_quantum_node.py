# Filename: tests/test_quantumfuse_node.py
import pytest
from unittest.mock import MagicMock, patch
from src.quantumfuse_node import QuantumFuseNode
from src.quantumfuse_blockchain import Transaction, Block

@pytest.fixture
def node():
    """Fixture to initialize a QuantumFuseNode instance for tests."""
    return QuantumFuseNode(host="127.0.0.1", port=8080, stake=0.5)

def test_initialization(node):
    """Test that QuantumFuseNode initializes correctly with default values."""
    assert node.host == "127.0.0.1"
    assert node.port == 8080
    assert node.stake == 0.5
    assert node.peers == []
    assert node.blockchain is not None
    assert node.pending_transactions == []

@patch('src.quantumfuse_node.socket.socket')
def test_start_node(mock_socket, node):
    """Test starting the node and initiating peer listener."""
    node.listen_for_peers = MagicMock()
    node.start()
    node.listen_for_peers.assert_called_once()

def test_generate_rsa_keys(node):
    """Test RSA key generation."""
    private_key, public_key = node.generate_rsa_keys()
    assert private_key is not None
    assert public_key is not None
    assert private_key.key_size == 2048

def test_add_transaction(node):
    """Test adding a transaction to the pending list."""
    transaction_data = {"sender": "Alice", "recipient": "Bob", "amount": 10.0}
    transaction = Transaction(**transaction_data)
    
    node.verify_transaction = MagicMock(return_value=True)  # Mock verification
    
    node.add_transaction(transaction_data)
    assert transaction in node.pending_transactions

def test_process_message_transaction(node):
    """Test processing a valid transaction message."""
    with patch.object(node, 'add_transaction') as mock_add:
        node.process_message(json.dumps({"type": "transaction", "transaction": {}}))
        mock_add.assert_called_once()
