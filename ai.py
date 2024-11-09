import logging
import google.generativeai as genai
from dataclasses import dataclass
from enum import Enum
import json
import time
import re
from typing import List, Tuple, Dict, Optional
import threading
import queue
from concurrent.futures import ThreadPoolExecutor

class SuggestionType(Enum):
    GRAMMAR = "grammar"
    AUTOCOMPLETE = "autocomplete"
    STYLE = "style"
    CONTEXT = "context"

@dataclass
class Suggestion:
    type: SuggestionType
    text: str
    start_index: str  # Tkinter text widget index
    end_index: str    # Tkinter text widget index
    replacement: str = None
    confidence: float = 1.0

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class GeminiChat:
    def __init__(self, gemini_token: str, chat_history: list = None) -> None:
        self.chat_history = chat_history or []
        self.GOOGLE_API_KEY = gemini_token
        genai.configure(api_key=self.GOOGLE_API_KEY)
        self.model = self._get_model()
        self.chat = self.model.start_chat(history=self.chat_history)
        logging.info("Initiated new chat model")

    def _handle_exception(self, operation: str, e: Exception) -> None:
        logging.warning(f"Failed to {operation}: {e}")
        raise ValueError(f"Failed to {operation}: {e}")

    def _get_model(self, generative_model: str = "gemini-pro") -> genai.GenerativeModel:
        try:
            logging.info("Trying to get generative model")
            return genai.GenerativeModel(generative_model)
        except Exception as e:
            self._handle_exception("get model", e)

    def send_message(self, message_text: str) -> str:
        try:
            if not self.chat:
                self.chat = self.model.start_chat(history=self.chat_history)
            
            response = self.chat.send_message(message_text, stream=True)
            response.resolve()
            logging.info("Received response from Gemini")
            return response.text
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            return "Couldn't reach out to Google Gemini. Try Again..."

    def get_chat_history(self) -> List[Dict]:
        try:
            return self.chat.history if self.chat else []
        except Exception as e:
            logging.error(f"Error getting chat history: {e}")
            return []

    def close(self) -> None:
        logging.info("Closed model instance")
        self.chat = None
        self.chat_history = []

class AIFeatures:
    def __init__(self, gemini_token: str):
        self.gemini_chat = GeminiChat(gemini_token)
        self.suggestion_queue = queue.Queue()
        self.last_text = ""
        self.last_analysis_time = 0
        self.analysis_delay = 1.0
        self.running = True
        self.suggestion_thread = None
        self.word_frequencies = {}
        self.context_cache = {}
        self.suggestion_cache = {}
        self.max_cache_size = 1000
        self._initialize_language_model()
        self._lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=3)


        
    def get_smart_autocomplete(self, current_word: str, context: str) -> List[str]:
     """Get context-aware autocomplete suggestions with retry logic"""
     if not current_word:
        return []

     # Check cache first
     cache_key = f"{current_word}:{context[-50:]}"
     if cache_key in self.suggestion_cache:
        return self.suggestion_cache[cache_key]

     prompt = f"""Given the context and current word, suggest completions:
     Context: {context}
      Current word: {current_word}
     Consider the writing style and topic.
     Return only the top 5 most relevant completions in a simple line-separated format."""

     retries = 3
     for attempt in range(retries):
        try:
            response = self.gemini_chat.send_message(prompt)
            suggestions = [s.strip() for s in response.split('\n') if s.strip()]
            with self._lock:  # Ensure thread safety
                self.suggestion_cache[cache_key] = suggestions[:5]  # Cache top 5
            return suggestions[:5]
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} - Error getting smart autocomplete: {e}")
            time.sleep(1)  # Wait before retrying

     # Fallback if all retries fail
     return self._get_frequency_based_suggestions(current_word)
   


    def _initialize_language_model(self) -> None:
        """Initialize language model preferences"""
        init_prompt = """You are a writing assistant that will help with:
        1. Grammar and style corrections
        2. Context-aware word completion
        3. Semantic suggestions
        Please provide suggestions in JSON format with specific positions and replacements."""
        
        try:
            self.gemini_chat.send_message(init_prompt)
        except Exception as e:
            logging.error(f"Error initializing language model: {e}")

    def learn_from_text(self, text: str) -> None:
        try:
            words = re.findall(r'\w+', text.lower())
            with self._lock:  # Lock the update of word frequencies
             for word in words:
              self.word_frequencies[word] = self.word_frequencies.get(word, 0) + 1

            # Trim cache if needed
            if len(self.word_frequencies) > self.max_cache_size:
                sorted_words = sorted(self.word_frequencies.items(), key=lambda x: x[1])
                self.word_frequencies = dict(sorted_words[-self.max_cache_size:])
        except Exception as e:
         logging.error(f"Error learning from text: {e}")



    def _get_frequency_based_suggestions(self, prefix: str) -> List[str]:
        """Fallback method for word completion based on learned frequencies"""
        try:
            return [word for word in self.word_frequencies.keys() 
                   if word.startswith(prefix.lower())][:5]
        except Exception as e:
            logging.error(f"Error getting frequency-based suggestions: {e}")
            return []

    def analyze_text_style(self, text: str) -> Dict[str, List[str]]:
        """Analyze text style and provide detailed feedback"""
        if not text.strip():
            return {}

        prompt = f"""Analyze the following text for:
        1. Tone and formality
        2. Sentence structure variety
        3. Word choice effectiveness
        4. Overall clarity
        Provide specific suggestions for improvement.
        
        Text: {text}
        
        Format the response with clear section headers and bullet points."""

        try:
            response = self.gemini_chat.send_message(prompt)
            return self._parse_style_analysis(response)
        except Exception as e:
            logging.error(f"Error in style analysis: {e}")
            return {}

    def _parse_style_analysis(self, response: str) -> Dict[str, List[str]]:
        """Parse style analysis response into structured feedback"""
        analysis = {
            'tone': [],
            'structure': [],
            'word_choice': [],
            'clarity': [],
            'suggestions': []
        }
        
        try:
            current_section = None
            for line in response.split('\n'):
                line = line.strip()
                if not line:
                    continue
                    
                if any(key in line.lower() for key in analysis.keys()):
                    current_section = next(key for key in analysis.keys() 
                                        if key in line.lower())
                elif current_section:
                    analysis[current_section].append(line)
        except Exception as e:
            logging.error(f"Error parsing style analysis: {e}")
            
        return analysis

    def get_context_suggestions(self, text: str, cursor_position: int) -> List[Suggestion]:
        """Get context-aware suggestions based on cursor position"""
        if not text or cursor_position < 0:
            return []

        # Extract relevant context around cursor
        context_before = text[max(0, cursor_position-100):cursor_position]
        context_after = text[cursor_position:min(len(text), cursor_position+100)]
        
        prompt = f"""Given the writing context, suggest improvements:
        Text before cursor: {context_before}
        Text after cursor: {context_after}
        
        Provide suggestions in JSON format:
        {{
            "suggestions": [
                {{
                    "text": "suggestion text",
                    "type": "completion|citation|concept|structure",
                    "confidence": 0.0-1.0
                }}
            ]
        }}"""

        try:
            response = self.gemini_chat.send_message(prompt)
            return self._parse_context_suggestions(response, cursor_position)
        except Exception as e:
            logging.error(f"Error getting context suggestions: {e}")
            return []

    def _parse_context_suggestions(self, response: str, cursor_position: int) -> List[Suggestion]:
        """Parse context suggestions into structured format"""
        suggestions = []
        try:
            data = json.loads(response)
            for item in data.get('suggestions', []):
                suggestion = Suggestion(
                    type=SuggestionType.CONTEXT,
                    text=item['text'],
                    start_index=f"1.{cursor_position}",
                    end_index=f"1.{cursor_position}",
                    confidence=item.get('confidence', 0.8)
                )
                suggestions.append(suggestion)
        except Exception as e:
            logging.error(f"Error parsing context suggestions: {e}")
            
        return suggestions

    def get_grammar_suggestions(self, text: str) -> List[Suggestion]:
        """Get detailed grammar and style suggestions"""
        if not text.strip():
            return []

        prompt = f"""Analyze the following text for grammar and style issues.
        Provide specific corrections with exact positions.
        
        Text: {text}
        
        Return in JSON format:
        {{
            "suggestions": [
                {{
                    "type": "grammar|style",
                    "position": "start,end",
                    "issue": "description",
                    "correction": "suggested correction",
                    "confidence": 0.0-1.0
                }}
            ]
        }}"""

        try:
            response = self.gemini_chat.send_message(prompt)
            return self._parse_grammar_suggestions(response, text)
        except Exception as e:
            logging.error(f"Error getting grammar suggestions: {e}")
            return []

    def _parse_grammar_suggestions(self, response: str, original_text: str) -> List[Suggestion]:
        """Parse grammar suggestions from AI response"""
        suggestions = []
        try:
            data = json.loads(response)
            for item in data.get('suggestions', []):
                start, end = map(int, item['position'].split(','))
                suggestion = Suggestion(
                    type=SuggestionType.GRAMMAR if item['type'] == 'grammar' 
                         else SuggestionType.STYLE,
                    text=item['issue'],
                    start_index=f"1.{start}",
                    end_index=f"1.{end}",
                    replacement=item['correction'],
                    confidence=item.get('confidence', 0.8)
                )
                suggestions.append(suggestion)
        except Exception as e:
            logging.error(f"Error parsing grammar suggestions: {e}")
            
        return suggestions

    def close(self) -> None:
        """Clean up resources"""
        self.running = False
        if self.gemini_chat:
            self.gemini_chat.close()