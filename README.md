# data-cleaner-gpt

# Installation
`python3 -m pip install -r requirements.txt`

# Configuration
- Create a file called input_data.csv with the data you want to categorize
- categories.json is your main configuration file
  - you can setup 1 category and many subcategories for your data
  - set processing_column to the name of the column header you want to categorize in input_data.csv
  - set id_column to be your unique identifier, allowing you to anonymize your data
  - Doing multiple categories at the same time is untested and may require more prompt engineering
- Set question to be the question you ask GPT to determine subcategory

# Execution
`python3 clean_data.py`
