# Need following installed:
# chromadb
# langchain
# openai
# pandas
# feedparser
# tiktoken


import feedparser
import pandas as pd
import chromadb
import openai
import tiktoken
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

def load_rss_to_vector_db(rss_url, db_path='chroma_db'):

  feed = feedparser.parse(rss_url)

  articles = []
  for entry in feed.entries:
    article = {
      "Title": entry.title,
      "Link": entry.link,
      "Published": entry.published,
      "Summary": entry.summary
    }
    articles.append(article)

  rss_df = pd.DataFrame(articles)

  chroma_client = chromadb.PersistentClient(path=db_path)
  collection = chroma_client.get_or_create_collection(name="rss_news")
  openai_embedding = OpenAIEmbeddings(openai_api_key="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")

  documents = []
  metadatas = []
  embeddings = []
  ids = []


  for _, row in rss_df.iterrows():

    document = f"{row['Published']} {row['Title']} {row['Summary']}"
    documents.append(document)

    embedding = openai_embedding.embed_documents([document])[0]
    embeddings.append(embedding)

    metadata = {
      "source": row["Link"],
      "type": "News"
    }
    metadatas.append(metadata)

  for i in range(len(documents)):
    doc_id = f"doc{i}"
    ids.append(doc_id)

  collection.add(
      ids = ids,
      embeddings=embeddings,
      documents=documents,
      metadatas=metadatas
  )

  print(f"Loaded {len(documents)} RSS feeds from {rss_url} into {db_path}")

  langchain_chroma = Chroma(client=chroma_client, collection_name="rss_news", embedding_function=openai_embedding,)

  return langchain_chroma


rss_url = "https://schiffgold.com/news/feed/"
vector_db = load_rss_to_vector_db(rss_url)

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

llm = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0.3, openai_api_key="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"),
    chain_type="stuff", retriever = vector_db.as_retriever()
)

from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent

conversation = "This is the current conversation: " + "\n"

while(1):

  question_template = input("You: ")
  query = ("You are an financial analyst capable of giving market updates.  Please answer the following question regarding the news: ")
  input_query = query + question_template
  response = llm.run(input_query)
  output = "\n" + "AI: " + response + "\n"
  print(output)

  # Store conversation into vector db
  conversation = conversation + "User: " + question_template + "\n" + "Your Response: " + response + "\n"


