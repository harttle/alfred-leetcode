#!/usr/bin/env python3
import sys
import json
from alfred_leetcode import search_leetcode, format_alfred_items

def main():
    # Check if a query was provided
    if len(sys.argv) < 2:
        print("Usage: python3 cli.py [search query]")
        print("Example: python3 cli.py two sum")
        return 1
    
    # Join all arguments as the search query
    query = " ".join(sys.argv[1:])
    
    # Search LeetCode
    print(f"Searching LeetCode for: '{query}'")
    try:
        questions = search_leetcode(query)
        
        if not questions:
            print("No results found.")
            return 0
        
        # Format results
        items = format_alfred_items(questions)
        
        # Print results in a readable format
        print(f"Found {len(items)} results:")
        print("-" * 50)
        for i, item in enumerate(items, 1):
            print(f"{i}. {item['title']}")
            print(f"   {item['subtitle']}")
            print(f"   {item['arg']}")
            print()
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 