import nltk
import os
import ssl
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Disable SSL certificate verification (use with caution)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Set NLTK data path
nltk_data_dir = os.path.expanduser("~/nltk_data")
nltk.data.path.append(nltk_data_dir)

def download_nltk_data():
    packages = ['punkt', 'averaged_perceptron_tagger', 'maxent_ne_chunker', 'words']
    
    logging.info(f"NLTK data directory: {nltk_data_dir}")
    logging.info(f"Current NLTK data path: {nltk.data.path}")

    for package in packages:
        logging.info(f"Checking {package}...")
        try:
            nltk.data.find(f"{package}")
            logging.info(f" {package} is already available")
        except LookupError:
            logging.info(f" Downloading {package}...")
            try:
                nltk.download(package, download_dir=nltk_data_dir, quiet=False)
            except Exception as e:
                logging.error(f" Failed to download {package}: {str(e)}")
                continue

        # Verify the package is now available
        try:
            nltk.data.find(f"{package}")
            logging.info(f" {package} is now available")
        except LookupError:
            logging.error(f" ERROR: {package} is still not available after download attempt")

    # Final verification
    logging.info("Final verification of all packages:")
    for package in packages:
        try:
            nltk.data.find(f"{package}")
            logging.info(f" {package} is available")
        except LookupError:
            logging.error(f" {package} is not available")

if __name__ == "__main__":
    download_nltk_data()