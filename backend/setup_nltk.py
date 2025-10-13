import nltk
import ssl

def perform_full_nltk_setup():
    """
    Performs a comprehensive download of essential NLTK data packages.
    This is a one-time setup script to prevent all future LookupErrors.
    """
    print("--- Starting Comprehensive NLTK Setup ---")

    # This is a workaround for a common SSL certificate issue on some systems.
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
        print("✅ Applied SSL context workaround for downloader.")

    # A comprehensive list of packages needed for tokenization, POS tagging,
    # named entity recognition, and other common NLP tasks.
    packages = [
        "punkt",          # Sentence Tokenizer
        "stopwords",      # Stopwords for various languages
        "averaged_perceptron_tagger", # Part-of-speech tagger
        "words",          # A corpus of English words
        "maxent_ne_chunker", # The standard Named Entity Chunker
    ]

    print("\nDownloading required NLTK packages...")
    for package in packages:
        try:
            print(f"   -> Downloading '{package}'...")
            nltk.download(package, quiet=True)
            print(f"      '{package}' downloaded successfully.")
        except Exception as e:
            print(f"      ❌ Failed to download '{package}': {e}")

    print("\n--- NLTK Setup Complete ---")
    print("You can now restart your main application server.")

if __name__ == "__main__":
    perform_full_nltk_setup()