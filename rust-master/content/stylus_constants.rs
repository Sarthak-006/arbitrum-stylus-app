#![cfg_attr(not(any(feature = "export-abi", test)), no_main)]
extern crate alloc;

use alloc::vec::Vec;
use stylus_sdk::alloy_primitives::Address;
use stylus_sdk::prelude::*;
use stylus_sdk::storage::StorageAddress;
use stylus_sdk::console;

// Constants are defined at the module level
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
    pub fn show_constants(_input: Vec<u8>) -> ArbResult {
        // Parse the const &str as a local Address variable
        let owner_address = Address::parse_checksummed(OWNER, None)
            .expect("Invalid address");
            
        console!("Contract: {}", CONTRACT_NAME);
        console!("Max Supply: {}", MAX_SUPPLY);
        console!("Owner Address: {}", owner_address);
        
        Ok(Vec::new())
    }
} 