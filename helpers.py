import re

def clean_title(raw_title: str) -> str:
    # Check if angle brackets exist and extract their content
    angle_bracket_match = re.search(r'<([^>]*)>', raw_title)
    if angle_bracket_match:
        # Use content inside angle brackets as base title
        title = angle_bracket_match.group(1)
    else:
        title = raw_title

    # Remove file extension at the end of the title
    title = re.sub(r'\.[a-z0-9]+$', '', title, flags=re.IGNORECASE)

    # Remove parentheses and contents inside them
    title = re.sub(r'\([^)]*\)', '', title)

    # Remove any extra spaces
    title = title.strip()

    # Optional: Remove trailing hyphens and spaces
    title = re.sub(r'[-–—]\s*$', '', title).strip()

    return title
