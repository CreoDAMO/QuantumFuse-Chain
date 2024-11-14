import unittest
import json
from quantumfuse_blockchain import EnhancedQuantumFuseBlockchain, Transaction
from cryptography.hazmat.primitives.asymmetric import rsa

class TestEnhancedQuantumFuseBlockchain(unittest.TestCase):

    def setUp(self):
        # Set up a new blockchain instance for testing
        self.blockchain = EnhancedQuantumFuseBlockchain(num_shards=3, difficulty=4)
        # Generate RSA keys for signing transactions
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()

    def test_add_transaction(self):
        # Test adding a transaction
        tx = Transaction("Alice", "Bob", 100, "QFC")
        tx.sign_transaction(self.private_key)
        result = self.blockchain.add_transaction(tx)
        self.assertTrue(result, "Transaction should be added successfully")

    def test_mine_block(self):
        # Test mining a block after a transaction
        tx = Transaction("Alice", "Bob", 100, "QFC")
        tx.sign_transaction(self.private_key)
        self.blockchain.add_transaction(tx)
        mined_block = self.blockchain.mine_block("MinerAddress")
        self.assertIsNotNone(mined_block, "Mining should produce a block")
        self.assertEqual(mined_block.index, 1, "Mined block index should be 1")

    def test_nft_creation(self):
        # Test NFT creation
        nft_id = "NFT1"
        result = self.blockchain.nft_marketplace.mint_nft(nft_id, "Alice", {"name": "First NFT", "description": "This is the first NFT on QuantumFuse"})
        self.assertTrue(result, "NFT should be created successfully")
        self.assertIn(nft_id, self.blockchain.nft_marketplace.nfts, "NFT should be present in the marketplace")

    def test_qfc_balance(self):
        # Test QFC balance handling
        self.blockchain.on_ramp.buy_qfc("Alice", 100, "USD")
        balance = self.blockchain.get_qfc_balance("Alice")
        self.assertGreater(balance, 0, "Alice's QFC balance should be greater than 0")

    def test_kyc_process(self):
        # Test KYC process
        result = self.blockchain.compliance_tools.perform_kyc("Alice", {"name": "Alice", "age": 30, "country": "Wonderland"})
        self.assertTrue(result, "KYC should be performed successfully")

    def test_cross_shard_transaction(self):
        # Test cross shard transaction
        tx = Transaction("Alice", "Bob", 50, "QFC")
        tx.sign_transaction(self.private_key)
        self.blockchain.add_transaction(tx)
        result = self.blockchain.cross_shard_coordinator.initiate_cross_shard_transaction(tx)
        self.assertTrue(result, "Cross shard transaction should be initiated successfully")

if __name__ == "__main__":
    unittest.main()
