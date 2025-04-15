#!/usr/bin/env python3
import sys
import json
import requests
from typing import Dict, List, Optional

def search_leetcode(query: str) -> List[Dict]:
    """Search LeetCode problems using the GraphQL API"""
    url = "https://leetcode.com/graphql"
    is_number = query.strip().isdigit()
    query_num = query.strip() if is_number else None
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    
    # For numeric queries, try to find exact problem by ID first
    if is_number:
        print(f"Searching for problem #{query_num}", file=sys.stderr)
        exact_problem = get_problem_by_id(url, headers, query_num)
        if exact_problem:
            return [exact_problem]
    
    # Do standard keyword search
    return perform_search(url, headers, query)[:10]  # Limit to 10 results

def get_problem_by_id(url: str, headers: Dict, problem_id: str) -> Optional[Dict]:
    """Try to get a specific problem by ID"""
    all_problems_query = """
    query allQuestions {
        allQuestions: allQuestionsRaw {
            questionId
            title
            titleSlug
            difficulty
            isPaidOnly
        }
    }
    """
    
    try:
        print(f"Trying direct problem lookup for #{problem_id}", file=sys.stderr)
        response = requests.post(
            url,
            json={"query": all_problems_query},
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            if "data" in data and "allQuestions" in data["data"]:
                all_problems = data["data"]["allQuestions"]
                for problem in all_problems:
                    if problem["questionId"] == problem_id:
                        print(f"Found direct match for problem #{problem_id}: {problem['title']}", file=sys.stderr)
                        return problem
                print(f"No problem with ID #{problem_id} found", file=sys.stderr)
    except Exception as e:
        print(f"Error in direct problem lookup: {str(e)}", file=sys.stderr)
    
    return None

def perform_search(url: str, headers: Dict, query: str) -> List[Dict]:
    """Perform a standard search by keywords"""
    query_string = """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
        problemsetQuestionList: questionList(
            categorySlug: $categorySlug
            limit: $limit
            skip: $skip
            filters: $filters
        ) {
            questions: data {
                title
                titleSlug
                difficulty
                questionId
                isPaidOnly
            }
        }
    }
    """
    
    variables = {
        "categorySlug": "",
        "skip": 0,
        "limit": 10,  # Only fetch 10 problems
        "filters": {
            "searchKeywords": query
        }
    }
    
    try:
        print(f"Connecting to LeetCode API...", file=sys.stderr)
        response = requests.post(
            url,
            json={"query": query_string, "variables": variables},
            headers=headers,
            timeout=10
        )
        
        print(f"Response status: {response.status_code}", file=sys.stderr)
        response.raise_for_status()
        
        data = response.json()
        questions = data.get("data", {}).get("problemsetQuestionList", {}).get("questions", [])
        print(f"Found {len(questions)} questions", file=sys.stderr)
        
        # For numeric queries, check for exact match
        if query.strip().isdigit():
            for q in questions:
                if q.get("questionId") == query.strip():
                    print(f"Found exact match for problem #{query}: {q['title']}", file=sys.stderr)
                    return [q]
        
        return questions
        
    except Exception as e:
        print(f"Error searching LeetCode: {str(e)}", file=sys.stderr)
        return []

def format_alfred_items(questions: List[Dict]) -> List[Dict]:
    """Format the questions into Alfred items"""
    items = []
    for q in questions:
        try:
            difficulty_emoji = {
                "Easy": "🟢",
                "Medium": "🟡",
                "Hard": "🔴"
            }.get(q.get("difficulty", ""), "")
            
            # Add problem number to the title
            problem_num = q.get("questionId", "")
            title = f"{problem_num}. {q['title']}" if problem_num else q["title"]
            
            subtitle = f"{difficulty_emoji} {q.get('difficulty', '')} • {q.get('titleSlug', '')}"
            
            if q.get("isPaidOnly", False):
                subtitle += " • 🔒 Premium"
            
            # Construct the full LeetCode URL
            problem_url = f"https://leetcode.com/problems/{q.get('titleSlug', '')}/"
            
            # Create Alfred item with the URL as the arg (for browser opening)
            items.append({
                "title": title,
                "subtitle": subtitle,
                "arg": problem_url,
                "valid": True,
                "icon": {"path": "icon.png"}
            })
        except Exception as e:
            print(f"Error formatting question: {e}", file=sys.stderr)
            continue
    
    # If no results, add a "no results" item
    if not items:
        items.append({
            "title": "No LeetCode problems found",
            "subtitle": "Try a different search term",
            "valid": False,
            "icon": {"path": "icon.png"}
        })
    
    return items

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"items": []}))
        return
    
    query = sys.argv[1]
    
    # Remove the immediate output that was blocking final results
    
    print(f"Searching LeetCode for: '{query}'", file=sys.stderr)
    questions = search_leetcode(query)
    
    # Print the results for debugging
    if questions:
        print(f"Found {len(questions)} results:", file=sys.stderr)
        print("-" * 50, file=sys.stderr)
        
        for i, q in enumerate(questions, 1):
            title = q.get("title", "Unknown")
            difficulty = q.get("difficulty", "Unknown")
            slug = q.get("titleSlug", "unknown")
            question_id = q.get("questionId", "N/A")
            difficulty_emoji = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}.get(difficulty, "")
            
            paid_only = "• 🔒 Premium" if q.get("isPaidOnly", False) else ""
            
            print(f"{i}. {question_id}. {title}", file=sys.stderr)
            print(f"   {difficulty_emoji} {difficulty} • {slug} {paid_only}", file=sys.stderr)
            print(f"   https://leetcode.com/problems/{slug}/", file=sys.stderr)
            print("", file=sys.stderr)
    
    items = format_alfred_items(questions)
    print(json.dumps({"items": items}))

if __name__ == "__main__":
    main() 