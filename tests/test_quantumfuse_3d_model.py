import pytest
from src.quantumfuse_3d_model import QuantumFuse3DVisualizer
from src.quantumfuse_blockchain import QuantumFuseBlockchain

def test_visualizer_initialization():
    blockchain = QuantumFuseBlockchain(num_shards=3, difficulty=4)
    visualizer = QuantumFuse3DVisualizer(blockchain)
    assert visualizer.blockchain == blockchain
