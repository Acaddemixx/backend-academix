#methods from this module will be used to load contexts and generaet text from other file types mainly image
from BasicApp.models import *
from CommunityApp.models import *
from PostApp.models import *
from pgvector.django import L2Distance
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain_core.output_parsers import StrOutputParser
import google.generativeai as vision


load_dotenv()
GOOGLE_API_KEY = os.getenv('GEMNI_API_KEY')

output = StrOutputParser()
model = vision.GenerativeModel('gemini-pro')
template = "answer this question : {question} "


def load_question(question):
    return model.generate_content([template , question]).text

def load_all(question):
    #gets the top 10 simmilar objects with the prompt_embedding and merges thier description and content
    prompt_embedding = main.embed(question)
    courses = Course.objects.order_by(L2Distance('embedding' , prompt_embedding))[:10]
    departments = Department.objects.order_by(L2Distance('embedding' , prompt_embedding))[:10]
    buildings = Building.objects.order_by(L2Distance('embedding' , prompt_embedding))[:10]
    clubs = Club.objects.order_by(L2Distance('embedding' , prompt_embedding))[:10]
    events = Event.objects.order_by(L2Distance('embedding' , prompt_embedding))[:10]
    posts = Post.objects.order_by(L2Distance('embedding' , prompt_embedding))[:10]
    comments = Comment.objects.order_by(L2Distance('embedding' , prompt_embedding))[:10]
    res = []

    for course in courses:
        res.append(course.overview )

    for department in departments:
        res.append(department.overview )

    for club in clubs:
        res.append(club.overview)

    for building in buildings:
        res.append(building.description)
    
    for event in events:
        res.append(event.description)
    
    for post in posts:
        res.append(post.content)
    
    for comment in comments:
        res.append(comment.content)
    
    res.append(load_question(question))
    
    return res

def load_picture(file):
    pass




    