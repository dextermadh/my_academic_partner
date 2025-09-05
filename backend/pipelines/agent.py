import sys
import os
from pathlib import Path
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage

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
        self.rag_llm = setup_llm('chat_model')
        self.chat_llm = setup_llm('chat_model')

    def rag_with_style(self, question: str):
        retriever = load_retriever(self.vectorstore)
        styled_raw = load_json(self.styled_dirs[0])

        style_examples_text = "\n\n".join(list(styled_raw.values())[:5]) if styled_raw else "Write in a clear academic style."

        docs = retriever.get_relevant_documents(question)
        context_text = "\n\n".join([doc.page_content for doc in docs]) or "No additional context available."

        # Truncate tokens safely
        MAX_MODEL_TOKENS = 3900
        combined_text = f"Styled Examples:\n{style_examples_text}\n\nQuestion:\n{question}\n\nRetrieved Context:\n{context_text}"
        tokens = combined_text.split()
        if len(tokens) > MAX_MODEL_TOKENS:
            tokens = tokens[-MAX_MODEL_TOKENS:]
        truncated_text = " ".join(tokens)

        human_msg = HumanMessage(content=truncated_text)
        response = self.rag_llm([human_msg])
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
                description="Search the web for academic information."
            ),
        ]

        memory = ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=True,
            max_token_limit=1000
        )

        team_agent = initialize_agent(
            tools=tools,
            llm=self.chat_llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            memory=memory,
            verbose=True,
            handle_parsing_errors=True,
        )

        return team_agent
