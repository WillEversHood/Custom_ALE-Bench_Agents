from openai import OpenAI
import base64
import os
from dotenv import load_dotenv
import regex as re 
from io import BytesIO
from PIL import Image
class OpenAIgent:
# --- CONFIGURATION ---
    def __init__(self, statement, constraints, pics):
        load_dotenv()
        self.task = 'tell me what you found?'
        self.role = 'you are an AI expert'
        self.messages = []
        self.MODEL = os.getenv("MODEL")  # Or "gpt-4" if 4.1 is not explicitly exposed
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.statement_content = statement
        self.constraint_content = constraints
        self.pics = pics
        self.research = ''
    

        def encode_image_base64(image_path):
            for path, img in image_path.items():
                buffered = BytesIO()
                img.save(buffered, format='PNG')
                img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')    
                return img_base64
           # with open(image_path, "rb") as image_file:
           #     return base64.b64encode(image_file.read()).decode("utf-8")
        '''
        def load_markdown_file(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        self.statement_content = load_markdown_file(self.statement)
        self.constraint_content = load_markdown_file(self.constraints)
        '''
        self.image_base64 = encode_image_base64(self.pics)
           # Replace with your actual OpenAI API key

    def task_set(self, task):
        self.task = task
        return

    def role_set(self, role):
        self.role = role
        return

    # Construct the prompt
    def messages_set(self):
        self.messages = [
            {"role": "system", "content": f"{self.role}"},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Here are two markdown files for context and some research (if the research is present it is the most important):"},
                    {"type": "text", "text": f"File 1:\n{self.statement_content}"},
                    {"type": "text", "text": f"File 2:\n{self.constraint_content}"},
                    {"type": "text", "text": f"File 2:\n{self.research}"},
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
    def useless(self):
        return
    # Send to OpenAI
    def run(self):
        # research Application
        client = OpenAI(api_key=self.api_key)
        self.role_set('You are a talented researcher and Analyst')
        self.task_set('Your job is to research and find the best possible methods to solve the given problem given the context and image')
        self.messages_set()
        response = client.chat.completions.create(model=self.MODEL, messages=self.messages, temperature=0)
        self.research = response.choices[0].message.content
        # Engineer
        self.role_set('You are a talented optimization engineer especially known for creating solutions in cpp20')
        self.task_set('Analyze the provided research, problem statement, constraints, and image, and generate a solution written cpp20. Product should be a single block of cpp20')
        self.messages_set()
        response = client.chat.completions.create(model=self.MODEL, messages=self.messages, temperature=0)
        #print(type(response.choices[0].message.content))
        output_text = response.choices[0].message.content
        #print(output_text)
        return output_text 

    # tooling functions
    def extract_code(self, response):
        #print(type(response))
        pattern = re.compile(r'(```|~~~)(.*?)(\n.*?)(\1)', re.DOTALL)
        matches = pattern.findall(response)
        code = matches[0][2] # the third block of the regex findalll is the code and there is only one markdown file
        return code

    # Print the response
