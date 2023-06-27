import pandas as pd
import random
import faker
import string

fake = faker.Faker()

def generate_normalization_data(num_samples):
    id_list = list(range(1, num_samples + 1))
    text_list = generate_random_text(num_samples)
    df = pd.DataFrame({'id': id_list, 'text': text_list})
    return df

def generate_random_text(num_samples):
    text_list = []
    for _ in range(num_samples):
        record = "; ".join(generate_random_info())
        text_list.append(record)
    return text_list

def generate_random_info():
    info_order = random.sample(range(5), 5)
    info_content = [
        f"My NaMe is {fake.name()}",
        f"birthDAY - {fake.date(pattern=random.choice(['%b %d, %y', '%d-%m-%Y', '%d/%m/%y']), end_datetime=None)}",
        f"email - {fake.email()}",
        f"{random.uniform(1, 10)}" + random.choice(["k", "000"]) + " earnings",
        f"Website - {fake.uri()}",
        f"special_character: {random.choice(['!', '@', '#', '$', '%', '^', '&', '*'])}"
    ]
    return [info_content[i] for i in info_order]

def introduce_typo(word):
    typo_position = random.randint(0, len(word) - 1)
    return word[:typo_position] + random.choice(string.ascii_lowercase) + word[typo_position+1:]

def introduce_randomness(title):
    words = title.split()
    title = repeat_word(words)
    title = swap_word_order(words)
    title = introduce_special_character(title)
    return title

def repeat_word(words):
    if random.random() < 0.1:
        return ' '.join(words + [random.choice(words)])
    return ' '.join(words)

def swap_word_order(words):
    if random.random() < 0.1:
        return ' '.join(reversed(words))
    return ' '.join(words)

def introduce_special_character(title):
    if random.random() < 0.1:
        return title.replace(' ', random.choice('!@#$%^&*'))
    return title

def generate_title():
    title = fake.job()
    title = introduce_typo_if_needed(title)
    title = introduce_randomness_if_needed(title)
    return title

def introduce_typo_if_needed(title):
    if random.random() < 0.2:
        return introduce_typo(title)
    return title

def introduce_randomness_if_needed(title):
    if random.random() < 0.3:
        return introduce_randomness(title)
    return title

def generate_title_data(num_samples):
    id_list = list(range(1, num_samples + 1))
    title_list = [generate_title() for _ in range(num_samples)]
    df = pd.DataFrame({'ID': id_list, 'Job Title': title_list})
    return df

def generate_and_save_data():
    # Generate test data and save to CSV
    normalization_data = generate_normalization_data(200)
    normalization_data.to_csv('denormalized_data.csv', index=False)

    # Generate random titles and write to CSV
    title_data = generate_title_data(100)
    title_data.to_csv('random_job_titles.csv', index=False)

if __name__ == "__main__":
    generate_and_save_data()
