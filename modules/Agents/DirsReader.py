from langchain_google_genai import ChatGoogleGenerativeAI
from utils import add_root_to_path
root_path = add_root_to_path()

from helpers import replace_input_sentence

prompt = """
you will be given a tree of dirs and files from a user of his project and you task
is too see the files and dirs from the user and choose which dirs and files are important 
and select them where this files will be given to another AI model so he can write readme file
for this files and dirs so your task is to classify the important files and dirs for the user.
note that you take prompt from user where he tells you what does he need you to focus on.

your max output should be atmost 5 files and 5 dirs (the most important one)
{input}

Instructions : 
1. Attempt the task based on the input provided.
2. Output your response.
3. Wait for human feedback.
4. If feedback is given, revise your response based on the feedback and attempt the task again.

"""


query = """ """
prompt = replace_input_sentence(prompt,query)
