import streamlit as st
import subprocess
from streamlit_ace import st_ace

st.set_page_config(page_title='Rust in Streamlit', page_icon='🦀', layout='wide')

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

if 'rust_code' not in st.session_state:
    st.session_state.rust_code = ''

if 'editor_code' not in st.session_state:
    st.session_state.editor_code = ''


st.title('🦀 Rust vs Stylus: Interactive Smart Contract Comparison')


col = st.columns(3)

with col[0]:
    st.subheader('Code Input')
    code_selection = st.selectbox('Select an example', ('Hello world!', 'Variable binding', 'Stylus Variables', 'Stylus Constants', 'Functions', 'Stylus Functions'))
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
    
    if code_dict[code_selection] == 'hello.rs':
        with st.expander('See explanation'):
            st.markdown("""
            ### Regular Rust vs Stylus Rust Hello World
            
            **Regular Rust Hello World**
            ```rust
            fn main() {
                println!("Hello World!");
            }
            ```
            
            **Stylus Rust Hello World**
            ```rust
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
            ```
            
            **Key Differences:**
            1. **Structure:**
               - Regular Rust: Simple `main()` function
               - Stylus: Smart contract structure with storage and entrypoint decorators
            
            2. **Output Method:**
               - Regular Rust: Uses `println!` macro
               - Stylus: Uses `console!` macro from stylus_sdk
            
            3. **Setup Requirements:**
               - Regular Rust: Just needs Rust compiler
               - Stylus: Requires:
                 - Stylus SDK
                 - Smart contract structure
                 - Debug feature flag in Cargo.toml
                 - Local Stylus dev node
            
            4. **Purpose:**
               - Regular Rust: Standard program output
               - Stylus: Blockchain smart contract with debugging output
            """)

        #with open(f'content/{code_dict[code_selection]}') as rust_file:
            #st.session_state.rust_code = rust_file.read()

    if code_dict[code_selection] == 'variable.rs':
        st.markdown("""Values can be assigned or bound to variables by using the `let` binding.
        """)

        #with open(f'content/{code_dict[code_selection]}') as rust_file:
            #st.session_state.rust_code = rust_file.read()
    with open(f'content/{code_dict[code_selection]}') as rust_file:
            st.session_state.rust_code = rust_file.read()
        
    if code_dict[code_selection] == 'stylus_variables.rs':
        with st.expander('See explanation'):
            st.markdown("""
            ### Regular Rust vs Stylus Rust Variables
            
            **Regular Rust Variables**
            ```rust
            fn main() {
                // Local variables
                let number = 42;
                let text = String::from("Hello");
                let mutable = 100;
                
                println!("Values: {}, {}, {}", number, text, mutable);
            }
            ```
            
            **Stylus Rust Variables**
            ```rust
            #[storage]
            pub struct Contract {
                // State variables (stored on blockchain)
                initialized: StorageBool,
                owner: StorageAddress,
                max_supply: StorageU256,
            }
            
            #[public]
            impl Contract {
                fn show_variables() -> ArbResult {
                    // Local variables (not stored on chain)
                    let local_number = 42u32;
                    let local_text = String::from("Local variable");
                    
                    // Global variables
                    let timestamp = block::timestamp();
                    let sender = msg::sender();
                    
                    console!("Variables: {}, {}", local_number, local_text);
                    Ok(Vec::new())
                }
            }
            ```
            
            **Key Differences:**
            1. **Variable Types:**
               - Regular Rust: Standard Rust types
               - Stylus: 
                 - State variables (StorageBool, StorageAddress, etc.)
                 - Local variables (standard Rust types)
                 - Global variables (blockchain context)
            
            2. **Storage:**
               - Regular Rust: All variables are temporary
               - Stylus: 
                 - State variables stored on blockchain
                 - Local variables temporary
                 - Global variables from blockchain context
            
            3. **Cost:**
               - Regular Rust: No cost considerations
               - Stylus:
                 - State variables: High cost (stored on chain)
                 - Local variables: Very efficient (>100x cheaper than Solidity)
                 - Global variables: Read-only blockchain data
            
            4. **Scope:**
               - Regular Rust: Function and block scope
               - Stylus: 
                 - State: Contract-wide persistence
                 - Local: Function scope
                 - Global: Blockchain context
            """)

    if code_dict[code_selection] == 'stylus_constants.rs':
        with st.expander('See explanation'):
            st.markdown("""
            ### Regular Rust vs Stylus Rust Constants
            
            **Regular Rust Constants**
            ```rust
            const MAX_POINTS: u32 = 100_000;
            const PI: f64 = 3.14159;
            const GREETING: &str = "Hello!";

            fn main() {
                println!("Max points: {}", MAX_POINTS);
                println!("Pi: {}", PI);
                println!("Greeting: {}", GREETING);
            }
            ```
            
            **Stylus Rust Constants**
            ```rust
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
                        
                    console!("Constants: {}, {}", MAX_SUPPLY, CONTRACT_NAME);
                    Ok(Vec::new())
                }
            }
            ```
            
            **Key Differences:**
            1. **Usage Context:**
               - Regular Rust: General-purpose programming
               - Stylus: Smart contract optimization and configuration
            
            2. **Gas Efficiency:**
               - Regular Rust: No gas considerations
               - Stylus: Constants are inlined at compile time, saving gas compared to storage variables
            
            3. **Common Use Cases:**
               - Regular Rust: Mathematical constants, configuration values
               - Stylus: Contract addresses, limits, fixed parameters
            
            4. **Scope and Lifetime:**
               - Regular Rust: Compile-time constants
               - Stylus: Transaction-wide constants, inlined at usage points
            
            **Important Notes:**
            - Constants must be type-annotated in both versions
            - Constants are immutable and known at compile time
            - In Stylus, constants can help optimize gas usage
            - Constants are typically defined at the module level
            - Values must be constant expressions that can be determined at compile time
            """)

    if code_dict[code_selection] == 'functions.rs':
        with st.expander('See explanation'):
            st.markdown("""
            ### Regular Rust vs Stylus Rust Functions
            
            **Regular Rust Functions**
            ```rust
            // Basic function
            fn add(a: u32, b: u32) -> u32 {
                a + b
            }

            // Function with multiple returns
            fn get_stats(numbers: &[i32]) -> (i32, i32) {
                let sum: i32 = numbers.iter().sum();
                let count = numbers.len() as i32;
                (sum, count)
            }
            ```
            
            **Stylus Rust Functions**
            ```rust
            #[storage]
            pub struct Contract {
                owner: StorageAddress,
                value: StorageU256,
            }

            // Public (external) functions
            #[public]
            impl Contract {
                pub fn get_value(&self) -> U256 {
                    self.value.get()
                }
                
                pub fn set_value(&mut self, new_value: U256) -> Result<(), Vec<u8>> {
                    self.value.set(new_value);
                    Ok(())
                }
            }

            // Internal (private) functions
            impl Contract {
                fn validate_owner(&self) -> bool {
                    self.owner.get() == msg::sender()
                }
            }
            ```
            
            **Key Differences:**
            1. **Function Types:**
               - Regular Rust: All functions are internal by default
               - Stylus: 
                 - Public functions (external interface) marked with `#[public]`
                 - Internal functions (private implementation)
            
            2. **Return Types:**
               - Regular Rust: Any type can be returned
               - Stylus: 
                 - Often returns `Result` for error handling
                 - Can return blockchain-specific types (Address, U256)
            
            3. **State Access:**
               - Regular Rust: Functions are stateless
               - Stylus: 
                 - Functions can access contract storage
                 - Use `&self` to read state
                 - Use `&mut self` to modify state
            
            4. **Error Handling:**
               - Regular Rust: Uses `Result` and `Option` for errors
               - Stylus: Uses `Result<T, Vec<u8>>` for external functions
            
            **Important Notes:**
            - Public functions in Stylus are part of the contract's ABI
            - Internal functions can help organize code and reduce gas costs
            - State modifications require `&mut self`
            - Error handling is crucial for blockchain operations
            """)

    with placeholder:
        st.session_state.editor_code = st_ace(st.session_state.rust_code, language='rust', min_lines=8)

    st.button('Run Code', on_click=generate_output, type='primary')
