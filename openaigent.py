import openai
import base64
import os
from dotenv import load_dotenv

class OpenAIgent:
# --- CONFIGURATION ---
    def __init__(self, statement, constraints, pics):
        load_dotenv()
        self.task = 'tell me what you found?'
        self.role = 'you are an AI expert'
        self.messages = []
        self.MODEL = os.getenv("gpt-4.1")  # Or "gpt-4" if 4.1 is not explicitly exposed
        self.statement = statement
        self.constraints = constraints
        self.pics = pics
        def encode_image_base64(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        def load_markdown_file(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        self.statement_content = load_markdown_file(self.statement)
        self.constraint_content = load_markdown_file(self.constraints)
        self.image_base64 = encode_image_base64(self.pics)
        openai.api_key = os.getenv('OPENAI_API_KEY')   # Replace with your actual OpenAI API key
    
    def task(self, task):
        self.task = task
    def role(self, role):
        self.role = role

    # Construct the prompt
    def messages(self):
        self.messages = [
            {"role": "system", "content": f"{self.role}"},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Here are two markdown files for context:"},
                    {"type": "text", "text": f"File 1:\n{self.statement_content}"},
                    {"type": "text", "text": f"File 2:\n{self.constraint_content}"},
                    {"type": "text", "text": "And here is an image to analyze in context:"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{self.image_base64}",
                            "detail": "high"
                        },
                    },
                    {"type": "text", "text": f"{self.task}"}
                ]
            }
        ]

    # Send to OpenAI
    def run(self):
        response = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=self.messages,
            temperature=0
        )
        return response
    
    # tooling functions
    def extract_code(self, response):
        pattern = re.compile(r'(```|~~~)(.*?)(\n.*?)(\1)', re.DOTALL)
        matches = pattern.findall(response)
        return matches

    # Print the response
