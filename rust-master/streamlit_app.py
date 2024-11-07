import streamlit as st
import subprocess
from streamlit_ace import st_ace
from web3 import Web3
from eth_account import Account
import json

# Arbitrum Sepolia configuration
ARBITRUM_SEPOLIA_RPC = "https://sepolia-rollup.arbitrum.io/rpc"
CHAIN_ID = 421614

# Initialize Web3
def initialize_web3():
    w3 = Web3(Web3.HTTPProvider(ARBITRUM_SEPOLIA_RPC))
    return w3

# Add MetaMask connection function
def setup_web3():
    if 'web3' not in st.session_state:
        st.session_state.web3 = initialize_web3()
    return st.session_state.web3

# Function to check if we're connected to Arbitrum Sepolia
def check_network():
    if 'web3' not in st.session_state:
        return False
    
    try:
        chain_id = st.session_state.web3.eth.chain_id
        return chain_id == CHAIN_ID
    except Exception:
        return False

# Modified run_rust_code to include blockchain storage
def run_rust_code(code):
    # Original rust execution code remains the same
    with open('code.rs', 'w') as file:
        file.write(code)
    
    process1 = subprocess.Popen(['rustc', 'code.rs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process1.wait()
    
    process2 = subprocess.Popen(['./code'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result2 = process2.communicate()
    return result2[0]

# Add the blockchain storage functionality
def store_on_blockchain(code):
    w3 = setup_web3()
    if not check_network():
        st.error("Please connect to Arbitrum Sepolia network in MetaMask")
        return None
    
    try:
        # Example contract ABI and address (you'll need to deploy your own contract)
        contract_address = "0x9727004333e3A8efcCDfaC3d20431b8aEA27c437"
        contract_abi = [
	{
		"anonymous":False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "user",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "code",
				"type": "string"
			}
		],
		"name": "CodeStored",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_code",
				"type": "string"
			}
		],
		"name": "storeCode",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getUserCodes",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "userCodes",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
        
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        
        # Get the connected account from MetaMask
        accounts = w3.eth.accounts
        if not accounts:
            st.error("Please connect MetaMask")
            return None
            
        # Create the transaction
        tx = contract.functions.storeCode(code).build_transaction({
            'from': accounts[0],
            'nonce': w3.eth.get_transaction_count(accounts[0]),
            'gas': 300000,
            'gasPrice': w3.eth.gas_price,
        })
        
        return tx
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

st.set_page_config(page_title='Rust in Streamlit', page_icon='🦀', layout='wide')

def generate_output():
    with col[1]:
        st.subheader('Code Content')
        st.code(st.session_state.editor_code, line_numbers=True)
    
        st.subheader('Code Output')
        output = run_rust_code(st.session_state.editor_code)
        st.code(output, line_numbers=True)

if 'rust_code' not in st.session_state:
    st.session_state.rust_code = ''

if 'editor_code' not in st.session_state:
    st.session_state.editor_code = ''


st.title('🦀 Rust in Streamlit with Arbitrum')

# Add network status indicator
if check_network():
    st.success("Connected to Arbitrum Sepolia")
else:
    st.warning("Please connect to Arbitrum Sepolia network in MetaMask")

# Create two columns for the buttons
col1, col2 = st.columns(2)

with col1:
    if st.button('Run Code', on_click=generate_output, type='primary'):
        pass

with col2:
    if st.button('Store on Arbitrum'):
        if check_network():
            tx = store_on_blockchain(st.session_state.editor_code)
            if tx:
                st.success(f"Transaction created! Hash: {tx['hash'].hex()}")
                st.markdown(f"[View on Arbiscan](https://sepolia.arbiscan.io/tx/{tx['hash'].hex()})")
        else:
            st.error("Please connect to Arbitrum Sepolia network")
