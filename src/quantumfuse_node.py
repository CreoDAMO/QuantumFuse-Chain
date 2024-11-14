import hashlib
import json
import time
import threading
import socket
import random
from typing import List, Dict, Any, Tuple
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import requests
from quantumfuse_blockchain import QuantumFuseBlockchain, Transaction, Block
from quantumfuse_3d_model import QuantumFuse3DModel

class QuantumFuseNode:
    def __init__(self, host: str, port: int, stake: float):
        self.host = host
        self.port = port
        self.stake = stake  # PoS stake for validation priority
        self.peers: List[Tuple[str, int]] = []
        self.blockchain = QuantumFuseBlockchain(num_shards=3, difficulty=4)
        self.pending_transactions = []
        self.multi_sig_transactions = []
        self.identity_registry = {}  # Store decentralized identities (DIDs)
        self.visualizer = QuantumFuse3DModel()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.private_key, self.public_key = self.generate_rsa_keys()
        self.on_ramp = QFCOnRamp(self.blockchain)

    def generate_rsa_keys(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def start(self):
        print(f"QuantumFuse Node starting on {self.host}:{self.port}")
        threading.Thread(target=self.listen_for_peers, daemon=True).start()
        threading.Thread(target=self.visualizer.start, daemon=True).start()
        self.run()

    def listen_for_peers(self):
        while True:
            client_socket, address = self.server_socket.accept()
            threading.Thread(target=self.handle_peer, args=(client_socket,), daemon=True).start()

    def handle_peer(self, client_socket):
        while True:
            try:
                message = client_socket.recv(4096).decode()
                if message:
                    self.process_message(message)
            except Exception as e:
                print(f"Error handling peer: {e}")
                break
        client_socket.close()

    def process_message(self, message: str):
        try:
            data = json.loads(message)
            if data['type'] == 'transaction':
                self.add_transaction(data['transaction'])
            elif data['type'] == 'multi_sig_transaction':
                self.add_multi_sig_transaction(data['transaction'])
            elif data['type'] == 'block':
                self.add_block(data['block'])
            elif data['type'] == 'sync_request':
                self.sync_chain(data['from'])
        except json.JSONDecodeError:
            print("Received invalid message")

    def add_transaction(self, transaction_data: Dict[str, Any]):
        transaction = Transaction(**transaction_data)
        if self.verify_transaction(transaction):
            self.pending_transactions.append(transaction)
            self.broadcast_transaction(transaction)
            print(f"Transaction added: {transaction}")

    def add_multi_sig_transaction(self, transaction_data: Dict[str, Any]):
        transaction = Transaction(**transaction_data)
        if self.verify_multi_sig_transaction(transaction):
            self.multi_sig_transactions.append(transaction)
            self.broadcast_transaction(transaction)
            print(f"Multi-Sig Transaction added: {transaction}")

    def verify_transaction(self, transaction: Transaction) -> bool:
        return transaction.amount > 0 and self.verify_identity(transaction.sender)

    def verify_multi_sig_transaction(self, transaction: Transaction) -> bool:
        valid_sigs = sum(1 for sig in transaction.signatures if self.verify_signature(sig, transaction))
        return valid_sigs >= len(transaction.signatures) // 2 + 1

    def verify_identity(self, identity: str) -> bool:
        return identity in self.identity_registry

    def verify_signature(self, signature: str, transaction: Transaction) -> bool:
        # Implement signature verification logic
        return True  # Placeholder

    def is_validator(self) -> bool:
        return random.random() < self.stake / 10

    def create_block(self):
        if self.is_validator():
            new_block = self.blockchain.mine_block(self.public_key)
            if new_block:
                self.broadcast_block(new_block)
                self.visualizer.update_blockchain(self.blockchain)
                print(f"New block created and broadcasted: {new_block}")

    def add_block(self, block_data: Dict[str, Any]):
        block = Block(**block_data)
        if self.blockchain.add_block(block):
            self.visualizer.update_blockchain(self.blockchain)

    def sync_chain(self, peer: Tuple[str, int]):
        latest_block = self.blockchain.get_latest_block()
        sync_message = json.dumps({
            'type': 'sync_request',
            'from': (self.host, self.port),
            'latest_block_index': latest_block.index
        })
        self.send_message_to_peer(peer, sync_message)

    def broadcast_transaction(self, transaction: Transaction):
        message = json.dumps({
            'type': 'transaction',
            'transaction': transaction.__dict__
        })
        self.broadcast_message(message)

    def broadcast_block(self, block: Block):
        message = json.dumps({
            'type': 'block',
            'block': block.__dict__
        })
        self.broadcast_message(message)

    def broadcast_message(self, message: str):
        for peer in self.peers:
            self.send_message_to_peer(peer, message)

    def send_message_to_peer(self, peer: Tuple[str, int], message: str):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(peer)
                encrypted_message = self.encrypt_message(message)
                s.sendall(encrypted_message)
        except Exception as e:
            print(f"Failed to send message to {peer}: {e}")

    def encrypt_message(self, message: str) -> bytes:
        return self.public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def connect_to_peer(self, peer_address: Tuple[str, int]):
        if peer_address not in self.peers:
            self.peers.append(peer_address)
            print(f"Connected to new peer: {peer_address}")
            self.sync_chain(peer_address)

    def run(self):
        while True:
            command = input("Enter command (mine/tx/balance/buy_qfc/exit): ")
            if command == "mine":
                self.create_block()
            elif command == "tx":
                sender = input("Enter sender: ")
                recipient = input("Enter recipient: ")
                amount = float(input("Enter amount: "))
                tx = Transaction(sender, recipient, amount)
                self.add_transaction(tx.__dict__)
            elif command == "balance":
                address = input("Enter address: ")
                balance = self.blockchain.get_balance(address)
                print(f"Balance of {address}: {balance}")
            elif command == "buy_qfc":
                user = input("Enter user: ")
                amount = float(input("Enter amount: "))
                currency = input("Enter currency (USD/EUR/JPY): ")
                success = self.on_ramp.buy_qfc(user, amount, currency)
                if success:
                    print(f"Successfully purchased QFC for {user}")
                else:
                    print("Failed to purchase QFC")
            elif command == "exit":
                break
            else:
                print("Invalid command")

class QFCOnRamp:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.exchange_rates = {
            "USD": 1.0,
            "EUR": 0.85,
            "JPY": 110.0
        }

    def buy_qfc(self, user: str, amount: float, currency: str) -> bool:
        if currency not in self.exchange_rates:
            print(f"Unsupported currency: {currency}")
            return False

        qfc_amount = amount / self.exchange_rates[currency]
        
        if self._process_payment(user, amount, currency):
            self.blockchain.add_balance(user, qfc_amount)
            print(f"Successfully purchased {qfc_amount} QFC for {user}")
            return True
        else:
            print("Payment processing failed")
            return False

    def _process_payment(self, user: str, amount: float, currency: str) -> bool:
        # Simulate calling an external payment API
        try:
            response = requests.post(
                "https://fake-payment-processor.com/api/process",
                json={
                    "user": user,
                    "amount": amount,
                    "currency": currency
                }
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

if __name__ == "__main__":
    node = QuantumFuseNode('localhost', 5000, stake=0.8)
    node.start()
