# code by Jerry Cohen
# https://www.linkedin.com/in/jerryscohen/
# https://github.com/jerrycohen

import openai
import os


openai.api_key = os.environ["OPENAI_API_KEY"]

def get_completion(prompt, temperature, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature, # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]
    except openai.error.OpenAIError as error:
        print(f"Error code: {error.code}")
        return None



def loop_prompts (myprompt, n, temp):

    for i in range(n):
    
        gpt_response = get_completion(myprompt, temp)
        
        print (gpt_response)


prompt1 = f"What is 2+2?"

print("temperature: 0.2")
loop_prompts (prompt1,10, 0.2)

print("temperature: 1")
loop_prompts (prompt1,10, 1)

print("temperature: 2")
loop_prompts (prompt1,10, 2)


