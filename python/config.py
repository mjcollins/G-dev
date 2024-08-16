import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('ANTHROPIC_API_KEY')
API_URL = 'https://api.anthropic.com/v1/messages'

SYSTEM_PROMPT = """You are an AI assistant with access to the user's local environment. You can perform various tasks such as reading and writing files, executing commands, analyzing code, managing tasks, processing natural language, and more. Always prioritize the user's safety and privacy."""

MAX_REQUESTS_PER_TASK = 20

# Set the working directory to the user's specified directory
WORKING_DIRECTORY = os.getenv('WORKING_DIRECTORY', os.getcwd())
if not os.path.exists(WORKING_DIRECTORY):
    print(f"Warning: Specified working directory '{WORKING_DIRECTORY}' does not exist. Using current directory.")
    WORKING_DIRECTORY = os.getcwd()

# NLP settings
NLTK_DATA_PATH = os.getenv('NLTK_DATA_PATH', os.path.join(os.getcwd(), 'nltk_data'))
os.environ['NLTK_DATA'] = NLTK_DATA_PATH

# Check if required NLTK data is available
required_nltk_data = ['punkt', 'averaged_perceptron_tagger', 'maxent_ne_chunker', 'words']
for data in required_nltk_data:
    if not os.path.exists(os.path.join(NLTK_DATA_PATH, data)):
        print(f"Warning: Required NLTK data '{data}' not found. Please ensure it's downloaded.")

# Memory settings
MEMORY_STORAGE_FILE = os.getenv('MEMORY_STORAGE_FILE', 'memory.json')

# Knowledge Base settings
KNOWLEDGE_BASE_API_URL = os.getenv('KNOWLEDGE_BASE_API_URL', 'https://api.duckduckgo.com/')
