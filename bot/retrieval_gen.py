from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from bot.ingest import ingest_data

def generation(vector_store):
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    PRODUCT_BOT_TEMPLATE = """
    You are an ecommerce-bot who is an expert in product recommendations and customer queries.
    It analyzes product titles and reviews to provide accurate and helpful responses.
    Ensure your answers are relevant to the product context and refrain from straying off-topic.
    Your responses should be concise and informative.

    CONTEXT:
    {context}

    QUESTION: {question}

    YOUR ANSWER:
    
    """

    prompt = ChatPromptTemplate.from_template(PRODUCT_BOT_TEMPLATE)

    llm = ChatGoogleGenerativeAI(model="gemini-pro",
                 temperature=0.6, top_p=0.8)
    
    chain = ({"context":retriever,"question":RunnablePassthrough()}|prompt|llm|StrOutputParser())

    return chain

if __name__ == "__main__":
    vector_store = ingest_data("done")#parameter is done cuz ingest_data ran and DB has been created
    chain  = generation(vector_store)
    print(chain.invoke("What is the best headphone to buy?"))

