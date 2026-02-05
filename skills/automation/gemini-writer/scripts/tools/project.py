"""
Project folder management tool.
"""

import os
import re
from typing import Optional


# Global variable to track the active project folder
_active_project_folder: Optional[str] = None


def sanitize_folder_name(name: str) -> str:
    """
    Sanitizes a folder name for filesystem compatibility.
    
    Args:
        name: The proposed folder name
        
    Returns:
        Sanitized folder name
    """
    # Replace spaces with underscores
    name = name.strip().replace(' ', '_')
    # Remove any characters that aren't alphanumeric, underscore, or hyphen
    name = re.sub(r'[^\w\-]', '', name)
    # Remove leading/trailing hyphens or underscores
    name = name.strip('-_')
    # Ensure it's not empty
    if not name:
        name = "untitled_project"
    return name


def get_active_project_folder() -> Optional[str]:
    """
    Returns the currently active project folder path.
    
    Returns:
        Path to active project folder or None if not set
    """
    return _active_project_folder


def set_active_project_folder(folder_path: str) -> None:
    """
    Sets the active project folder.
    
    Args:
        folder_path: Path to the project folder
    """
    global _active_project_folder
    _active_project_folder = folder_path


def create_project_impl(project_name: str) -> str:
    """
    Creates a new project folder in the output directory.
    
    Args:
        project_name: The desired project name
        
    Returns:
        Success message with folder path or error message
    """
    global _active_project_folder
    
    # Sanitize the folder name
    sanitized_name = sanitize_folder_name(project_name)
    
    # Get the script's root directory (where kimi-writer.py is located)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)  # Go up from tools/ to root
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(root_dir, "output")
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            return f"Error creating output directory: {str(e)}"
    
    # Create the full path inside output directory
    project_path = os.path.join(output_dir, sanitized_name)
    
    # Check if folder already exists
    if os.path.exists(project_path):
        # Use existing folder and set it as active
        _active_project_folder = project_path
        return f"Project folder already exists at '{project_path}'. Set as active project folder."
    
    # Create the folder
    try:
        os.makedirs(project_path, exist_ok=True)
        _active_project_folder = project_path
        return f"Successfully created project folder at '{project_path}'. This is now the active project folder."
    except Exception as e:
        return f"Error creating project folder: {str(e)}"

