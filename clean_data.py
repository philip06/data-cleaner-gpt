import json
import pandas as pd
import openai
from requests.exceptions import RetryError
from tenacity import retry, stop_after_attempt, wait_exponential

openai.api_key = ""

def load_categories(filename):
    # load the JSON file as a pandas DataFrame
    data = pd.read_json(filename)
    
    # retrieve the "categories" column as a list of dictionaries
    categories = data['categories'].tolist()

    # return the categories
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


def process_data(survey_data, categories):
    for _, row in survey_data.iterrows():
        categorized_row = {}
        for cat in categories:
            question = cat["question"]
            subcategories = [subcat["name"] for subcat in cat["subcategories"]]
            response_key = question.lower().replace(' ', '_')
            if response_key not in row:
                print(f'Key {response_key} not found in row. Skipping...')
                continue
            responses = row[response_key]
            if responses:
                categorized_responses = categorize_response(question, responses, subcategories)
                categorized_row[response_key] = categorized_responses
        new_row = {**row, **categorized_row}
        # save new row to the csv file
        new_data = pd.DataFrame([new_row])
        new_data.to_csv('newdata.csv', mode='a', header=False, index=False)

if __name__ == "__main__":
    # load data from csv
    survey_data = pd.read_csv("JobTitle.csv", encoding='ISO-8859-1')

    # load categories from json file
    categories = load_categories("categories.json")

    # process the data
    process_data(survey_data, categories)
