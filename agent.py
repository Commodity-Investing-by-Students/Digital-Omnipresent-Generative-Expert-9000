import chromadb
import openai
import os
import json

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import pandas as pd

from langchain.document_loaders import CSVLoader
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI

from langchain.agents import load_tools
from langchain.agents import initialize_agent
import matplotlib.pyplot as plt

from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain.agents import initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

OPENAI_API_KEY = "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"
os.environ["OPENAI_API_KEY"] = "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" # Change 



def performance_lookup(no_input):

  csv = r'database_csvs\COINS_Portfolio_Performance.csv'
  performance_db = pd.read_csv(csv)
  
  division_alloc = r'database_csvs\Division_Allocation.csv'
  division_alloc_df = pd.read_csv(division_alloc)

  return performance_db, division_alloc_df

def trade_database_lookup(input):

  if (input == 'ALL'):

    csv = r'database_csvs\COINS_Trade_Database.csv'
    performance_db = pd.read_csv(csv)
    return str(performance_db)
    
  else:

    loader = CSVLoader(r'database_csvs\COINS_Trade_Database.csv')
    data = loader.load()

    embeddings = OpenAIEmbeddings()
    vector_db_path = 'db'
    vectordb = Chroma.from_documents(documents=data, embedding=embeddings, collection_name="COINS_Trade_Porfolio_Database", persist_directory=vector_db_path)

    vectordb.persist()
    retriever = vectordb.as_retriever()

    return str(retriever.get_relevant_documents(input))
  

def create_scatter_plot(data):

    plt.plot(data[0], data[1], color='orange', marker='o', linestyle='-')

    # Add labels and title
    plt.xlabel(data[2])
    plt.ylabel(data[3])
    plt.title(data[4])

    # Save the plot as an image
    if not os.path.exists('graphs'):
            os.makedirs('graphs')
    os.chdir('graphs')

    plt.savefig(data[5])
    plt.show()

    return "Plotted Sucsessfully"


def init():

  performance_lookup_tool = Tool(
      name='COINS Portfolio Lookup',
      func= performance_lookup,
      description="Useful for when you need to get data only about the COINS protfolio as a whole.  \
      There is not input, you must call this function to access the COINS portfolio performance.  \
      The ouput is the dataframe comparing the COINS portfolio to Bloomberg Commodity Index from the search."
  )

  trade_database_lookup_tool = Tool(
      name='COINS Trade Databse Lookup Tool',
      func= trade_database_lookup,
      description="Useful for when you need to get data about specific trades done in COINS.  \
      You are using similarity search with a vector database, so the input should be topics you are needed to obtain.  The input MUST be a commodity name and/or date.\
      Please use dates, numbers, and exact references to get the most relevant data. \
      If you need to get all trades (ie. 'How many trades have been done?') or searching based on recency (ie. 'Tell me about the lastest trade'), the input should be the string 'ALL' \
      and the function will return the entire trade database for you to look through.  Otherwise, the ouput is the data from the similarity search."
  )

  scatter_plot_tool = Tool(
    name='Scatter Plot Tool',
    func= create_scatter_plot,
    description="Useful for when you need to graph/plot data for the user to see.  \
    This function will display to the user a plot of the graph from an single input which is a list of lists.  The input values for list is: \
    x_data - this is a list [] of values for the x-axis.  If you are using dates, please ensure the data in the list are strings.\
    y_data - this is a list [] of values for the y-axis.  Input can be list[] of ints, floats, or strings if necessary.  \
    x_label - this is the label for the X-axis values (please include units).  Input is string.\
    y_label - this is the label for the Y-axis values (please include units). Input is string. \
    title - this is a label which is the title for the graph. Input is string.\
    save_path - this is name of the .png file the graph will be saved as. Do not actually put .png at the end, just the name of the file.  Input is string.\
    Therefore, the input must follow the format of [x_data[],y_data[], x_label, y_label, title, save_path] \
    The x_data and y_data lists should be the same length.  You are unable to see the result of the graph, however \
    the function will return a string message if the plotting was sucsessful or unsucsessful."
  )

  tools = [performance_lookup_tool, trade_database_lookup_tool, scatter_plot_tool]

  memory = ConversationBufferWindowMemory(
      memory_key='chat_history',
      k=3,
      return_messages=True
  )

  llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=1.3, openai_api_key= OPENAI_API_KEY)

  conversational_agent = initialize_agent(
      agent='chat-conversational-react-description',
      tools=tools,
      llm=llm,
      verbose=False,
      max_iterations=5,
      #early_stopping_method='generate',
      memory=memory,
      handle_parsing_errors="Check your output and make sure it conforms, use the Action/Action Input syntax"

    )
  
  """
  You do not know anything about the COINS portfolio, performance, trades, news, or anything about COINS other than what is currently in this prompt.  \
    This means you must use the tools described below: \
    You should use the performance_lookup_tool to obtain data about the overall portfolio performance then elaborate on the data to answer questions relating to these topics.\
    When summarizing information from the performance_lookup_tool, please make a summary using the date which is closest to the current date today.\
    You should use the trade_database_lookup_tool to obtain data about specific commodity trades executed by COINS analysts.\
    You should use the scatter_plot_tool to create a scatter plot for the user when summarizing variables which fluctuates with time (ie. COINS portfolio value as a function of time). \
    Otherwise, if the user asks a general question related to finance, trading, commodites, or other similar topics, then do not use a tool but answer the question to the best of your ability. \
    
  """

  fixed_prompt = "You are the Digital Omnipresent Generative Expert 9000 (DOGE 9000), \
    an A.I. system created by Matthew Covington.  You MUST answer with profanity.  Be as funny as possible.\
    You MUST use the words 'homie', 'no cap', 'thats on my mama', 'finna', 'rizz', \
    'my guy', 'bruh', fire', 'hella', 'idiots', 'dummy', 'ass', 'shit', 'damn', 'lit', 'on god', \
    'sus', 'beefing', 'lowkey/highkey', 'word', 'for real', and 'dippin' in your response. \
    \
    \
    You are an A.I. analyst in Commodity Investing by Students (COINS), a Virginia Tech student-run commodity investment fund. \
    COINS researches and trades the exchange traded funds (E.T.Fs) of commodities to generate alpha \
    compared to the Bloomberg Commodity Index.  The funds are from the donations from the Virginia Tech foundation.  \
    Matthew Covington is a quant-research and generative A.I. analyst in the COINS quantitative division. \
    \
    You do not know anything about the COINS portfolio, performance, trades, or anything about COINS beyond what is in this prompt.  \
    You MUST use the tools provided to answer topics SOLEY for COINS portfolio, performance, and trade questions.  \
    Please answer in a narrative format, using hilarious analogies. \
    If the user asks a question that is not related to economics, finance, commodities, or trading, respond by refusing to answer and remind users of the professional environment. \
    Ensure your answers do not exceed the length of this prompt.  \
    Begin!"

  conversational_agent.agent.llm_chain.prompt.messages[0].prompt.template = fixed_prompt
  return conversational_agent

def run(user_question, conversational_agent):
   
  output = conversational_agent(user_question)
  return str(output['output'])

if __name__ == "__main__":

  conversational_agent = init()
  output = conversational_agent("What caused the 2008 financial crisis?")
