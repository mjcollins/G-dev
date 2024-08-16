import nltk
import os
import ssl

# Disable SSL certificate verification (use with caution)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Set and print NLTK data path
nltk_data_dir = os.path.expanduser("~/nltk_data")
nltk.data.path.append(nltk_data_dir)
print(f"NLTK data path: {nltk.data.path}")

def download_and_test_nltk_data():
    packages = ['punkt', 'averaged_perceptron_tagger', 'maxent_ne_chunker', 'words']
    
    for package in packages:
        print(f"Checking {package}...")
        try:
            nltk.data.find(f'{package}')
            print(f"  {package} is already available.")
        except LookupError:
            print(f"  Downloading {package}...")
            nltk.download(package, download_dir=nltk_data_dir, quiet=False)
        
        # Verify the package is now available
        try:
            nltk.data.find(f'{package}')
            print(f"  {package} is now available.")
        except LookupError:
            print(f"  ERROR: {package} is still not available after download attempt.")

    # Test NLTK functionality
    print("\nTesting NLTK functionality:")
    text = "NLTK is a leading platform for building Python programs to work with human language data."
    
    tokens = nltk.word_tokenize(text)
    print("Tokenization:", tokens[:5], "...")
    
    pos_tags = nltk.pos_tag(tokens)
    print("POS Tagging:", pos_tags[:5], "...")
    
    entities = nltk.chunk.ne_chunk(pos_tags)
    print("Named Entity Recognition:", entities)

if __name__ == "__main__":
    download_and_test_nltk_data()