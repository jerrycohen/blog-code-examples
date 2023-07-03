# code by Jerry Cohen
# https://www.linkedin.com/in/jerryscohen/
# https://github.com/jerrycohen



import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

def get_completion(messages, temperature=0.2, model="gpt-3.5-turbo"):
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

# Initial prompt to gpt
initial_prompt = f"Write a sentence about a boy named Jack and a girl named Jill. Your output should be a single sentence with 12 words. Delimit the sentence with backticks."

print (initial_prompt)
messages = [
    {"role": "user", "content": initial_prompt}
]

while True:
    completion = get_completion(messages)

    # Remove backticks
    completion_words = completion.replace("`", "").split()

    #if the response has the correct number of words then we are done. print the repsonse
    if len(completion_words) == 12:
        print(f"Assistant's response has 12 words: {completion}")
        break
    
    #if not, then tell GPT to try again
    else:
        # Append assistant and user feedback to the message list so GPT is aware of the conversation history
        feedack_prompt = f"The last message had {len(completion_words)} words. Please try again with exactly 12 words."
        
        print (feedack_prompt) #this is so the end user is aware that GPT needs to try again

        messages.append({"role": "assistant", "content": completion})
        messages.append({"role": "user", "content": feedack_prompt})
