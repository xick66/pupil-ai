import os
import PIL.Image
import google.generativeai as genai
from google.generativeai.types import content_types
from dotenv import load_dotenv
from .prompts import SYSTEM_PET, SYSTEM_VISION, MODEL_AFFIRM

# import sys
# sys.path.append('../search')

from search.searcher import Searcher
from search.serper import Serper

load_dotenv()

def list_files(directory):
    dir_len = len(directory)
    file_list = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if not file.startswith('.'):
                file_list.append(os.path.join(root, file)[dir_len:])
    return file_list

class GeminiLLM():
    def __init__(self, max_n_history=20):
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

        self.chat_model = genai.GenerativeModel('gemini-pro')
        self.vision_model = genai.GenerativeModel('gemini-pro-vision')

        self.search = Searcher()
        self.serper = Serper()

        self.vision_prompt = SYSTEM_VISION
        self.system_prompt = SYSTEM_PET
        self.affirm = MODEL_AFFIRM

        self.content_to_prepend = [
            content_types.to_content({"role": "user", "parts": SYSTEM_PET}), 
            content_types.to_content({"role": "model", "parts": MODEL_AFFIRM})
        ]

        self.chat = self.chat_model.start_chat(history=self.content_to_prepend)
        self.max_n_history = max_n_history

    def prepend_system_prompt(self, clean_history):
        return [*self.content_to_prepend, *clean_history]

    def pop_history(self):
        if len(self.chat.history[2:]) <= self.max_n_history:
            return
        
        chats = self.chat.history[2:]
        self.chat.history = self.prepend_system_prompt(chats[2:])
    
    def reset_history(self):
        self.chat.history = []

    def query(self, prompt):
        response = self.chat.send_message(prompt)
        self.pop_history()
        return response.text
        
    def query_with_image(self, image, prompt=None):
        if prompt is None:
            prompt = self.vision_prompt
        
        img = PIL.Image.open(image)
        safe = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
        
        described = self.vision_model.generate_content(["Describe what's on the image in detail", img], safety_settings=safe)
        described.resolve()
        additional_response = self.query("Given a description:\n" + described.text + "\nIs the description has anything related to what's have been discussed by us? If there's then answer with \"Yes\" as the first word, otherwise \"No\" as the first word" )

        response = self.vision_model.generate_content([prompt, img], safety_settings=safe)
        response.resolve()

        c = content_types.to_content({"role": "user", "parts": prompt})
        self.chat.history.append(c)
        c = content_types.to_content({"role": "model", "parts": response.text})
        self.chat.history.append(c)
        self.pop_history()

        initial_response = response.text
        
        return {"initial_response": initial_response, "additional_response": additional_response}
    
    def query_directory(self, directory):
        all_files = list_files(directory)
        all_files = str(all_files)

        prompt = f"Given a directory named {directory}\n"
        prompt += "\n"
        prompt += f"And all the files names and its subdirectories inside\n"
        prompt += f"{all_files}\n"
        prompt += "\n"
        prompt += "Interpret or figure out what is the main content of the given directory by knowing the filenames and the subdirectorie names only.\n"
        prompt += "And any thoughts or insights or comments regarding the directory? maybe something that can be improved?"

        response = self.chat.send_message(prompt)
        self.pop_history()
        return response.text
    
    def query_search(self, query:str, include_full_url:bool = False,    searcher_kwargs = {}, serper_kwargs = {}):
        response_serp = self.serper.get_answer(query=query, kwargs=serper_kwargs)

        if response_serp is None:
            response_search = self.search.search(query=query, include_full_url=include_full_url, kwargs=searcher_kwargs)
            response_search = response_search['answer']
            response = response_search

            prompt = "Given user asked somebody with this query: " + query
            prompt += "\n"
            prompt += "And the user received answer: " + response
            prompt += "\n"
            prompt += "Consider the answer and give your own answer or reconstruct to a new sentence so that the answer feels friendly, remember that you are a teacher and you are very polite and known for explaining things in a simpler and polite way. explain as if you are explaining to a neurodiverse and blind kids who are in the age group of 5 to 16yo. The kid usually studies NCERT syllabus from Diksha portal."

            gemini_response = self.query(prompt)
            response = gemini_response
            self.pop_history()
            
        else:
            response = response_serp
            prompt = "Given user web searched with this query: " + query
            prompt += "\n"
            prompt += "And the user received answer: " + response
            prompt += "\n"
            prompt += "Reconstruct to a new sentence so that the answer feels easy and fun to understand and polite, be really kind, explain in the simplest way possible, explain as if you are explaining to neurodiverse and blind students but don't mention that."
            response = self.query(prompt)
            self.pop_history()

        # self.append_history(query, response)
        # self.pop_history()

        return response

    def append_history(self, user_query, model_response):
        c = content_types.to_content({"role": "user", "parts": user_query})
        self.chat.history.append(c)
        c = content_types.to_content({"role": "model", "parts": model_response})
        self.chat.history.append(c)

if __name__ == "__main__":
    gemini = GeminiLLM()

    response = gemini.query_search("what time is it now in India?")
    print(response)
    print(gemini.chat.history)

    response = gemini.query("What's the best things to do at this time?")
    print(response)
    print(gemini.chat.history)
