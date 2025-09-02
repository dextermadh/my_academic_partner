import re
import string

def clean_text(text: str) -> str :
    '''
    cleans extracted academic answers.
    adjust rules based on your dataset
    '''
    # lowercase
    text = text.lower() 
    
    # remove extra whitespaces
    text = re.sub(r'\s+', '', text).strip()
    
    # remove numbers and punctuation
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # remove multiple new lines -> single new line
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    
    # remove extract spaces
    text = re.sub(r'[ \t]+', ' ', text)
    
    # remove page numbers 
    text = re.sub(r'Page\s*\d+', '', text, flags=re.IGNORECASE) 
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"–\s*\d+\s*–", "", text)    
    text = re.sub(r"P a g e \W \d+", "", text)
    
    text = re.sub(r"\d\) .*", "", text)
    text = re.sub(r"(\d\)|(\d.|(\d.\d)|(\d.\d.\d|\d))) .*", "", text)
    
    # remove dates
    text = re.sub(r"\d{2}\/\d{2}\/\d{4}", "", text)
    text = re.sub(r'\d{4}\/\d{2}\/', "", text)
    text = re.sub(r'\d{2}\/\d{2}\/\d+', "", text)
    
    # Remove references section if present
    text = re.sub(r"(References|BIBLIOGRAPHY).*", "", text, flags=re.IGNORECASE | re.DOTALL)
    
    # remove web links
    text = re.sub(r'https:\/\/.*', "",text)
    
    text = re.sub(r'(Name:|(S|s) number:|Registration Number:) (L.B.D.M.A. Wijesundara|(S|s)\d+|\d+)', "", text)
    text = re.sub(r'(\S+|\S+ \S+) - s\d+', '', text)
    
    # remove table of contents
    text = re.sub(r'\w+\.{5,}\d+', "", text)
    text = re.sub(r'(\w+) \.{5,}', '', text)
    text = re.sub(r'\w+\.{10,} \d', '', text)
    
    # other things to remove
    text = re.sub(r'Student \d\(\w+ \w+\) .{10,}', '', text)
    
    
    # normalize the quotes and dashes 
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("’", "'").replace("–", "-")
    
    # remove non-ASCII junk (optional)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    text = text.strip()
    return text 

def apply_clean(df_raw, df_sections): 
    # apply cleaning to raw documents
    df_raw['cleaned_text'] = df_raw['raw_text'].apply(clean_text)
    df_raw = df_raw.dropna()     
    
    # filter out empty or whitespace only strings in raw documents
    df_raw = df_raw[df_raw['cleaned_text'].str.strip() != '']
    
    # apply cleaning to sectioned documents 
    df_sections['cleaned_content'] = df_sections['content'].apply(clean_text)
    df_sections = df_sections.dropna()

    df_sections = df_sections[df_sections['cleaned_content'].str.strip() != '']
    
    return df_raw, df_sections