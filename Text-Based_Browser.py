import os
import sys
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style


def get_url():
    link = input().lower()
    if link != "back" and link != "exit" and "https://" not in link and "http://" not in link:
        return f"https://{link}"
    else:
        return link


def get_filename(site_url):
    filename = ""
    if site_url.startswith("https://"):
        filename = site_url[8:]
    if site_url.startswith("http://"):
        filename = site_url[7:]
    if site_url.startswith("www."):
        filename = site_url[4:]
    if "/" in filename:
        filename = filename.replace("/", ".")
    return filename


def print_user_view(r):
    soup = BeautifulSoup(r.content, 'html.parser')
    text = soup.find_all(["p", "a", "ul", "ol", "li"])
    output = []
    for line in text:
        output.append(line.text)
        if line.name == "a":
            print(Fore.BLUE + line.text + Style.RESET_ALL)
        else:
            print(line.text)
    return output


directory_name = sys.argv[1]
pages_history = []
try:
    os.mkdir(directory_name)
except FileExistsError:
    print("The directory already exist.")
else:
    print("Directory created successfully.")
while True:
    url = get_url()
    if url == "back" and pages_history:
        pages_history.pop()
        url = pages_history.pop()
    if "." in url:
        pages_history.append(url)
        request = requests.get(url)
        page_name = get_filename(url)
        page_output = print_user_view(request)
        with open(f"{directory_name}/{page_name}", "w", encoding="utf-8") as file:
            for text_line in page_output:
                file.write(text_line)
    elif url == "exit":
        break
    else:
        print("Error: wrong url.")
