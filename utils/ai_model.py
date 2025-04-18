# Updated HybridAssistant class
from typing import List, Dict, Optional
from llama_cpp import Llama
from utils.api_handlers import get_news, get_weather

class HybridAssistant:
    def __init__(self):
        self.llm = Llama(
            model_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            n_ctx=4096,  # Increased context window
            n_gpu_layers=0,
            verbose=False
        )
        
    def needs_internet(self, query: str) -> bool:
        triggers = ["weather", "news", "stock", "latest", "current", "today's"]
        return any(trigger in query.lower() for trigger in triggers)
    
    def extract_location(self, query: str) -> str:
        return query.split("weather in")[-1].strip().split()[0]
    
    def extract_topic(self, query: str) -> str:
        return query.split("about")[-1].strip().split()[0]
    
    def call_api(self, query: str) -> Optional[str]:
        if "weather" in query:
            location = self.extract_location(query)
            return get_weather(location)
        elif "news" in query:
            topic = self.extract_topic(query)
            return get_news(topic)
        return None
    
    def generate_response(self, query: str, conversation_history: List[Dict[str, str]]) -> str:
        """Generate response with conversation context"""
        # Format conversation history for Mistral
        formatted_history = self._format_history(conversation_history)
        
        if self.needs_internet(query):
            api_result = self.call_api(query)
            if api_result:
                prompt = f"""{formatted_history}[INST] Combine this information:
                User Question: {query}
                API Data: {api_result}
                Provide a concise, helpful response [/INST]"""
            else:
                prompt = f"{formatted_history}[INST] {query} [/INST]"
        else:
            prompt = f"{formatted_history}[INST] {query} [/INST]"
        
        output = self.llm(
            prompt,
            max_tokens=500,
            temperature=0.7,
            stop=["</s>"],
            echo=False
        )
        
        return output['choices'][0]['text'].strip()
    
    def _format_history(self, history: List[Dict[str, str]]) -> str:
        """Format conversation history for Mistral instruct model"""
        formatted = []
        for msg in history:
            if msg["sender"] == "user":
                formatted.append(f"[INST] {msg['message']} [/INST]")
            else:
                formatted.append(msg['message'])
        return "\n".join(formatted) + "\n" if formatted else ""