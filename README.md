# data-cleaner-gpt

# Installation
`python3 -m pip install -r requirements.txt`

# Configuration
- Create a file called input_data.csv with the data you want to categorize
- Following the example in categories.json, you can setup a category and subcategories for your data
- Doing multiple categories at the same time is untested and may require more prompt engineering
- In categories.json,
  - set processing_column to the name of the column header you want to categorize in input_data.csv
  - set id_column to be your unique identifier, allowing you to anonymize your data
- Set question to be the question you ask GPT to determine subcategory

# Execution
`python3 clean_data.py`
