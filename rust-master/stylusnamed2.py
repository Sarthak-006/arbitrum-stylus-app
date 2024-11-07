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


st.title('🦀 Rust in Streamlit')


col = st.columns(3)

with col[0]:
    st.subheader('Code Input')
    code_selection = st.selectbox('Select an example', ('Hello world!', 'Variable binding', 'Stylus Hello'))
    code_dict = {
        "Hello world!": "hello.rs",
        "Variable binding": "variable.rs",
        "Stylus Hello": "stylus_hello.rs",
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
            - Regular Rust uses `println!` macro for console output
            - Stylus Rust uses `console!` macro from stylus_sdk
            - Stylus requires additional setup:
              - Debug feature flag in Cargo.toml
              - Local Stylus dev node
              - Smart contract structure with storage and entrypoint
            
            **Note:** Stylus code is for blockchain development and requires proper setup to run.
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
        
    if code_dict[code_selection] == 'stylus_hello.rs':
        with st.expander('See explanation'):
            st.markdown("""This example demonstrates how to use the Stylus SDK's console macro 
                for debugging Rust smart contracts on Arbitrum.""")
            
            st.markdown("**Overview**")
            
            st.markdown("""
- The `console!` macro works similar to Rust's `println!` macro
- Output will be visible when running on a local Stylus dev node
- Requires the debug feature flag in Cargo.toml
- Useful for debugging smart contract execution
            """)

    with placeholder:
        st.session_state.editor_code = st_ace(st.session_state.rust_code, language='rust', min_lines=8)

    # Add explanations after the code editor
    if code_dict[code_selection] == 'hello.rs':
        st.markdown("""
        ### Rust vs Stylus Hello World Comparison
        
        **Standard Rust Hello World**
        - Uses the built-in `println!` macro
        - Output goes directly to the console/terminal
        - No special setup required
        - Commonly used in regular Rust applications
        
        Example:
        ```rust
        println!("Hello, world!");
        ```
        """)

    if code_dict[code_selection] == 'stylus_hello.rs':
        st.markdown("""
        ### Stylus SDK Hello World
        
        The `console!` macro from `stylus_sdk` is specifically designed for smart contract debugging:
        
        - Works similar to Rust's `println!` macro but for blockchain context
        - Output is only visible when running on a local Stylus dev node
        - Requires the debug feature flag in Cargo.toml
        - Supports various formatting options:
        
        ```rust
        // Basic usage
        console!("hello there!");
        
        // With formatting
        console!("format {} arguments", "some");
        
        // Using variables
        let local_variable = "Stylus";
        console!("{local_variable} is awesome!");
        console!("When will you try out {}?", local_variable);
        ```
        
        Note: This code should only be used for development and debugging purposes.
        """)

    st.button('Run Code', on_click=generate_output, type='primary')
