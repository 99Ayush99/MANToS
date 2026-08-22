import json
from rich import print

def extract_questions_from_json():
    with open("spider_data/train_spider.json", 'r') as file:
        data = json.load(file)
    questions = []
    for item in data:
        if item['question']:
            questions.append(item['question'])
        
    with open("spider_data/questions.txt", 'w') as outfile:
        outfile.write("\n".join(questions))

    

if __name__ == "__main__":
    extract_questions_from_json()