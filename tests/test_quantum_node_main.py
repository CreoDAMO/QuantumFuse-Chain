import pytest
from src.quantumfuse_node_main import QuantumFuseNode, QFCOnRamp

def test_node_initialization():
    node = QuantumFuseNode('localhost', 5000, stake=0.8)
    assert node.host == 'localhost'
    assert node.port == 5000
    assert node.stake == 0.8

def test_on_ramp_initialization():
    blockchain_mock = None  # Replace with a mock or a real instance if needed
    on_ramp = QFCOnRamp(blockchain_mock)
    assert on_ramp.exchange_rates["USD"] == 1.0
