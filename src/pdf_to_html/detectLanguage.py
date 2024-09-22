from langdetect import detect, DetectorFactory

# Ensure consistent language detection results
DetectorFactory.seed = 0

class DetectLanguage:
    def __init__(self):
        """Initialize the language detector."""
        self.lang_code = "unknown"
    
    def detect_language(self, text: str):
        """Detect the language of a given text."""
        try:
            self.lang_code = detect(text)
        except Exception as e:
            print(f"Error detecting language: {e}")
            self.lang_code = "unknown"

    def get_language_code(self, text: str) -> str:
        """Detect the language code based on the provided text."""
        self.detect_language(text)
        return self.lang_code
