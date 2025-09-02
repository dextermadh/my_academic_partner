from langchain.schema import HumanMessage, SystemMessage 

def style_text(
    llm,
    text,
    style = 'Write this text in my own grammar and tone, keep meaning same',
):
    if not text.strip(): 
        return ''
    try: 
        response = llm.invoke([
            SystemMessage(content=style),
            HumanMessage(content=text) 
        ])
        return response.content.strip() 
    except Exception as e: 
        print(f'Error styling: {e}')
        return text