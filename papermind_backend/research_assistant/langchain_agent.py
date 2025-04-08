from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from .utils import extract_text_from_pdf
from django.conf import settings  


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3, google_api_key=settings.GENAI_API_KEY)

# Tools
def summarize_tool(text: str) -> str:
    prompt = PromptTemplate.from_template("Summarize the following research paper:\n{text}")
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"text": text})

def insights_tool(text: str) -> str:
    prompt = PromptTemplate.from_template("Extract 3 key insights from this paper:\n{text}")
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"text": text})

def citation_tool(text: str) -> str:
    prompt = PromptTemplate.from_template("Generate a citation for this research paper:\n{text}")
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"text": text})

tools = [
    Tool(name="Summarizer", func=summarize_tool, description="Summarizes academic papers."),
    Tool(name="Insights Extractor", func=insights_tool, description="Extracts insights."),
    Tool(name="Citation Generator", func=citation_tool, description="Generates citations."),
]

# Main Agent
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


def gemini_agent(pdf_path):
    text = extract_text_from_pdf(pdf_path)

    summary = summarize_tool(text)
    insights = insights_tool(text)
    citation = citation_tool(text)

    
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    named_entities = [(ent.text, ent.label_) for ent in doc.ents]

    return {
        "summary": summary,
        "insights": insights,
        "citation": citation,
        "named_entities": named_entities
    }
