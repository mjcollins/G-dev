import os
import nltk
import logging
import ssl
import json
from typing import List, Dict
from api_client import AnthropicAPIClient
from config import SYSTEM_PROMPT, MAX_REQUESTS_PER_TASK
from file_utils import list_files, read_file, write_file, parse_file
from command_utils import execute_command
from code_analyzer import analyze_code, generate_code
from task_manager import TaskManager
from nlp_processor import NLPProcessor
from memory_manager import MemoryManager
from knowledge_base import KnowledgeBase
from download_nltk_data import download_nltk_data

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Disable SSL certificate verification (use with caution)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Set NLTK data path to the virtual environment
nltk_data_dir = "/Users/marcus/Documents/C-dev/venv/lib/python3.12/site-packages/nltk_data"
nltk.data.path = [nltk_data_dir]  # Use only this path

logging.info(f"NLTK data directory: {nltk_data_dir}")
logging.info(f"NLTK data path: {nltk.data.path}")

def download_nltk_data():
    packages = ['punkt', 'averaged_perceptron_tagger', 'maxent_ne_chunker', 'words']
    for package in packages:
        try:
            nltk.data.find(f'{package}')
            logging.info(f"NLTK data '{package}' is already available.")
        except LookupError:
            logging.info(f"Downloading NLTK data '{package}'...")
            nltk.download(package, download_dir=nltk_data_dir, quiet=False)

def verify_nltk_data():
    required_data = [
        ('tokenizers/punkt/english.pickle', 'punkt'),
        ('taggers/averaged_perceptron_tagger/averaged_perceptron_tagger.pickle', 'averaged_perceptron_tagger'),
        ('chunkers/maxent_ne_chunker/PY3/english_ace_binary.pickle', 'maxent_ne_chunker'),
        ('corpora/words/en', 'words')
    ]
    missing_data = []
    for file_path, package_name in required_data:
        full_path = os.path.join(nltk_data_dir, file_path)
        if os.path.exists(full_path):
            logging.info(f"NLTK data '{package_name}' found at: {full_path}")
        else:
            logging.error(f"NLTK data '{package_name}' not found at: {full_path}")
            missing_data.append(package_name)
    
    if missing_data:
        logging.warning(f"The following NLTK data packages are missing: {', '.join(missing_data)}")
    else:
        logging.info("All required NLTK data packages are available.")

# Ensure NLTK data is available
download_nltk_data()
verify_nltk_data()

# Now try to use NLTK functions
try:
    nltk.word_tokenize("This is a test sentence.")
    logging.info("NLTK word tokenization successful.")
except Exception as e:
    logging.error(f"Error during NLTK word tokenization: {str(e)}")

try:
    nltk.pos_tag(nltk.word_tokenize("This is a test sentence."))
    logging.info("NLTK POS tagging successful.")
except Exception as e:
    logging.error(f"Error during NLTK POS tagging: {str(e)}")

try:
    nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize("John lives in New York.")))
    logging.info("NLTK named entity recognition successful.")
except Exception as e:
    logging.error(f"Error during NLTK named entity recognition: {str(e)}")

# Check for NumPy
try:
    import numpy
    logging.info("NumPy is installed.")
except ImportError:
    logging.error("NumPy is not installed. Please install it using 'pip install numpy'.")
    print("Warning: NumPy is not installed. Some NLP features may not work correctly.")

class AssistantSession:
    def __init__(self):
        self.client = AnthropicAPIClient()
        self.conversation_history: List[Dict[str, str]] = []
        self.working_directory: str = os.getcwd()
        self.request_count: int = 0
        self.task_manager = TaskManager()
        try:
            self.nlp_processor = NLPProcessor()
        except Exception as e:
            logging.error(f"Error initializing NLPProcessor: {str(e)}")
            print(f"Warning: NLPProcessor initialization failed. NLP features may not be available.")
            self.nlp_processor = None
        self.memory_manager = MemoryManager()
        self.knowledge_base = KnowledgeBase()

    def get_working_directory(self) -> str:
        return self.working_directory

    def set_working_directory(self, path: str) -> str:
        if os.path.isdir(path):
            self.working_directory = os.path.abspath(path)
            return f"Working directory set to: {self.working_directory}"
        else:
            return f"Error: {path} is not a valid directory."

    def send_message_to_claude(self, message: str) -> str:
        if self.request_count >= MAX_REQUESTS_PER_TASK:
            return "Error: Maximum number of requests reached for this task. Please start a new session."
        
        self.conversation_history.append({"role": "user", "content": message})
        response = self.client.send_message(message, SYSTEM_PROMPT, self.conversation_history)
        self.conversation_history.append({"role": "assistant", "content": response})
        self.request_count += 1
        return response

    def stream_message_from_claude(self, message: str):
        if self.request_count >= MAX_REQUESTS_PER_TASK:
            yield "Error: Maximum number of requests reached for this task. Please start a new session."
            return

        self.conversation_history.append({"role": "user", "content": message})
        full_response = ""
        try:
            for chunk in self.client.stream_message(message, SYSTEM_PROMPT, self.conversation_history):
                full_response += chunk
                yield chunk
        except Exception as e:
            logging.error(f"Error streaming message to Claude API: {str(e)}")
            yield f"Error: {str(e)}"

        self.conversation_history.append({"role": "assistant", "content": full_response})
        self.request_count += 1

    def handle_file_operations(self, command: str) -> str:
        if command.startswith("list"):
            directory = self.working_directory if len(command.split()) == 1 else os.path.join(self.working_directory, command.split(None, 1)[1])
            files = list_files(directory)
            return "\n".join(files)
        elif command.startswith("read "):
            file_path = os.path.join(self.working_directory, command.split(" ", 1)[1])
            content = read_file(file_path)
            return content
        elif command.startswith("write "):
            _, rel_path, content = command.split(" ", 2)
            file_path = os.path.join(self.working_directory, rel_path)
            result = write_file(file_path, content)
            return result
        elif command.startswith("parse "):
            file_path = os.path.join(self.working_directory, command.split(" ", 1)[1])
            if not os.path.isfile(file_path):
                return f"Error: File '{file_path}' not found."
            
            parsed_data = parse_file(file_path)
            if "error" in parsed_data:
                return parsed_data["error"][0]
            
            result = f"Parsed data for {file_path}:\n"
            for key, values in parsed_data.items():
                if values:
                    result += f"{key.capitalize()}: {', '.join(values)}\n"
            return result.strip()
        elif command.startswith("cd "):
            new_dir = command.split(" ", 1)[1]
            return self.set_working_directory(os.path.join(self.working_directory, new_dir))
        elif command == "pwd":
            return f"Current working directory: {self.working_directory}"
        else:
            return "Invalid file operation command."

    def handle_system_command(self, command: str) -> str:
        if command.startswith("exec "):
            cmd = command.split(" ", 1)[1]
            output = execute_command(cmd)
            return output
        else:
            return "Invalid system command."

    def handle_code_operations(self, command: str) -> str:
        if command.startswith("analyze "):
            file_path = os.path.join(self.working_directory, command.split(" ", 1)[1])
            analysis = analyze_code(file_path)
            return json.dumps(analysis, indent=2)
        elif command.startswith("generate "):
            _, language, description = command.split(" ", 2)
            generated_code = generate_code(language, description)
            return generated_code
        else:
            return "Invalid code operation command."

    def handle_task_management(self, command: str) -> str:
        if command.startswith("task "):
            task_command = command.split(" ", 1)[1]
            return self.task_manager.handle_command(task_command)
        else:
            return "Invalid task management command."

    def handle_nlp_processing(self, command: str) -> str:
        if command.startswith("nlp "):
            nlp_command = command.split(" ", 1)[1]
            return self.nlp_processor.process(nlp_command)
        else:
            return "Invalid NLP processing command."

    def handle_memory_operations(self, command: str) -> str:
        if command.startswith("memory "):
            memory_command = command.split(" ", 1)[1]
            return self.memory_manager.handle_command(memory_command)
        else:
            return "Invalid memory operation command."

    def handle_knowledge_base(self, command: str) -> str:
        if command.startswith("kb "):
            kb_command = command.split(" ", 1)[1]
            return self.knowledge_base.query(kb_command)
        else:
            return "Invalid knowledge base command."

    def export_conversation(self, file_path: str) -> str:
        try:
            with open(file_path, 'w') as f:
                for message in self.conversation_history:
                    f.write(f"# {message['role'].capitalize()}\n\n")
                    f.write(f"{message['content']}\n\n")
            return f"Conversation exported to {file_path}"
        except Exception as e:
            return f"Error exporting conversation: {str(e)}"

def main():
    session = AssistantSession()
    print(f"Welcome to the local AI assistant. Type 'quit' to exit.")
    print(f"Current working directory: {session.get_working_directory()}")
    print(f"You have {MAX_REQUESTS_PER_TASK} requests available for this session.")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                break
            
            if user_input.startswith("file "):
                response = session.handle_file_operations(user_input[5:])
            elif user_input.startswith("system "):
                response = session.handle_system_command(user_input[7:])
            elif user_input.startswith("code "):
                response = session.handle_code_operations(user_input[5:])
            elif user_input.startswith("task "):
                response = session.handle_task_management(user_input[5:])
            elif user_input.startswith("nlp "):
                if session.nlp_processor:
                    response = session.handle_nlp_processing(user_input[4:])
                else:
                    response = "NLP processing is not available due to initialization errors."
            elif user_input.startswith("memory "):
                response = session.handle_memory_operations(user_input[7:])
            elif user_input.startswith("kb "):
                response = session.handle_knowledge_base(user_input[3:])
            elif user_input.startswith("export "):
                file_path = user_input.split(" ", 1)[1]
                response = session.export_conversation(file_path)
            else:
                response = ""
                print("Assistant: ", end="", flush=True)
                for chunk in session.stream_message_from_claude(user_input):
                    print(chunk, end="", flush=True)
                    response += chunk
                print()  # New line after the complete response
            
            if response:
                print("Assistant:", response)
            
            print(f"Requests remaining: {MAX_REQUESTS_PER_TASK - session.request_count}")
        
        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected. Type 'quit' to exit or continue with your next input.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()