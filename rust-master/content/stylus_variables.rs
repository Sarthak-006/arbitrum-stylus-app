#![cfg_attr(not(any(feature = "export-abi", test)), no_main)]
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
    pub fn show_variables(_input: Vec<u8>) -> ArbResult {
        // Local variables
        let local_number = 42u32;
        let local_text = String::from("Local variable");
        
        // Using global variables
        let timestamp = block::timestamp();
        let sender = msg::sender();
        
        console!("Local variables: {}, {}", local_number, local_text);
        console!("Global variables - Timestamp: {}, Sender: {}", timestamp, sender);
        
        Ok(Vec::new())
    }
} 