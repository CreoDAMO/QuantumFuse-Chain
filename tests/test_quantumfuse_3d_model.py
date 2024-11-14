import pytest
from unittest.mock import MagicMock, patch
from pygame.math import Vector3

# Mock imports for OpenGL and pygame
with patch("OpenGL.GL"), patch("OpenGL.GLU"), patch("OpenGL.GLUT"), patch("pygame.display"):
    from quantumfuse_blockchain import QuantumFuseBlockchain, Transaction, Block  # Assuming these are real
    from your_visualization_module import QuantumFuse3DVisualizer, QFCOnRamp  # Replace with your module name

@pytest.fixture
def blockchain_mock():
    """Fixture to create a mock QuantumFuseBlockchain."""
    blockchain = MagicMock(spec=QuantumFuseBlockchain)
    blockchain.shards = [{}] * 3
    blockchain.get_recent_transactions.return_value = []
    blockchain.get_new_smart_contracts.return_value = []
    blockchain.fusion_reactor.generate_energy.return_value = 500  # Mock energy level
    blockchain.get_carbon_footprint.return_value = 50
    blockchain.get_energy_efficiency.return_value = 80
    blockchain.ai_optimizer.get_performance.return_value = [0.1, 0.2, 0.3]
    blockchain.nft_marketplace.get_trading_volume.return_value = 100000
    blockchain.get_cross_chain_activity.return_value = 5
    blockchain.governance.get_activity.return_value = [0.1, 0.2]
    blockchain.layer2_solution.get_transaction_count.return_value = 3
    return blockchain

@pytest.fixture
def visualizer(blockchain_mock):
    """Fixture to create a QuantumFuse3DVisualizer instance with a mocked blockchain."""
    return QuantumFuse3DVisualizer(blockchain=blockchain_mock)

def test_create_quantum_node(visualizer):
    """Test that a quantum node is created with the correct attributes."""
    position = Vector3(1, 2, 3)
    visualizer.create_quantum_node(position, size=0.5, color=(1, 0, 0, 1))
    
    assert len(visualizer.nodes) == 1
    node = visualizer.nodes[0]
    assert node["position"] == position
    assert node["size"] == 0.5
    assert node["color"] == (1, 0, 0, 1)
    assert node["quantum_effect"] in [True, False]

def test_create_transaction(visualizer):
    """Test transaction creation between two nodes."""
    start, end = Vector3(0, 0, 0), Vector3(1, 1, 1)
    visualizer.create_transaction(start, end, "Test Transaction")
    
    assert len(visualizer.transactions) == 1
    tx = visualizer.transactions[0]
    assert tx["start"] == start
    assert tx["end"] == end
    assert tx["data"] == "Test Transaction"
    assert tx["progress"] == 0.0

def test_update_blockchain_data(visualizer):
    """Test that blockchain data is correctly updated in the visualizer."""
    visualizer.create_quantum_node(Vector3(0, 0, 0))  # Add one node for testing
    visualizer.update_blockchain_data()
    
    assert len(visualizer.nodes) == 1
    assert visualizer.nodes[0]["color"] == (0, 1, 1, 1)
    assert visualizer.fusion_reactor["energy_level"] == 0.5  # normalized

def test_qfc_onramp_buy_qfc():
    """Test the QFCOnRamp buy_qfc method, mocking payment processing."""
    blockchain_mock = MagicMock(spec=QuantumFuseBlockchain)
    onramp = QFCOnRamp(blockchain_mock)
    
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        success = onramp.buy_qfc(user="user1", amount=100, currency="USD")
        
        assert success is True
        assert "user1" in blockchain_mock.assets["QFC"]["balances"]
        assert blockchain_mock.assets["QFC"]["balances"]["user1"] > 0

        # Check if recent purchases are updated
        recent_purchases = onramp.get_recent_purchases()
        assert len(recent_purchases) == 1
        assert recent_purchases[0]["user"] == "user1"
        assert recent_purchases[0]["amount"] > 0

def test_update_qfc_onramp_data(visualizer):
    """Test that on-ramp data is updated by creating a new transaction."""
    # Mock recent purchases from on_ramp
    visualizer.on_ramp.get_recent_purchases.return_value = [{"user": "user1", "amount": 50}]
    visualizer.update_qfc_onramp_data()
    
    assert len(visualizer.transactions) == 1
    tx = visualizer.transactions[0]
    assert tx["data"] == "50 QFC"
    assert tx["start"].x == 10  # start point is set to Vector3(10, 0, 0)
