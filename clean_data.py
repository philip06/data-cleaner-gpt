import json
import pandas as pd
import openai
from requests.exceptions import RetryError
from tenacity import retry, stop_after_attempt, wait_exponential
from enum import Enum

openai.api_key = ""

class Operation(Enum):
    CATEGORIZE = "categorize"
    NORMALIZE = "normalize"

# Dummy function
def normalize_response(question, responses, subcategories):
    normalized_response = responses.lower()
    return normalized_response


def load_categories(filename):
    data = pd.read_json(filename)
    
    categories = data['categories'].tolist()

    return categories

@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def categorize_response(question, responses, subcategories):
    payload = {
        "model": "gpt-3.5-turbo",
        "temperature": 0,
        "messages": [
            {
                "role": "system",
                "content": "You are a survey response classifier taking user response "
                           "and converting it to the most likely subcategories provided",
            },
            {
                "role": "assistant",
                "content": f"""
                Question: {question}
                Here are the possible subcategories: {', '.join([subcat['name'] if isinstance(subcat, dict) else subcat for subcat in subcategories])}. 
                Please categorize the following response: 
                ###
                {responses}
                ###
                Desired Format: JSON with the key subcategory.
                Example: {{ "subcategory":"None"}}
                """,
            },
        ],
    }

    try:
        response = openai.ChatCompletion.create(**payload)
        content = response['choices'][0]['message']['content']
        print("Response Content:", content)  # Debug statement
        subcat = json.loads(content)['subcategory']
        return subcat
    except openai.error.ServiceUnavailableError as e:
        print("Service Unavailable Error. Retrying...")
        raise RetryError(attempt=e.last_attempt)  # Raising RetryError to trigger retry with exponential backoff
    except Exception as e:
        print("Error in JSON Parse", e)
        return 'Other'
    
operation_to_function_map = {
    Operation.CATEGORIZE: categorize_response,
    Operation.NORMALIZE: normalize_response,
}

def process_data(survey_data, categories):
    for _, row in survey_data.iterrows():
        processed_row = {}
        for cat in categories:
            question = cat.get("question")
            operation_str = cat.get("operation")
            try:
                operation = Operation[operation_str.upper()]
            except KeyError:
                print(f'Operation {operation_str} not found. Skipping...')
                continue

            process_func = operation_to_function_map[operation]
            
            subcategories = [subcat.get("name") for subcat in cat.get("subcategories", [])]
            response_key = cat.get("column_name")
            
            if response_key not in row:
                print(f'Key {response_key} not found in row. Skipping...')
                continue
                
            responses = row[response_key]
            if responses:
                processed_responses = process_func(question, responses, subcategories)
                processed_row[response_key] = processed_responses

        new_row = {**row, **processed_row}
        # save new row to the csv file
        new_data = pd.DataFrame([new_row])
        new_data.to_csv('newdata.csv', mode='a', header=False, index=False)


if __name__ == "__main__":
    # load data from csv
    survey_data = pd.read_csv("input_data.csv", encoding='ISO-8859-1')

    # load categories from json file
    categories = load_categories("categories.json")

    # process the data
    process_data(survey_data, categories)
