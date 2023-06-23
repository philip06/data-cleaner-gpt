# data-cleaner-gpt

# Installation
python3 -m pip install -r requirements.txt

# Configuration
- Create a file called input_data.csv with the data you want to categorize
- Update the categories.json file to have categories for each data point you want to categorize, within those categories setup your subcategories and descriptions
- In categories.json, set column_name to the name of the column header you want to categorize in input_data.csv
- Set question to be the question you ask GPT to determine subcategory

# Execution
python3 clean_data.py
