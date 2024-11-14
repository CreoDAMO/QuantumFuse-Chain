import unittest
from unittest.mock import MagicMock
from src.quantumfuse_blockchain import QuantumFuseBlockchain
from src.quantumfuse_3d_visualizer import QuantumFuse3DVisualizer
from pygame.math import Vector3

class TestQuantumFuse3DVisualizer(unittest.TestCase):

    def setUp(self):
        # Create a mock blockchain
        self.blockchain = MagicMock(spec=QuantumFuseBlockchain)
        self.visualizer = QuantumFuse3DVisualizer(self.blockchain)

    def test_create_quantum_node(self):
        position = Vector3(1, 1, 1)
        self.visualizer.create_quantum_node(position)
        
        self.assertEqual(len(self.visualizer.nodes), 1, "Node should be added to the visualizer")
        self.assertEqual(self.visualizer.nodes[0]["position"], position, "Node position should match the input")

    def test_create_transaction(self):
        start = Vector3(0, 0, 0)
        end = Vector3(1, 1, 1)
        self.visualizer.create_transaction(start, end)
        
        self.assertEqual(len(self.visualizer.transactions), 1, "Transaction should be added to the visualizer")
        self.assertEqual(self.visualizer.transactions[0]["start"], start, "Start position should match the input")
        self.assertEqual(self.visualizer.transactions[0]["end"], end, "End position should match the input")

    def test_create_smart_contract(self):
        position = Vector3(0, 0, 0)
        self.visualizer.create_smart_contract(position)
        
        self.assertEqual(len(self.visualizer.smart_contracts), 1, "Smart contract should be added to the visualizer")
        self.assertEqual(self.visualizer.smart_contracts[0]["position"], position, "Smart contract position should match the input")

    def test_create_fusion_reactor(self):
        position = Vector3(0, 0, 0)
        self.visualizer.create_fusion_reactor(position)
        
        self.assertEqual(self.visualizer.fusion_reactor["position"], position, "Fusion reactor position should match the input")
        self.assertEqual(self.visualizer.fusion_reactor["radius"], 1.5, "Fusion reactor radius should be initialized to 1.5")

    def test_update_blockchain_data(self):
        self.blockchain.get_recent_transactions.return_value = []
        self.blockchain.get_new_smart_contracts.return_value = []
        self.blockchain.fusion_reactor.generate_energy.return_value = 1000
        self.blockchain.get_carbon_footprint.return_value = 100
        self.blockchain.get_energy_efficiency.return_value = 100

        self.visualizer.update_blockchain_data()

        # Check that the fusion reactor energy level is updated
        self.assertAlmostEqual(self.visualizer.fusion_reactor["energy_level"], 1.0, places=1, 
                               msg="Fusion reactor energy level should be updated correctly")

    def test_update_qfc_onramp_data(self):
        self.visualizer.on_ramp.get_recent_purchases.return_value = [{'user': 'Alice', 'amount': 100}]
        self.visualizer.create_quantum_node(Vector3(0, 0, 0))

        self.visualizer.update_qfc_onramp_data()

        self.assertEqual(len(self.visualizer.transactions), 1, "Transaction should be created from recent purchase")
        self.assertEqual(self.visualizer.transactions[0]["data"], "100 QFC", "Transaction data should reflect the purchase amount")

if __name__ == "__main__":
    unittest.main()
