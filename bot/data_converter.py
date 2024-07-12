from langchain_core.documents import Document
import pandas as pd

def data_converter():
    data = pd.read_csv(r"C:\Projects\E-Commerce-Chatbot\data\flipkart_product_review.csv")
    data = data[["product_title","review"]]

    product_list = []

    for i,row in data.iterrows():
        dict = {
            "product_name" : row["product_title"],
            "review" : row["review"]
        }
        product_list.append(dict)

    docs = []
    for dict in product_list:
        metadata = {"product_name" : dict["product_name"]}
        doc = Document(page_content = dict["review"],metadata = metadata)
        docs.append(doc)

    return docs