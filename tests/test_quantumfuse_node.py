import unittest
from unittest.mock import patch, MagicMock
from quantumfuse_blockchain import Transaction
from quantumfuse_node import QuantumFuseNode


class TestQuantumFuseNode(unittest.TestCase):

    def setUp(self):
        self.node = QuantumFuseNode('localhost', 5000, stake=0.8)

    @patch('quantumfuse_node.socket.socket')
    def test_add_transaction(self, mock_socket):
        # Mock the transaction process
        transaction_data = {
            'sender': 'Alice',
            'recipient': 'Bob',
            'amount': 100,
            'asset': 'QFC'
        }
        self.node.add_transaction(transaction_data)

        # Assert that the transaction is in pending transactions
        self.assertEqual(len(self.node.pending_transactions), 1, "Transaction should be added to pending transactions")

    @patch('quantumfuse_node.socket.socket')
    def test_mine_block(self, mock_socket):
        # Mock a valid transaction
        transaction_data = {
            'sender': 'Alice',
            'recipient': 'Bob',
            'amount': 100,
            'asset': 'QFC'
        }
        self.node.add_transaction(transaction_data)

        # Test block creation
        with patch.object(self.node.blockchain, 'mine_block', return_value=MagicMock()) as mock_mine:
            self.node.create_block()
            self.assertTrue(mock_mine.called, "Mine block should be called")

    @patch('quantumfuse_node.socket.socket')
    @patch('requests.post')
    def test_buy_qfc(self, mock_post, mock_socket):
        # Mock the response of the payment processor
        mock_post.return_value.status_code = 200

        result = self.node.on_ramp.buy_qfc("Alice", 100, "USD")
        self.assertTrue(result, "Buying QFC should succeed")

    @patch('quantumfuse_node.socket.socket')
    def test_invalid_transaction(self, mock_socket):
        # Test adding an invalid transaction (negative amount)
        transaction_data = {
            'sender': 'Alice',
            'recipient': 'Bob',
            'amount': -100,
            'asset': 'QFC'
        }
        self.node.add_transaction(transaction_data)

        # Assert that the transaction is not added
        self.assertEqual(len(self.node.pending_transactions), 0, "Invalid transaction should not be added")

    @patch('quantumfuse_node.socket.socket')
    def test_listen_for_peers(self, mock_socket):
        # This test will simply check that the listening thread starts without errors
        with patch.object(self.node, 'listen_for_peers', return_value=None) as mock_listen:
            self.node.start()
            self.assertTrue(mock_listen.called, "Listening for peers should be initiated")

if __name__ == "__main__":
    unittest.main()
