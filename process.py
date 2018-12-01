import os
import pathlib
import json
import re
import codecs
from tqdm import tqdm

def vocab_from_wiki():
    cwd = os.getcwd()
    vocab = []
    for filename in os.listdir(cwd+"/data"):
        vocab.append(filename.replace(".json", ""))
    return vocab

def raw_text(name):
    f = open("data/{}.json".format(name), "r")
    text = json.loads(f.read())["parse"]["wikitext"]["*"]
    if text[:9].lower() == "#redirect":
        return None
    # eliminate headers
    if text[0] in "{\}/|[]_\n":
        text = re.search(r"[}\]|]\n+([^ _\n<>*{}|[\][a-z\]](?s).*)", text).group(1)
    # eliminate brackets that link to other pages
    result = re.search(r"(\[\[[^\[\]][^:\[\]]+?\|[^\[\]]*\]\])", text)
    while result != None:
        string = result.group(1)
        swap = re.search(r"\|(.*?)\]\]", string).group(1)
        text = text.replace(string, swap)
        result = re.search(r"(\[\[[^\[\]][^:\[\]]+?\|[^\[\]]*\]\])", text)
    result = re.search(r"(\[\[[^\[\]][^:]+?\]\])", text)
    while result != None:
        string = result.group(1)
        swap = string.replace("[", "")
        swap = swap.replace("]", "")
        text = text.replace(string, swap)
        result = re.search(r"(\[\[[^\[\]][^:]+?\]\])", text)
    # remove standalone ref tags
    while re.search(r"(<ref(?s)[^>]*?\/>)", text) != None:
        text = text.replace(re.search(r"(<ref(?s)[^>]*?\/>)", text).group(1), "")
    # remove ref tags and contents
    while re.search(r"(<ref(?s).*?<\/re.+?>)", text) != None:
        text = text.replace(re.search(r"(<ref(?s).*?<\/re.+?>)", text).group(1), "")
    # remove bolding
    result = re.search(r"(''+)[^'].*?(''+)", text)
    while result != None:
        text = text.replace(result.group(1), "")
        text = text.replace(result.group(2), "")
        result = re.search(r"(''+)[^'].*?(''+)", text)
    # simplify conversion units
    result = re.search(r"((?i)..convert\|.*?\|.*?\|[^ ]*)", text)
    while result != None:
        string = result.group(1)
        if string[0] != "{":
            string = string[2:]
        swap = re.search(r"(?i)convert\|(.*?\|.*?)\|[^ ]*", string).group(1)
        text = text.replace(string, swap)
        result = re.search(r"((?i)..convert\|.*?\|.*?\|[^ ]*)", text)
    # remove files
    result = re.search(r"(\[\[(?i)file:.*?\]\])", text)
    while result != None:
        string = result.group(1)
        text = text.replace(string, "")
        result = re.search(r"(\[\[(?i)file:.*?\]\])", text)
    # remove main article tag
    result = re.search(r"(\{\{(?i)main.*?\}\})", text)
    while result != None:
        string = result.group(1)
        text = text.replace(string, "")
        result = re.search(r"(\{\{(?i)main.*?\}\})", text)
    # remove see also
    result = re.search(r"(\{\{(?i)see also.*?\}\})", text)
    while result != None:
        string = result.group(1)
        text = text.replace(string, "")
        result = re.search(r"(\{\{(?i)see also.*?\}\})", text)
    # remove update
    result = re.search(r"(\{\{(?i)update.*?\}\})", text)
    while result != None:
        string = result.group(1)
        text = text.replace(string, "")
        result = re.search(r"(\{\{(?i)update.*?\}\})", text)
    # remove citation needed
    result = re.search(r"(\{\{(?i)citation needed.*?\}\})", text)
    while result != None:
        string = result.group(1)
        text = text.replace(string, "")
        result = re.search(r"(\{\{(?i)citation needed.*?\}\})", text)
    # remove who tag
    result = re.search(r"(\{\{(?i)who.*?\}\})", text)
    while result != None:
        string = result.group(1)
        text = text.replace(string, "")
        result = re.search(r"(\{\{(?i)who.*?\}\})", text)
    # remove expand section
    result = re.search(r"(\{\{(?i)expand.*?\}\})", text)
    while result != None:
        string = result.group(1)
        text = text.replace(string, "")
        result = re.search(r"(\{\{(?i)expand.*?\}\})", text)
    # remove clarify
    result = re.search(r"(\{\{(?i)clarify.*?\}\})", text)
    while result != None:
        string = result.group(1)
        text = text.replace(string, "")
        result = re.search(r"(\{\{(?i)clarify.*?\}\})", text)
    # remove image
    result = re.search(r"(\[\[(?i)image.*?\]\])", text)
    while result != None:
        string = result.group(1)
        text = text.replace(string, "")
        result = re.search(r"(\[\[(?i)image.*?\]\])", text)
    # remove all text formatting
    text = text.replace("&nbsp;", "")
    text = text.replace("<small>", "").replace("</small>", "").replace("<sub>", "").replace("</sub>", "").replace("<sup>","").replace("</sup>","")
    return text

def cleanup():
    vocab = vocab_from_wiki()
    if not pathlib.Path("process").is_dir():
        os.mkdir("process")
    for word in tqdm(vocab):
        if raw_text(word) != None:
            f = codecs.open("process/{}.txt".format(word), "w", "utf-8")
            f.write(raw_text(word))

# todo
# eliminate ref tags including contents
# eliminate sub tags but not contents