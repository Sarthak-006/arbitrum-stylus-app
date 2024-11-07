import streamlit as st
import subprocess
from streamlit_ace import st_ace

st.set_page_config(page_title='Rust vs Stylus', page_icon='🦀', layout='wide')

# Store code examples as dictionary
CODE_EXAMPLES = {
    "hello.rs": """fn main() {
    println!("Hello World! Rust works!");
}""",
    
    "variable.rs": """fn main() {
    let x = 5u32;
    let y = true;
    let z = String::from("Hello world!");
    println!("The value of x: {:?}", x);
    println!("The value of y: {:?}", y);
    println!("The value of z: {:?}", z);
}""",
    
    "stylus_variables.rs": """#![cfg_attr(not(any(feature = "export-abi", test)), no_main)]
extern crate alloc;

use stylus_sdk::alloy_primitives::{U16, U256};
use stylus_sdk::prelude::*;
use stylus_sdk::storage::{StorageAddress, StorageBool, StorageU256};
use stylus_sdk::{block, console, msg};

#[storage]
#[entrypoint]
pub struct Contract {
    initialized: StorageBool,
    owner: StorageAddress,
    max_supply: StorageU256,
}

#[public]
impl Contract {
    pub fn show_variables() -> ArbResult {
        let local_number = 42u32;
        let local_text = String::from("Local variable");
        
        let timestamp = block::timestamp();
        let sender = msg::sender();
        
        console!("Local variables: {}, {}", local_number, local_text);
        console!("Global variables: {}, {}", timestamp, sender);
        Ok(Vec::new())
    }
}""",
    
    "stylus_constants.rs": """#![cfg_attr(not(any(feature = "export-abi", test)), no_main)]
extern crate alloc;

use stylus_sdk::alloy_primitives::Address;
use stylus_sdk::prelude::*;
use stylus_sdk::storage::StorageAddress;
use stylus_sdk::console;

const OWNER: &str = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045";
const MAX_SUPPLY: u32 = 1000;
const CONTRACT_NAME: &str = "MyContract";

#[storage]
#[entrypoint]
pub struct Contract {
    owner: StorageAddress,
}

#[public]
impl Contract {
    pub fn show_constants() -> ArbResult {
        let owner_address = Address::parse_checksummed(OWNER, None)
            .expect("Invalid address");
            
        console!("Contract: {}", CONTRACT_NAME);
        console!("Max Supply: {}", MAX_SUPPLY);
        console!("Owner Address: {}", owner_address);
        
        Ok(Vec::new())
    }
}""",
    
    "stylus_functions.rs": """#![cfg_attr(not(any(feature = "export-abi", test)), no_main)]
extern crate alloc;

use stylus_sdk::alloy_primitives::{Address, U256};
use stylus_sdk::prelude::*;
use stylus_sdk::storage::{StorageAddress, StorageU256};
use stylus_sdk::console;

#[storage]
#[entrypoint]
pub struct Contract {
    owner: StorageAddress,
    value: StorageU256,
}

#[public]
impl Contract {
    pub fn get_value(&self) -> U256 {
        self.value.get()
    }
    
    pub fn set_value(&mut self, new_value: U256) -> Result<(), Vec<u8>> {
        self.value.set(new_value);
        Ok(())
    }
    
    pub fn get_contract_info(&self) -> (Address, U256) {
        (self.owner.get(), self.value.get())
    }
}

impl Contract {
    fn log_operation(&self, operation: &str) {
        console!("Performing operation: {}", operation);
    }
    
    fn validate_owner(&self) -> bool {
        self.owner.get() == msg::sender()
    }
}"""
}

def run_rust_code(code):
    with open('code.rs', 'w') as file:
        file.write(code)
    
    process1 = subprocess.Popen(['rustc', 'code.rs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process1.wait()
    
    process2 = subprocess.Popen(['./code'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result2 = process2.communicate()
    return result2[0]

def generate_output():
    with col[1]:
        st.subheader('Code Content')
        st.code(st.session_state.editor_code, line_numbers=True)
    
        st.subheader('Code Output')
        output = run_rust_code(st.session_state.editor_code)
        st.code(output, line_numbers=True)

if 'editor_code' not in st.session_state:
    st.session_state.editor_code = ''

st.title('🦀 Rust vs Stylus: Interactive Smart Contract Comparison')

col = st.columns(3)

with col[0]:
    st.subheader('Code Input')
    code_selection = st.selectbox('Select an example', 
        ('Hello world!', 'Variable binding', 'Stylus Variables', 'Stylus Constants', 'Functions', 'Stylus Functions'))
    
    code_dict = {
        "Hello world!": "hello.rs",
        "Variable binding": "variable.rs",
        "Stylus Variables": "stylus_variables.rs",
        "Stylus Constants": "stylus_constants.rs",
        "Functions": "functions.rs",
        "Stylus Functions": "stylus_functions.rs"
    }

    st.caption(f'Contents of {code_dict[code_selection]}:')
    placeholder = st.empty()
    
    # Get code from the dictionary instead of file
    st.session_state.editor_code = CODE_EXAMPLES.get(code_dict[code_selection], "// Example not found")
    
    # Your existing explanation sections remain the same
    if code_dict[code_selection] == 'hello.rs':
        with st.expander('See explanation'):
            # Your existing hello.rs explanation
            pass
    
    # ... rest of your explanations ...
    
    with placeholder:
        st.session_state.editor_code = st_ace(st.session_state.editor_code, language='rust', min_lines=8)

    st.button('Run Code', on_click=generate_output, type='primary')
