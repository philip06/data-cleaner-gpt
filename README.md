# data-cleaner-gpt

# Installation
python3 -m pip install -r requirements.txt

# Configuration
- Create a file called input_data.csv with the data you want to categorize
- Update the categories.json file to have categories for each data point you want to categorize, within those categories setup your subcategories and descriptions
- Create your question for the category, and use a snake_case version of that question as the column header for the data point you want to categorize.
  - ie: What is your job title? => what_is_your_job_title?

# Execution
python3 clean_data.py
