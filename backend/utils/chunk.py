def chunk_text(text, chunk_size = 200, overlap=50): 
    '''
    split text into overlapping chunks 
    '''
    words = text.split()
    chunks = []
    start = 0
    
    while start < len(words): 
        end = min(start + chunk_size, len(words))
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    
    return chunks
    