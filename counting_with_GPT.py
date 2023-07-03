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


prompt2 = f"""
    How many characters are in the string that is included below and is delimited with triple backticks

    ```zYf7gM2hK9jP3qR5x2r9Lp5sT6Qk3jzYf7gM2hK9jP3qR5x2r9Lp5sT6w8Qk3j```
    """

print("temperature: 0.2")
loop_prompts (prompt2,20, 0.2)
