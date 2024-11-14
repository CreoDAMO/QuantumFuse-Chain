import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from quantumfuse_node import QuantumFuseNode, QFCOnRamp

def test_quantum_fuse_node_initialization():
    node = QuantumFuseNode('localhost', 5000, stake=0.8)
    assert node.host == 'localhost'
    assert node.port == 5000
    assert node.stake == 0.8

def test_qfc_onramp():
    blockchain_mock = type('MockBlockchain', (), {'add_balance': lambda self, user, amount: None})()
    on_ramp = QFCOnRamp(blockchain_mock)
    assert on_ramp.buy_qfc("Alice", 100, "USD") == True
    assert on_ramp.buy_qfc("Bob", 100, "GBP") == False
