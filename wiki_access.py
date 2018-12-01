import datetime
from pathlib import Path
from time import sleep
import requests
import json
import os
import codecs
import re

# url for wikimedia api
url = "https://en.wikipedia.org/w/api.php?"

# microsecond sleep
usleep = lambda x: sleep(x/1000000.0)

# Search a specific page and return that page's data, and the other pages it points to
def search(page_title):
    params = dict (
        action = "parse",
        page = page_title,
        prop = "wikitext",
        format = "json"
    )
    try:
        response = requests.get(url=url, params=params).text
    except ConnectionError:
        print("No connection to the Internet")
        exit()
    parsed = json.loads(response)
    # remove all of the comments
    try:
        parsed_string = parsed["parse"]["wikitext"]["*"]
    except KeyError:
        return None
    if parsed_string[:9].lower() == "#redirect":
        return None
    comments = re.search(r"(<!--.*?-->)", parsed_string)
    while comments != None:
        parsed_string = parsed_string.replace(comments.group(1), "")
        comments = re.search(r"(<!--.*?-->)", parsed_string)
    parsed["parse"]["wikitext"]["*"] = parsed_string
    # find all outside page references
    references = []
    ref_string = parsed_string
    ref = re.search(r"(\[\[[^:]*?\]\])", ref_string)
    while ref != None:
        references.append(ref.group(1))
        ref_string = ref_string.replace(ref.group(1), "")
        ref = re.search(r"(\[\[[^:]*?\]\])", ref_string)
    for i in range(0, len(references)):
        if "|" in references[i]:
            references[i] = references[i][2:references[i].find("|")]
        else:
            references[i] = references[i][2:-2]
        references[i] = references[i].lower().replace("/", "slash")
    wiki_data = json.dumps(parsed, indent=4, sort_keys=True)
    return wiki_data, references

# establish a file according to the day which logs progress
def init_meta_file():
    now = datetime.datetime.today()
    date = now.strftime("%b-%d-%Y")
    log_path = Path("{}-LOG.txt".format(date))
    if not log_path.is_file():
        header = open(log_path, "w")
        header.write(date + "\n")
        header.close()
    f = open(log_path, "a")
    return f

# save progress as a page is saved
def record_meta_file(f, page_action):
    now = datetime.datetime.today()
    time = now.strftime("%H:%M:%S")
    to_write = "{} found and stored {}.json".format(time, page_action)
    f.write(to_write + "\n")

# load items that have been saved
def read_list(name):
    array = []
    if Path("{}.txt".format(name)).is_file():
        f = codecs.open("{}.txt".format(name), "r", "utf-8")
        for line in f:
            if line[-1] == "\n":
                array.append(line[:-1])
            else:
                array.append(line)
    else:
        array = []
    return array

def write_list(name, array):
    f = codecs.open("{}.txt".format(name), "w", "utf-8")
    to_write = []
    for item in array:
        to_write.append("{}\n".format(item))
    f.writelines(to_write)

def restart():
    cwd = os.getcwd()
    if Path("data").exists():
        for filename in os.listdir(cwd+"/data"):
            if Path(filename).is_file:
                os.remove("data/"+filename)
        os.rmdir("data")
    for filename in os.listdir(cwd):
        if not filename.endswith(".py") and Path(filename).is_file():
            os.remove(filename)