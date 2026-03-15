import os, openai
#python -m venv .venv   
#source .venv/bin/activate  (Linux/Mac)
# .venv\Scripts\Activate.ps1 (Windows)  
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv(override=True, dotenv_path="../.env.local")
my_api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key: {my_api_key[-6:]}")  # Print only last 6characters for security")

my_client = OpenAI(api_key=my_api_key)
# my_client

def ask_question_open_ai(prompt, context):

    llm_response = my_client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", 
             "content": '''
                You are an assistant who answers only based on the given context. 
                If the context does not contain the answer, respond with 'I don't know'.
             '''},
            {"role": "user", 
             "content": f"Context: {context}\n\n User Question: {prompt}"} 
        ]

    )
    return llm_response.choices[0].message.content  

if __name__ == "__main__":
    prompt = "What is Generative AI?"
    context = "Generative AI refers to a category of artificial intelligence techniques that enable machines to generate new content, such as text, images, or music, based on patterns learned from existing data."
    response = ask_question_open_ai(prompt, context)
    print(f"Response from OpenAI LLM: {response}")