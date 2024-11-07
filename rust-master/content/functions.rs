// Basic function with return value
fn add(a: u32, b: u32) -> u32 {
    a + b
}

// Function with multiple return values using tuple
fn get_stats(numbers: &[i32]) -> (i32, i32) {
    let sum: i32 = numbers.iter().sum();
    let count = numbers.len() as i32;
    (sum, count)
}

// Function with generic type
fn print_value<T: std::fmt::Display>(value: T) {
    println!("Value is: {}", value);
}

fn main() {
    let result = add(5, 3);
    println!("Sum: {}", result);
    
    let numbers = vec![1, 2, 3, 4, 5];
    let (sum, count) = get_stats(&numbers);
    println!("Sum: {}, Count: {}", sum, count);
    
    print_value(42);
    print_value("Hello");
} 