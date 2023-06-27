# OpenAI Data Processing Tool

This tool is designed to perform various data operations like categorization, normalization, and enrichment using OpenAI's GPT-3.5-turbo model. 

## Prerequisites

1. Python 3.7 or above installed
2. OpenAI API key. You can get it by creating an account at https://beta.openai.com/signup/.

## Installing Required Packages

All required Python packages are listed in `requirements.txt` file. You can install all of them by running the following command in your terminal:

```bash
python3 -m pip install -r requirements.txt
```

## Configuration

The tool uses a YAML configuration file named config.yaml where you define the tasks you want to execute. The tasks include:

categorize: Categorizes provided responses according to predefined categories
normalize: Normalizes text data according to specified rules
enrich: Enriches the data with additional relevant information
Each task should be specified in the following way:

```yaml
tasks:
  - operation: "operation_name" # one of "categorize", "normalize", "enrich"
    context: "context_for_operation" # context or rules for the operation
    input_file: "input_file.csv" # input file containing the data
    output_file: "output_file.csv" # output file where results will be stored
    data_column: "column_name" # name of the column in the CSV that contains the data to be processed
    model: "gpt-3.5-turbo-16k" # OpenAI model to use
    batch_size: 50 # number of rows to process at a time
    id_column: "id" # column name of the ID column
    subcategories: # only for "categorize" operation, list of possible categories
      - name: category_name
        description: category_description
```

## Running the Tool

To run the tool, you will need to set the OPENAI_API_KEY environment variable to your OpenAI API key. You can do it in the terminal by running:

```bash
export OPENAI_API_KEY='your-api-key'
```

Or you can set it programmatically before running the script:

```python
import os
os.environ["OPENAI_API_KEY"] = 'your-api-key'
```
To execute the tasks, run the script as follows:

```bash
python3 clean_data.py
```

## Output

The output for each task will be written to the CSV file specified in the output_file parameter for each task in the config.yaml. The output will be appended to the existing data in the file.

## Debugging

In case of errors or exceptions, the script will print an error message in the console. The most common exceptions are OpenAI's `ServiceUnavailableError` (when the OpenAI API service is temporarily unavailable) and `KeyError` (when an operation name does not exist).

## Example

Here's an example config.yaml that uses all three operations:

The tool uses a YAML configuration file named config.yaml where you define the tasks you want to execute. Here's an example config.yaml:
```yaml
tasks:
  - operation: "categorize"
    context: "What is your job title?"
    input_file: "random_job_titles.csv"
    output_file: "job_title_processed.csv"
    data_column: "job_title"
    model: "gpt-3.5-turbo-16k"
    batch_size: 50
    id_column: "id"
    subcategories:
      - name: Executive Leadership
        description: Roles at the senior-most level of an organization, responsible for overall strategic direction and decision-making
      - name: Other
        description: Any role that does not fit into one of the other categories mentioned above.
  
  - operation: "normalize"
    input_file: "denormalized_data.csv"
    output_file: "normalized2.csv"
    data_column: "text"
    model: "gpt-3.5-turbo-16k"
    batch_size: 50
    id_column: "id"
  
  - operation: "enrich"
    input_file: "random_job_titles.csv"
    output_file: "enriched_data.csv"
    data_column: "job_title"
    model: "gpt-3.5-turbo-16k"
    batch_size: 50
    id_column: "id"
```