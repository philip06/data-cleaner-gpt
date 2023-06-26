# data-cleaner-gpt

This project uses OpenAI's GPT model to categorize and normalize survey data. It uses a YAML configuration file to setup tasks and the OpenAI API for AI-powered categorization and normalization.

## Installation

To install the necessary dependencies, run the following command:
`python3 -m pip install -r requirements.txt`


## Configuration

You will need to provide the following:

- `input_data.csv`: This file contains the data you want to process. Make sure it contains all the columns mentioned in your tasks configuration file.

- `config.yaml`: This is your main configuration file where you set up the tasks for processing your data. Here's how to setup your tasks:

  - Each task has an `operation` (either 'categorize' or 'normalize'), a `question`, a `data_column`, an `id_column`, `subtasks` (for categorization), and an `output_file`.

  - The `data_column` corresponds to the name of the column in `input_data.csv` that you want to process.

  - The `id_column` should be your unique identifier, allowing you to keep track of your data records.

  - The `question` is what you ask the GPT model to guide it in processing the data.

  - The `subtasks` list is used for categorization tasks and contains the possible categories your data can fall into.

  - The `output_file` specifies the filename where the processed data for the task should be written. If not provided, the default is 'newdata.csv'.

- You can run multiple tasks in sequence, each task outputs to a separate file as specified in the config.

## Execution

Set your OpenAI API key as an environment variable, and then execute the script:

```
export OPENAI_API_KEY=<Your API Key>
python3 clean_data.py
```
