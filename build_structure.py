import os
import re
from typing import List, Tuple, Optional

def create_structure_from_txt(txt_path: str, output_dir: str, verbose: bool = True):
    """
    Create a folder/file structure from a text file representation.
    Handles complex structures with comments and tree-style formatting.
    
    Args:
        txt_path: Path to the text file containing the structure
        output_dir: Directory where the structure will be created
        verbose: Whether to print detailed progress information
    """
    if not os.path.exists(txt_path):
        raise FileNotFoundError(f"Text file not found: {txt_path}")
    
    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    stack = []  # Track folder hierarchy
    stats = {'folders': 0, 'files': 0, 'skipped': 0}
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    for line_num, line in enumerate(lines, 1):
        try:
            # Parse the line
            item_name, is_file, indent_level = parse_line(line)
            
            # Skip if nothing to create
            if not item_name:
                continue
            
            # Adjust stack to current indent level
            while len(stack) > indent_level:
                stack.pop()

            # Build current path
            if stack:
                current_path = os.path.join(output_dir, *stack, item_name)
            else:
                current_path = os.path.join(output_dir, item_name)

            # Create file or folder
            if is_file:
                create_file(current_path, verbose)
                stats['files'] += 1
            else:
                create_folder(current_path, verbose)
                stack.append(item_name)
                stats['folders'] += 1
        
        except Exception as e:
            if verbose:
                print(f"⚠ Warning at line {line_num}: {e}")
            stats['skipped'] += 1
            continue

    # Print summary
    print(f"\n{'='*60}")
    print(f"✓ Structure created successfully at: {output_dir}")
    print(f"{'='*60}")
    print(f"  Folders created: {stats['folders']}")
    print(f"  Files created:   {stats['files']}")
    if stats['skipped'] > 0:
        print(f"  Items skipped:   {stats['skipped']}")
    print(f"{'='*60}\n")


def parse_line(line: str) -> Tuple[Optional[str], bool, int]:
    """
    Parse a line from the structure file.
    
    Returns:
        Tuple of (item_name, is_file, indent_level)
    """
    # Remove newlines and carriage returns
    line = line.rstrip('\n\r')
    
    # Skip empty lines
    if not line.strip():
        return None, False, 0
    
    # Calculate indentation level
    indent_level = calculate_indent_level(line)
    
    # Remove tree characters and indentation
    cleaned = remove_tree_characters(line)
    
    # Skip if line is only a comment
    if cleaned.startswith('#'):
        return None, False, 0
    
    # Remove inline comments (anything after # that's not part of the filename)
    # Keep # if it's part of the actual name (like __init__.py)
    item_name = extract_item_name(cleaned)
    
    # Skip if nothing left
    if not item_name:
        return None, False, 0
    
    # Determine if it's a file or folder
    is_file = is_file_item(item_name)
    
    return item_name, is_file, indent_level


def calculate_indent_level(line: str) -> int:
    """
    Calculate the indentation level of a line.
    Handles both spaces and tabs, as well as tree characters.
    """
    # Count leading whitespace and tree characters
    indent_chars = 0
    for char in line:
        if char in ' \t│':
            indent_chars += 1
        elif char in '├└─':
            continue
        else:
            break
    
    # Convert to indent level (every 4 characters = 1 level)
    return indent_chars // 4


def remove_tree_characters(line: str) -> str:
    """
    Remove tree-style characters from the line.
    """
    # Remove common tree characters
    tree_chars = ['│', '├', '└', '─', '├──', '└──']
    
    cleaned = line
    for char in tree_chars:
        cleaned = cleaned.replace(char, '')
    
    # Remove leading/trailing whitespace
    cleaned = cleaned.strip()
    
    return cleaned


def extract_item_name(text: str) -> str:
    """
    Extract the actual item name from cleaned text.
    Removes inline comments while preserving the item name.
    """
    # Split by # to separate name from comments
    parts = text.split('#')
    
    if len(parts) > 1:
        # Take the part before the first #
        name = parts[0].strip()
    else:
        name = text.strip()
    
    # Remove any invalid filename characters
    invalid_chars = '<>:"|?*\\'
    for char in invalid_chars:
        name = name.replace(char, '_')
    
    return name


def is_file_item(item_name: str) -> bool:
    """
    Determine if an item is a file or folder.
    
    Args:
        item_name: Name of the item
        
    Returns:
        True if it's a file, False if it's a folder
    """
    # Check if it has an extension (but not if it starts with a dot)
    if '.' in item_name and not item_name.startswith('.'):
        return True
    
    # Check if it's a dotfile (like .gitignore, .env)
    if item_name.startswith('.') and len(item_name) > 1:
        # If there's a dot after the first character, it's a file
        if '.' in item_name[1:]:
            return True
        # Otherwise, it could be a folder like .git or a file like .gitignore
        # We'll treat it as a file if it has no extension indicators
        return True
    
    # If it ends with /, it's definitely a folder
    if item_name.endswith('/'):
        return False
    
    # Default: if no extension, treat as folder
    return False


def create_file(file_path: str, verbose: bool = True):
    """
    Create an empty file at the specified path.
    """
    # Ensure parent directory exists
    parent_dir = os.path.dirname(file_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    
    # Create the file
    with open(file_path, 'w', encoding='utf-8') as f:
        pass
    
    if verbose:
        print(f"  📄 Created file: {file_path}")


def create_folder(folder_path: str, verbose: bool = True):
    """
    Create a folder at the specified path.
    """
    os.makedirs(folder_path, exist_ok=True)
    
    if verbose:
        print(f"  📁 Created folder: {folder_path}")


def preview_structure(txt_path: str, max_lines: int = 50):
    """
    Preview what will be created without actually creating it.
    
    Args:
        txt_path: Path to the structure file
        max_lines: Maximum number of lines to preview
    """
    if not os.path.exists(txt_path):
        raise FileNotFoundError(f"Text file not found: {txt_path}")
    
    print(f"\n{'='*60}")
    print(f"PREVIEW: Structure from {txt_path}")
    print(f"{'='*60}\n")
    
    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    folders = 0
    files = 0
    
    for i, line in enumerate(lines[:max_lines], 1):
        item_name, is_file, indent_level = parse_line(line)
        
        if item_name:
            indent = "  " * indent_level
            icon = "📄" if is_file else "📁"
            print(f"{indent}{icon} {item_name}")
            
            if is_file:
                files += 1
            else:
                folders += 1
    
    if len(lines) > max_lines:
        print(f"\n... and {len(lines) - max_lines} more lines")
    
    print(f"\n{'='*60}")
    print(f"Total: {folders} folders, {files} files")
    print(f"{'='*60}\n")


# Example usage
if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) < 3:
        print("Usage: python script.py <structure_file.txt> <output_directory> [--preview]")
        print("\nExample:")
        print("  python script.py structure.txt ./output")
        print("  python script.py structure.txt ./output --preview")
        sys.exit(1)
    
    txt_file = sys.argv[1]
    output_directory = sys.argv[2]
    
    # Preview mode
    if len(sys.argv) > 3 and sys.argv[3] == '--preview':
        preview_structure(txt_file)
    else:
        # Create the structure
        create_structure_from_txt(txt_file, output_directory, verbose=True)