#!/usr/bin/env python3
"""
Simple Python Application
Takes user input and outputs it back
"""

def main():
    print("=" * 50)
    print("Simple Python Application")
    print("=" * 50)
    print()
    
    while True:
        try:
            # Get user input
            user_input = input("Enter something (or 'quit' to exit): ")
            
            # Check if user wants to quit
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            # Output the input back
            print(f"Output: {user_input}")
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main() 