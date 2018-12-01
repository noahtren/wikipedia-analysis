# wikipedia-analysis
Working with wikipedia data - scraping from API and parsing with regex.

## wiki-access.py
This file contains the `search(page_title)` method which calls the wikimedia API to access the raw wikitext of a given page. Pages are defined by a string, for example, `"Cat"`. The search method returns the json file of a certain page as well as a list of all of the pages that the original page references. This allows an algorithm to start with one page and branch out to every other page in the network, which is near 5 million.
wiki-access.py also contains methods to initialize and record a meta file, which stores the progress of the api-calling algorithm. A file is generated each day and has a line for each wikipedia article that is collected.
Finally, there are two simple methods to read and write a list to a `.txt` file in UTF-8 encoding. This is used to store a list of all of the pages that have been accessed, as well as all of the pages that still need to be accessed.
The restart method simply clears the `data` folder, which is where the `.json` files are stored.

## pull-data.py
This file runs an algorithm referencing the methods of `wiki-access.py` to indefinitely access wikipedia articles and store a `.json` file for each article in a folder named `data` until every article in the network has been stored. It starts with the page `"Cat"` and cascades from there. This program is intended to be run on an AWS EC2 instance so that it can run uninterrupted.

## process.py
Once enough pages have been collected in the `data` folder, the `cleanup()` method in this file can be called from the correct working directory to read all of the `.json` files and simplify to a form without any special wikitext tags or text formatting. This will be the basis for different NLP algorithms. These simplified files will be stored in a folder called `process`.
