import os
import nltk
import logging
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk

logging.basicConfig(level=logging.INFO)

# Set NLTK data path
nltk_data_dir = os.path.expanduser("~/nltk_data")
nltk.data.path.append(nltk_data_dir)

def download_nltk_data():
    packages = ['punkt', 'averaged_perceptron_tagger', 'maxent_ne_chunker', 'words']
    for package in packages:
        try:
            nltk.data.find(f'{package}')
            logging.info(f"NLTK data '{package}' is available.")
        except LookupError:
            logging.info(f"Downloading NLTK data '{package}'...")
            nltk.download(package, download_dir=nltk_data_dir, quiet=False)

# Ensure NLTK data is available
download_nltk_data()

class NLPProcessor:
    def tokenize(self, text):
        try:
            return word_tokenize(text)
        except Exception as e:
            logging.error(f"Error in tokenization: {str(e)}")
            return []

    def pos_tag(self, tokens):
        try:
            return pos_tag(tokens)
        except Exception as e:
            logging.error(f"Error in POS tagging: {str(e)}")
            return []

    def ner(self, text):
        try:
            tokens = word_tokenize(text)
            pos_tags = pos_tag(tokens)
            return ne_chunk(pos_tags)
        except Exception as e:
            logging.error(f"Error in NER: {str(e)}")
            return None

    def process(self, command):
        parts = command.split(maxsplit=1)
        if len(parts) < 2:
            return "Invalid NLP command. Use 'tokenize', 'pos', or 'ner' followed by the text to analyze."
        
        operation, text = parts
        
        if operation == "tokenize":
            tokens = self.tokenize(text)
            return f"Tokens: {tokens}"
        elif operation == "pos":
            tokens = self.tokenize(text)
            pos_tags = self.pos_tag(tokens)
            return f"POS Tags: {pos_tags}"
        elif operation == "ner":
            ner_result = self.ner(text)
            return f"Named Entities: {ner_result}"
        else:
            return "Invalid NLP operation. Use 'tokenize', 'pos', or 'ner'."

def main():
    nlp = NLPProcessor()
    
    # Test tokenization
    text = "Hello, how are you doing today?"
    tokens = nlp.tokenize(text)
    print("Tokens:", tokens)
    
    # Test POS tagging
    pos_tags = nlp.pos_tag(tokens)
    print("POS Tags:", pos_tags)
    
    # Test NER
    ner_result = nlp.ner(text)
    print("Named Entities:", ner_result)
    
    # Test process method
    print(nlp.process("tokenize This is a test sentence."))
    print(nlp.process("pos This is another test sentence."))
    print(nlp.process("ner John lives in New York."))

if __name__ == "__main__":
    main()