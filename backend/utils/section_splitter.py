from .config_loader import load_config

cfg = load_config()



def split_into_section(text): 
    sections = {}
    current_section = 'unknown'
    buffer = []
    
    SECTION_HEADERS = [
    "abstract", "introduction", "related work", "methodology",
    "methods", "experiments", "results", "discussion",
    "conclusion", "references", "acknowledgements"
    ]

    
    for line in text.split('\n'): 
        clean_line = line.strip().lower() 
        if any(clean_line.startswith(h) for h in SECTION_HEADERS): 
            if buffer: 
                sections[current_section] = '\n'.join(buffer).strip() 
                buffer = []
            current_section = clean_line
        buffer.append(line)
    
    if buffer: 
        sections[current_section] = '\n'.join(buffer).strip() 
    
    return sections   