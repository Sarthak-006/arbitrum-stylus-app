#![cfg_attr(not(any(feature = "export-abi", test)), no_main)]
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

// Public functions - external interface
#[public]
impl Contract {
    // External function returning a simple value
    pub fn get_value(&self) -> U256 {
        self.value.get()
    }
    
    // External function with parameters
    pub fn set_value(&mut self, new_value: U256) -> Result<(), Vec<u8>> {
        self.value.set(new_value);
        Ok(())
    }
    
    // External function returning multiple values via tuple
    pub fn get_contract_info(&self) -> (Address, U256) {
        (self.owner.get(), self.value.get())
    }
}

// Internal functions - private implementation
impl Contract {
    // Internal helper function
    fn log_operation(&self, operation: &str) {
        console!("Performing operation: {}", operation);
    }
    
    // Internal function with complex logic
    fn validate_owner(&self) -> bool {
        self.owner.get() == msg::sender()
    }
} 