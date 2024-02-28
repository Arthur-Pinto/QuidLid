import requests
import csv
import json
import math
import os
from dotenv import load_dotenv
import sys


def check_for_csv(csvname):
    return os.path.exists(csvname)
def main():
    load_dotenv()
    API_KEY = os.environ['API_KEY']
    print("Welcome to QuidLid!\n\n")
    csvname = input("Please enter the name of the csv file: ")
    if check_for_csv(csvname) == False:
        raise ValueError("No valid csv with that name")
    print("Please enter the words that will be used to check the websites: \n")
    for i in range(3):
        if i:
            words = words+", "+input()
        else:
            words = input()
    lines = math.ceil(count_csv_lines(csvname)/5)
    band = 0
    for i in range(lines):
        prompt, aux = create_prompt(csvname, band, words)
        band += aux
        response = make_request(prompt, API_KEY)
        write_output_file(response)
    print("Done! :)")



def create_prompt(csvname, lines, words):
    links = ""
    band = 0
    with open(csvname) as file:
        reader = csv.reader(file)
        for _ in range(lines):
            next(reader)
        for Name, Link in reader:
            if band:
                links = f"{links}\n{Link}"
            else:
                links = Link
            band +=1
            if band ==5:
                break
    return f"Please check the list of urls Im about to give you and if any of the following keywords ({words}) are present in the websites that those urls lead to please output the url followed by a comma and 'TRUE' or 'FALSE'. Should you be unable to enter and read the website, output the url followed by a comma and 'FALSE'.\nYour output should look like this:\n\nurl1.com,TRUE\nurl2.com,FALSE\nurl3.com,TRUE\n\nHere is the list of urls I need you to check:\n\n{links}", band


def make_request(prompt, API_KEY):
    headers = {
    'Content-Type': 'application/json',
    }

    params = {
    'key': API_KEY,
    }

    json_data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': prompt,
                    },
                ],
            },
        ],
    }

    response = requests.post(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
        params=params,
        headers=headers,
        json=json_data,
    )
    if response.status_code != 200:
        raise ValueError("Gemini currently is at capacity or the API key is invalid")
    return response.json()['candidates'][0]['content']['parts'][0]['text']

def write_output_file(response):
    if response == None or response == "":
        raise ValueError("Response was empty")
    company_list_lines = response.splitlines()
    with open('output.csv', 'a') as file:
        writer = csv.writer(file)
        for company in company_list_lines:
            to_write = company.split(',')
            writer.writerow([to_write[0], to_write[1]])

def count_csv_lines(csvname):
    with open(csvname, 'r') as file:
        return sum(1 for line in file)



if __name__ == "__main__":
    main()
