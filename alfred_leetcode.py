#!/usr/bin/env python3
import sys
import json
import urllib.request
import urllib.parse
from typing import Dict, List, Optional

def search_leetcode(query: str) -> Optional[List[Dict]]:
    """
    Search LeetCode problems using the GraphQL API.
    
    Args:
        query: Search query string (problem title, keywords)
    
    Returns:
        List of problem dictionaries or None on error
    """
    # Use a consistent query structure and result limit for all search types
    graphql_query = {
        "query": """
            query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
                problemsetQuestionList: questionList(
                    categorySlug: $categorySlug
                    limit: $limit
                    skip: $skip
                    filters: $filters
                ) {
                    questions: data {
                        difficulty
                        frontendQuestionId: questionFrontendId
                        isPaidOnly: isPaidOnly
                        questionId
                        title
                        titleSlug
                    }
                }
            }
        """,
        "variables": {
            "categorySlug": "",
            "skip": 0,
            "limit": 10,  # Standard limit of 10 results
            "filters": {
                "searchKeywords": query
            }
        }
    }

    # Construct the request
    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com/problemset/all/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    
    # Let exceptions propagate to caller
    print(f"Searching LeetCode for: '{query}'", file=sys.stderr)
    data = json.dumps(graphql_query).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        if 'data' in result and 'problemsetQuestionList' in result['data']:
            questions = result['data']['problemsetQuestionList']['questions']
            print(f"Found {len(questions)} results", file=sys.stderr)
            return questions
        return []

def perform_search(query):
    """
    Performs a search on LeetCode and returns formatted results.
    
    Args:
        query: Search query string
        
    Returns:
        List of problem dictionaries formatted for Alfred display
    """
    try:
        # Get problems from LeetCode
        problems = search_leetcode(query)
        
        if not problems:
            # No results found - consistent message for all query types
            return [{
                "title": "No LeetCode problems found",
                "subtitle": f"No results for '{query}'",
                "icon": {"path": "icon.png"},
                "valid": False
            }]
        
        # Format all returned problems as Alfred items
        return format_alfred_items(problems)
    except Exception as e:
        # Get error details based on exception type
        error_type = type(e).__name__
        
        if isinstance(e, urllib.error.HTTPError):
            title = "LeetCode API Error"
            message = f"HTTP Error {e.code}: {e.reason}"
        elif isinstance(e, urllib.error.URLError):
            title = "Network Error"
            message = f"Could not connect to LeetCode: {str(e)}"
        else:
            title = "Error"
            message = f"An unexpected error occurred: {str(e)}"
            print(f"Error ({error_type}): {str(e)}", file=sys.stderr)
            
        # Return appropriate error message
        return [{
            "title": title,
            "subtitle": message,
            "icon": {"path": "icon.png"},
            "valid": False
        }]

def format_alfred_items(problems: List[Dict]) -> List[Dict]:
    """
    Format LeetCode problems as Alfred items.
    
    Args:
        problems: List of problem dictionaries from LeetCode API
        
    Returns:
        List of dictionaries formatted for Alfred JSON output
    """
    alfred_items = []
    
    for problem in problems:
        # Extract problem data
        problem_id = problem.get('frontendQuestionId', 'Unknown')
        title = problem.get('title', 'Unknown')
        difficulty = problem.get('difficulty', 'Unknown')
        is_premium = problem.get('isPaidOnly', False) or problem.get('paidOnly', False)
        slug = problem.get('titleSlug', '')
        
        # Create a formatted title with difficulty indicator
        difficulty_icon = {
            'Easy': '🟢',
            'Medium': '🟡',
            'Hard': '🔴'
        }.get(difficulty, '')
        
        premium_icon = '🔒 ' if is_premium else ''
        
        formatted_title = f"{problem_id}. {title}"
        subtitle = f"{difficulty_icon} {difficulty} {premium_icon}- Click to open in browser"
        
        # Create Alfred item
        alfred_item = {
            "title": formatted_title,
            "subtitle": subtitle,
            "arg": f"https://leetcode.com/problems/{slug}/",
            "icon": {"path": "icon.png"},
            "valid": True
        }
        
        alfred_items.append(alfred_item)
    
    return alfred_items

def main():
    # Get the search query from command line arguments
    if len(sys.argv) < 2:
        print("Usage: python alfred_leetcode.py [search_query]")
        return
    
    # Get the search query from arguments
    query = ' '.join(sys.argv[1:])
    
    # Perform the search and get results
    results = perform_search(query)
    
    # Output the results in Alfred's JSON format
    alfred_output = {
        "items": results
    }
    
    print(json.dumps(alfred_output))

if __name__ == "__main__":
    main() 