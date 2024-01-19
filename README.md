# Digital Omnipresent Generative Expert 9000 (Doge 9000) - COINS AI Assistant 

Doge 9000 is a Python-based speech assistant that utilizes Langchain and LLMs to provide a conversational interface. In this README, we'll guide you through the steps to set up and run Doge 9000 on your local system.

## Installation

1. **Install Requirements**

   First, make sure you have Python 3.9 or higher installed on your system. Then, install the required dependencies from the `requirements.txt` file using pip:

pip install -r requirements.txt


## Getting an OpenAI API Key

2. **Get an OpenAI API Key**

To use Doge 9000, you need to obtain an API key from OpenAI. Follow these steps:

- Visit the [OpenAI website](https://openai.com).
- Sign in to your OpenAI account or create a new one.
- Navigate to the API section and generate an API key.

3. **Fill in the API Key**

Once you have your OpenAI API key, you need to fill it in the necessary files:

- `GUI.py`: Locate the variable `openai_api_key` in `GUI.py` and replace `YOUR_API_KEY_HERE` with your actual API key.

- `Agent.py`: Similarly, find the variable `openai_api_key` in `Agent.py` and replace `YOUR_API_KEY_HERE` with your API key.

4. **Running Doge 9000**

You're now ready to run Doge 9000. To start the GUI interface, open a terminal and run the following command:

streamlit run GUI.py


This will launch the Doge 9000 interface in your web browser using the streamlit library.

## Notes for Usage

- **Closing the GUI Tab**: Make sure to close the GUI tab when you're done using Doge 9000. This is important because it helps clean up and delete any audio files that were generated during the conversation. This helps save memory and ensures the smooth operation of the application.

- **Shutting Down**: When you're finished using Doge 9000, remember to properly shut down the application. You can do this by closing the script from the code terminal or using the appropriate shutdown command, depending on your operating system (ctrl + c in VS code).

