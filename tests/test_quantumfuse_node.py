import sys
import os
import pytest
from quantumfuse_node import QuantumFuseNode, QFCOnRamp

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Mock class to simulate the blockchain behavior
class MockBlockchain:
    def __init__(self):
        self.balances = {}

    def add_balance(self, user, amount):
        if user in self.balances:
            self.balances[user] += amount
        else:
            self.balances[user] = amount

    def get_balance(self, user):
        return self.balances.get(user, 0)

@pytest.fixture
def blockchain_mock():
    return MockBlockchain()

def test_quantum_fuse_node_initialization():
    node = QuantumFuseNode('localhost', 5000, stake=0.8)
    assert node.host == 'localhost'
    assert node.port == 5000
    assert node.stake == 0.8

def test_qfc_onramp(blockchain_mock):
    on_ramp = QFCOnRamp(blockchain_mock)
    assert on_ramp.buy_qfc("Alice", 100, "USD") == True
    assert blockchain_mock.get_balance("Alice") == 100
    assert on_ramp.buy_qfc("Bob", 100, "GBP") == False
