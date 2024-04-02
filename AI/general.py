import os
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from . import loader
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GEMNI_API_KEY')

#this whole class is intended to contain the ai functionalities we want chat and content verification 
class LLM:
    def __init__(self):
        self._template = """You are an asistant chat-bot on a web social media platform designed for
            Ethiopian University students, where only educational matterials are posted, 
            a student has asked you with this question: {question},
            if the question is related to any of these context: {context},
            provide a response based on the context, else give the student a general response, that 
            fits the question asked and provide resources to where he/she could find better answers.
            """
        self._output = StrOutputParser()
        self._llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
        self.prompt = PromptTemplate.from_template(self._template)
    

    def get_context(self , question):
        question_embedding = self.embed(question)
        context_list = loader.load_all(question_embedding)
        return context_list
   
    def chat(self , question):
        chain = self.prompt | self._llm | self._output
        return chain.invoke({
            "question": question,
            "context": self.get_context(question)
        })
    
    def verify_content(self, content):
        # image to text and text spliter should be added from the loader module
        template = """classify this content:{content} as 'Educational', Non-educational' , 'Advertisement' , or 'Other'"""
        prompt = PromptTemplate.from_template(template)

        chain = prompt | self._llm | self._output

        if chain.invoke(content) == 'Educational':
            return True
        else:
            return False
