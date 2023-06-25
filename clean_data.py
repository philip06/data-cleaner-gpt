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
                Please categorize the following responses: 
                ###
                {responses}
                ###
                Desired Format: JSON with the key subcategory. Make sure 
                Example: {{
                    "responses": [
                        {{ 
                            "record_id":"None"
                            "subcategory":"None"
                        }}
                    ]
                }}
                """,
            },
        ],
    }

    try:
        response = openai.ChatCompletion.create(**payload)
        content = response['choices'][0]['message']['content']
        print("Response Content:", content)  # Debug statement
        responses = json.loads(content)['responses']
        return responses
    except openai.error.ServiceUnavailableError as e:
        print("Service Unavailable Error. Retrying...")
        raise RetryError(attempt=e.last_attempt)  # Raising RetryError to trigger retry with exponential backoff
    except Exception as e:
        print("Error in JSON Parse", e)
        return ["Other" for _ in responses]
    
operation_to_function_map = {
    Operation.CATEGORIZE: categorize_response,
    Operation.NORMALIZE: normalize_response,
}

def process_data(survey_data, categories, batch_size=50):
    num_rows = len(survey_data)
    for i in range(0, num_rows, batch_size):
        batch_data = survey_data.iloc[i:min(i+batch_size, num_rows)].copy()
        for cat in categories:
            question = cat.get("question")
            operation_str = cat.get("operation")
            id_column = cat.get("id_column")

            try:
                operation = Operation[operation_str.upper()]
            except KeyError:
                print(f'Operation {operation_str} not found. Skipping...')
                continue

            process_func = operation_to_function_map[operation]
            subcategories = [subcat.get("name") for subcat in cat.get("subcategories", [])]
            response_key = cat.get("processing_column")

            batch_responses = batch_data[response_key].tolist()
            batch_ids = batch_data[id_column].tolist()

            if batch_responses and batch_ids:
                responses_stringified = "\n".join([f"{id_},{resp}" for id_, resp in zip(batch_ids, batch_responses)])
                processed_responses = process_func(question, responses_stringified, subcategories)
                processed_subcategories = [resp['subcategory'] for resp in processed_responses]
                
                batch_data.loc[:, response_key] = processed_subcategories

            new_data = pd.DataFrame(batch_data)
            mode = 'a' if i > 0 else 'w'  # write mode, use 'a' for append if it's not the first batch
            new_data.to_csv('newdata.csv', mode=mode, header=(i == 0), index=False)


if __name__ == "__main__":
    # load data from csv
    survey_data = pd.read_csv("input_data.csv", encoding='ISO-8859-1')

    # load categories from json file
    categories = load_categories("categories.json")

    # process the data
    process_data(survey_data, categories)
