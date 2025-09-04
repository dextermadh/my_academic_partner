import os
import sys
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from pathlib import Path
from langchain_community.tools import DuckDuckGoSearchRun 
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory

load_dotenv() 

# Add the project root (two levels up from extract.py) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.utils.config_loader import load_config
from backend.utils.load_vectorstore import load_vectorstore, load_retriever
from backend.utils.file_utils import load_json
from backend.utils.setup_llm import setup_llm

cfg = load_config()

class Agent: 
    def __init__(self):
        self.styled_dirs = [Path(cfg['paths']['styled_raw']), Path(cfg['paths']['styled_sections'])]
        self.vectorstore = load_vectorstore()
        self.rag_llm = setup_llm('chat_model1')
        self.chat_llm = setup_llm('chat_model1')
        
    def rag_with_style(self, question: str): 
        '''Retrieve from vector DB + styled raw examples'''
        retriever = load_retriever(self.vectorstore)
        
        styled_raw = load_json(self.styled_dirs[0])
        
        # build a global style summary from styled_raw
        if styled_raw:
            style_examples = "\n\n".join(list(styled_raw.values())[:10])  # few samples
        else:
            style_examples = "Write in a clear academic style with structured arguments."
        
        docs = retriever.get_relevant_documents(question)
        context = '\n\n'.join([doc.page_content for doc in docs])
        
        # Use fallback text if empty
        context_text = context if context else "No additional context available."
        style_examples_text = style_examples if style_examples else "No student style examples provided."
        
        prompt_template = '''
        You are an academic assistant.
        ALWAYS USE this Tool eventhough you can answer without them:
        1. Studen't styled examples
        2. Retrieved academic context
        to answer the question. 
        
        Styled Examples:
        {styled_examples}
        
        Question:
        {question}
        
        Retrieved Context:
        {context}
        
        Write a final academic answer that matches the student's style.
        '''
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=['question', 'context', 'styled_examples']
        )
        
        formatted_prompt = prompt.format(
            question=question,
            context=context_text,
            styled_examples=style_examples_text
        )
        
        response = self.rag_llm.invoke(formatted_prompt)
        return response.content        
        
    def web_search(self, query: str):
         web_search = DuckDuckGoSearchRun()
         return web_search.run(query) 
     
    def team_agent(self):
        tools = [
            Tool(
                name="AcademicRAG",
                func=self.rag_with_style,
                description="Always use this to answer knowledge queries using the RAG method."
            ),
            Tool(
                name="WebsearchTool",
                func=self.web_search,
                description="Search the web for academic information"
            ),
        ]
        
        # memeory
        memory = ConversationBufferMemory(
            memory_key='chat_history', 
            return_messages=True
        )

        # Agent
        team_agent = initialize_agent(
            tools=tools,
            llm=self.chat_llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            memory=memory,
            verbose=True,
            handle_parsing_errors=True,
        )
        
        return team_agent

if __name__ == '__main__': 
    agent = Agent()
    team_agent = agent.team_agent()
    
    query = "what is the role of engineers in the current world?"
    
    response = team_agent.run(query) 
    print("Team Agent Response:\n", response)
        
         
        
            