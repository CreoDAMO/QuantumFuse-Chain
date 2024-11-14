import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from pygame.math import Vector3
from quantumfuse_3d_model import QuantumFuse3DVisualizer, QFCOnRamp

class MockQuantumFuseBlockchain:
    def __init__(self):
        self.assets = {"QFC": {"balances": {}}}

    def get_qfc_balance(self, user):
        return self.assets["QFC"]["balances"].get(user, 0)

@pytest.fixture
def mock_blockchain():
    return MockQuantumFuseBlockchain()

@pytest.fixture
def visualizer(mock_blockchain):
    return QuantumFuse3DVisualizer(mock_blockchain)

def test_create_quantum_node(visualizer):
    position = Vector3(1, 2, 3)
    visualizer.create_quantum_node(position)
    assert len(visualizer.nodes) == 1
    assert visualizer.nodes[0]["position"] == position

def test_qfc_onramp(mock_blockchain):
    on_ramp = QFCOnRamp(mock_blockchain)
    assert on_ramp.buy_qfc("Alice", 100, "USD") == True
    assert on_ramp.buy_qfc("Bob", 100, "GBP") == False
