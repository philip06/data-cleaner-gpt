import pandas as pd
import random
import faker
from random import randint, uniform, choice
import string
import csv

fake = faker.Faker()

def generate_normalization_data(num_samples):
    id_list = list(range(1, num_samples + 1))
    text_list = []
    
    for _ in range(num_samples):
        # Randomize order and content of information
        info_order = random.sample(range(5), 5)
        info_content = [
            f"My NaMe is {fake.name()}",
            f"birthDAY - {fake.date(pattern=random.choice(['%b %d, %y', '%d-%m-%Y', '%d/%m/%y']), end_datetime=None)}",
            f"email - {fake.email()}",
            f"{random.uniform(1, 10)}" + random.choice(["k", "000"]) + " earnings",
            f"Website - {fake.uri()}",
            f"special_character: {random.choice(['!', '@', '#', '$', '%', '^', '&', '*'])}"
        ]
        record = "; ".join([info_content[i] for i in info_order])
        text_list.append(record)

    df = pd.DataFrame({
        'id': id_list,
        'text': text_list
    })

    return df


def introduce_typo(word):
    """Introduce a random typo into a given word"""
    typo_position = random.randint(0, len(word) - 1)
    return word[:typo_position] + random.choice('qwertyuiopasdfghjklzxcvbnm') + word[typo_position+1:]

def introduce_randomness(title):
    """Introduce some randomness into a given title"""
    words = title.split()
    
    # Occasionally repeat a word
    if random.random() < 0.1:
        title = ' '.join(words + [random.choice(words)])

    # Occasionally swap the order of words
    if random.random() < 0.1:
        title = ' '.join(reversed(words))

    # Occasionally introduce a special character
    if random.random() < 0.1:
        title = title.replace(' ', random.choice('!@#$%^&*'))

    return title

def generate_title():
    """Generate a random job title, occasionally with a typo or randomness"""
    # Use a real job title
    title = fake.job()

    # 20% of the time introduce a typo
    if random.random() < 0.2:
        title = introduce_typo(title)

    # 30% of the time introduce some randomness
    if random.random() < 0.3:
        title = introduce_randomness(title)

    return title

# Generate 100 random titles and write to CSV
with open('random_job_titles.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "Job Title"])
    for i in range(1, 101):  # IDs start from 1
        writer.writerow([i, generate_title()])


# Generate test data with 200 examples
df = generate_normalization_data(200)

# Save the DataFrame to a CSV file
df.to_csv('denormalized_data.csv', index=False)
