#![cfg_attr(not(feature = "export-abi"), no_main)]
extern crate alloc;

use stylus_sdk::{console, prelude::*, stylus_proc::entrypoint, ArbResult};

#[storage]
#[entrypoint]
pub struct Hello;

#[public]
impl Hello {
    fn user_main(_input: Vec<u8>) -> ArbResult {
        console!("Hello Stylus!");
        Ok(Vec::new())
    }
} 