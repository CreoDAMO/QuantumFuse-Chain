import pytest
from unittest.mock import MagicMock
from quantumfuse_3d_model import QuantumFuse3DVisualizer
from pygame.math import Vector3

@pytest.fixture
def mock_blockchain():
    return MagicMock()

@pytest.fixture
def visualizer(mock_blockchain):
    return QuantumFuse3DVisualizer(mock_blockchain)

def test_create_quantum_node(visualizer):
    position = Vector3(1, 2, 3)
    visualizer.create_quantum_node(position)
    assert len(visualizer.nodes) == 1
    assert visualizer.nodes[0]["position"] == position

def test_create_transaction(visualizer):
    start = Vector3(0, 0, 0)
    end = Vector3(1, 1, 1)
    visualizer.create_transaction(start, end, "Test Transaction")
    assert len(visualizer.transactions) == 1
    assert visualizer.transactions[0]["start"] == start
    assert visualizer.transactions[0]["end"] == end
    assert visualizer.transactions[0]["data"] == "Test Transaction"

def test_create_fusion_reactor(visualizer):
    position = Vector3(0, 0, 0)
    visualizer.create_fusion_reactor(position)
    assert visualizer.fusion_reactor["position"] == position
    assert visualizer.fusion_reactor["radius"] == 1.5
    assert visualizer.fusion_reactor["energy_level"] == 1.0

def test_update_blockchain_data(visualizer, mock_blockchain):
    mock_blockchain.get_recent_transactions.return_value = [
        MagicMock(sender="Alice", recipient="Bob", amount=100)
    ]
    mock_blockchain.get_new_smart_contracts.return_value = [MagicMock()]
    mock_blockchain.fusion_reactor.generate_energy.return_value = 500
    mock_blockchain.get_carbon_footprint.return_value = 50
    mock_blockchain.get_energy_efficiency.return_value = 80

    visualizer.nodes = [{"position": Vector3(0, 0, 0)}]
    visualizer.impact_metrics = [{"impact_level": 0}, {"impact_level": 0}]
    
    visualizer.update_blockchain_data()

    assert len(visualizer.transactions) == 1
    assert visualizer.fusion_reactor["energy_level"] == 0.5
    assert visualizer.impact_metrics[0]["impact_level"] == 0.5
    assert visualizer.impact_metrics[1]["impact_level"] == 0.8
