from typing import Optional
from llama_cpp import Llama
from utils.api_handlers import get_news, get_weather

class HybridAssistant:
    def __init__(self):
        # Initialize Llama with Metal acceleration
        self.llm = Llama(
            model_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf",  # ARM-compatible quantized model
            n_ctx=2048,  # Context window size
            n_gpu_layers=1,  # Enable Metal acceleration (M1/M2)
            verbose=False
        )
        
    def needs_internet(self, query: str) -> bool:
        """Check if query requires live data"""
        triggers = ["weather", "news", "stock", "latest", "current", "today's"]
        return any(trigger in query.lower() for trigger in triggers)
    
    def extract_location(self, query: str) -> str:
        """Extract location from query (e.g., 'weather in Paris' -> 'Paris')"""
        # Your existing implementation
        return query.split("weather in")[-1].strip().split()[0]
    
    def extract_topic(self, query: str) -> str:
        """Extract topic from query (e.g., 'news about AI' -> 'AI')"""
        # Your existing implementation
        return query.split("about")[-1].strip().split()[0]
    
    def call_api(self, query: str) -> Optional[str]:
        """Route to appropriate API"""
        if "weather" in query:
            location = self.extract_location(query)
            return get_weather(location)
        elif "news" in query:
            topic = self.extract_topic(query)
            return get_news(topic)
        return None
    
    def generate_response(self, query: str) -> str:
        """Hybrid generation with llama.cpp"""
        if self.needs_internet(query):
            api_result = self.call_api(query)
            if api_result:
                # Format for Mistral instruct template
                prompt = f"""<s>[INST] Combine this information:
                User Question: {query}
                API Data: {api_result}
                Provide a concise, helpful response [/INST]"""
                
                output = self.llm(
                    prompt,
                    max_tokens=200,
                    temperature=0.7,
                    stop=["</s>"]
                )
                return output['choices'][0]['text']
        
        # Pure local response
        output = self.llm(
            f"<s>[INST] {query} [/INST]",
            max_tokens=200,
            temperature=0.7
        )
        return output['choices'][0]['text']