from project import create_prompt
from project import make_request
from project import count_csv_lines
import pytest

def test_create_invalid_prompt():
    with pytest.raises(OSError):
        create_prompt("invalid.csv", 0, "words")

def test_invalid_API():
    with pytest.raises(ValueError):
        make_request("a prompt", "InvalidAPI#adsdcevrebrb")

def test_count_csv():
    with pytest.raises(OSError):
        count_csv_lines("invalid.csv")

def test_good_prompt():
    create_prompt("testing.csv", 0, "Contacts, Leads, B2B") ==  f"Please check the list of urls Im about to give you and if any of the following keywords (Contacts, Leads, B2B) are present in the websites that those urls lead to please output the url followed by a comma and 'TRUE' or 'FALSE'. Should you be unable to enter and read the website, output the url followed by a comma and 'FALSE'.\nYour output should look like this:\n\nurl1.com,TRUE\nurl2.com,FALSE\nurl3.com,TRUE\n\nHere is the list of urls I need you to check:\n\nwww.example.com", 1




