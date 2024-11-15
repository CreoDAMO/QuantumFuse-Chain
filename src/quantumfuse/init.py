# Import main classes and functions to make them available when importing the package
from .quantumfuse_blockchain import QuantumFuseBlockchain, Transaction
from .quantumfuse_node import QuantumFuseNode

# You can also define __all__ to control what gets imported with "from quantumfuse import *"
__all__ = ['QuantumFuseBlockchain', 'Transaction', 'QuantumFuse3DModel', 'QuantumFuseNode']

# Optional: Add package-level docstring
"""
QuantumFuse Package

This package contains the core components of the QuantumFuse blockchain system,
including the blockchain implementation, 3D model, and node functionality.
"""

# Optional: Package metadata
__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# You can also perform any necessary package-level initialization here
def initialize():
    print("Initializing QuantumFuse package...")
    # Add any initialization code here

# Call the initialize function when the package is imported
initialize()
