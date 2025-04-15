# Alfred LeetCode

A powerful Alfred workflow to quickly search and access LeetCode problems.

## Features

- Search LeetCode problems by number (e.g., "1" for "Two Sum")
- Search by keywords (e.g., "merge" to find all merge-related problems)
- View problem difficulty (Easy 🟢, Medium 🟡, Hard 🔴)
- See Premium problems marked with 🔒
- Open problems directly in your browser

## Installation

1. Download the latest version from the [Releases](https://github.com/harttle/alfred-leetcode/releases) page
2. Double-click the `alfred-leetcode.alfredworkflow` file to install it in Alfred
3. Alfred will automatically install the workflow

## Usage

1. Type `lc` in Alfred's search bar followed by a space
2. Enter a problem number or keywords (examples below)
3. Select a problem from the results and press Enter to open it in your browser

### Examples

- `lc 1` - Find problem #1 (Two Sum)
- `lc merge` - Find all problems containing "merge"
- `lc dp easy` - Find easy Dynamic Programming problems

## Tips

- When searching by problem number, the workflow will find the exact match
- For keywords, up to 10 matching problems will be displayed
- Problem results show:
  - Problem number and title
  - Difficulty indicator (🟢 Easy, 🟡 Medium, 🔴 Hard)
  - Premium indicator (🔒) for LeetCode Premium problems

## Development

To contribute to this project:

1. Clone the repository
2. Make your changes to `alfred_leetcode.py`
3. Test locally with `python3 cli.py [search term]`
4. Build the workflow with `./build.sh` for local testing, or with a specific version for release
5. Submit a pull request

### Building the Workflow

There are two ways to build the workflow:

```bash
# For local development (uses version 1.0.0-dev)
./build.sh

# For releases with a specific version number
./build.sh --version 1.2.3

# Short form also works
./build.sh -v 1.2.3
```

This will create an `alfred-leetcode.alfredworkflow` file that can be installed in Alfred.

## License

MIT 