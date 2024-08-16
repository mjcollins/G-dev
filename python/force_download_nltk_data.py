import nltk
import os
import ssl
import shutil

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

def force_download_nltk_data():
    packages = ['punkt', 'averaged_perceptron_tagger', 'maxent_ne_chunker', 'words']
    
    # Remove existing nltk_data directory
    if os.path.exists(nltk_data_dir):
        print(f"Removing existing NLTK data directory: {nltk_data_dir}")
        shutil.rmtree(nltk_data_dir)
    
    # Create fresh nltk_data directory
    os.makedirs(nltk_data_dir, exist_ok=True)
    
    for package in packages:
        print(f"Downloading {package}...")
        nltk.download(package, download_dir=nltk_data_dir, quiet=False)
        
        # Verify the package is now available
        package_dir = os.path.join(nltk_data_dir, package)
        if os.path.exists(package_dir):
            print(f"  {package} is now available at {package_dir}")
            print(f"  Contents: {os.listdir(package_dir)}")
        else:
            print(f"  ERROR: {package} directory not found at {package_dir}")

    print("\nNLTK data directory structure:")
    for root, dirs, files in os.walk(nltk_data_dir):
        level = root.replace(nltk_data_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")

if __name__ == "__main__":
    force_download_nltk_data()