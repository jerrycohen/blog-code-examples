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
            temperature=0.2, # specifies randmonness of model output. higher numbers add more randmoness
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

#this function is used to convert to take the json response and appended it as a row in the output csv file 
def append_json_to_csv(json_data, csv_file):
    field_names = [
        "id",
        "input_text",
        "spanish",
        "french",
        "russian"
    ]

    with open(csv_file, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)

        # Write headers if the CSV file is empty
        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(json_data)


def bulk_prompts_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        #next(reader)  # If header rower in import file then skip first row. Comment out if no header row.

        for row in reader:
            prompt_input_id = row[0]   # assumes a unique ID in the first column
            prompt_input_text = row[1]  # assumes the input text is in the second column

            #below I provided a prompt similar to using ChatGPT. I'm very careful to request that the response is in JSON so my code can reliably consume it 
            prompt = f"""
                Your task is to perform the following actions on a User's input text. The input text is copied below in triple backticks. Your only output should be the JSON object described in the last step. Do not output your responses to the subsequent steps.

                1 - Translate the text to Spanish

                2 - Translate the text to French

                3 - Translate the text to Russian

                4 - JSON Output: Create a JSON object that includes the following keys: input_text, spanish, french, russian. The JSON object should represent the final output.


                Input Text:
                ```{prompt_input_text}```
            """


            gpt_response = call_openai(prompt_input_id, prompt)
            #print (gpt_response)
            
            json_data = json.loads(remove_trailing_comma(gpt_response))  #converts json string into pythons json object
            json_data["id"] = prompt_input_id   #adds the input rows id column value to json boject
            append_json_to_csv(json_data, output_file_path)  #appends to csv output file
            print (f"ID: {prompt_input_id} added to ouput file")



input_file_path = './python/bulkprompt/bulkprompt-import.csv'  #replace with whatever location you'd like
output_file_path = './python/bulkprompt/bulkprompt-export.csv'   #replace with whatever location you'd like


bulk_prompts_from_csv(input_file_path)



