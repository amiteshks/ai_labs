import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True, dotenv_path="../.env.local")
my_api_key = os.getenv("OPENAI_API_KEY")
my_api_key[:5], my_api_key[-10:]
client = OpenAI(api_key=my_api_key)

def assert_llm_judge(question, expected_response, actual_response):
    
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": "You are an expert evaluator. Compare the Model Answer to the Reference Answer and determine if they match in meaning. Give a score of 0 to 100 based on the match in JSON format."},
            {"role": "user", "content": f"""Compare the Model Answer to the Reference Answer and determine if they match in meaning.
            Question: {question}
            Reference Answer: {expected_response}
            Model Answer: {actual_response}
            Do they match in meaning? Answer with 'Yes' or 'No' and provide a brief explanation. Also give a score of 0 to 100 based on the match in JSON format:
            {{
                "score": <number between 0 and 100>,
                "explanation": "<short explanation>"
            }}"""},
        ]
    )
    print("Question: ", question)
    print("Expected Response: ", expected_response)
    print("Actual Response: ", actual_response)
    print("--------------------------------")
    print("LLM Judge Response: ", response.choices[0].message.content)
    return response.choices[0].message.content
