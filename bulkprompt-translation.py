### Folow me on Linkedin
### https://linkedin.com/in/jerryscohen

## The below code imports a csv file and sends each row to GPT3.5 for translation into other languages
## You could modify the prompt template to analyze or transpose the input text in anyway you want.   Send me a DM if you need help.

import openai
import os
import json
import csv
import re


openai.api_key = os.environ["OPENAI_API_KEY"]    #this grabs my secret api key from an environment variable


#this function handles calling the openai chatcompletion api
def call_openai(prompt_id, prompt):
    messages = [{"role": "user", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(   
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0, # specifies randmonness of model output. higher numbers add more randmoness
        )
        return response.choices[0].message["content"]
    except openai.error.OpenAIError as error:
        print(f"Prompt ID: {prompt_id} Error code: {error.code}")
        return None

#sometimes openai will add an extra comma in its response which is invalid for json. this strips it out
def remove_trailing_comma(json_string):
    pattern = r",\s*}"
    replaced_string = re.sub(pattern, "}", json_string)
    return replaced_string


def read_csv(file_path, skip_header=True):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        if skip_header:
            next(reader)  # Skip the header row
        for row in reader:
            data.append(row)
    return data

def write_csv(data, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


#update the prompt_template to whatever you'd like. this is similar to a prompt you would provide chatgpt. 
# The JSON "keys" will become the column names in the output CSV
def process_text_with_gpt(input_id, input_text):

    prompt_template = f"""
        Your task is to perform the following actions on a user's input text. The input text is copied below and delimted by the characters ####. Your only output should be the JSON object described in the last step. Do not output your responses to the subsequent steps.

        1 - Translate the text to Spanish
        2 - Translate the text to French
        3 - Translate the text to Russian
        4 - JSON Output: Create a JSON object that includes the following keys: spanish, french, russian. The JSON object should represent the final output.

        Input Text:
        ####{input_text}####
    """

    gpt_response = call_openai(input_id, prompt_template)

    processed_data = {
        "id": input_id,
        "input_text": input_text
    }

    response_data = json.loads(remove_trailing_comma(gpt_response))
    processed_data.update(response_data)

    return processed_data


def process_text_from_csv(input_file_path, output_file_path):
    data = read_csv(input_file_path, skip_header=True)

    # Extract the keys names to use them for the csv header 
    processed_data_keys = None
    for row in data:
        prompt_input_id = row[0]
        prompt_input_text = row[1]
        processed_data = process_text_with_gpt(prompt_input_id, prompt_input_text)
        processed_data_keys = list(processed_data.keys())  # Extract keys from the first row
        break  # We only need keys from the first row

    if not processed_data_keys:
        print("No data found.")
        return

    with open(output_file_path, 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=processed_data_keys)
        writer.writeheader()

        for row in data:
            prompt_input_id = row[0]
            prompt_input_text = row[1]
            processed_data = process_text_with_gpt(prompt_input_id, prompt_input_text)
            writer.writerow(processed_data)

            print(f"ID:{prompt_input_id} added to output file")
    
    print("Done")


input_file_path = './python/bulkprompt/translation-import.csv'
output_file_path = './python/bulkprompt/translation-export.csv'
process_text_from_csv(input_file_path, output_file_path)
