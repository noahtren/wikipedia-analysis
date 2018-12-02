# wikipedia-analysis
This repository contains all of the code involved in pulling data from Wikipedia, parsing and simplifying it, and feeding it into a Recurrent Neural Network for the creation of machine-generated wikipedia pages! 

## Data Collection
### wiki-access.py
This file contains the `search(page_title)` method which calls the wikimedia API to access the raw wikitext of a given page. Pages are defined by a string, for example, `"cat"`. The search method returns the json file of a certain page as well as a list of all of the pages that the original page references. This list is generated through a regex search that finds all of the other wikipedia pages linked to by the contents of the page. This allows an algorithm to start with one page and branch out to pages linked by previous pages. For the demo in this repository, the data is compiled from 3,122 articles.

wiki-access.py also contains methods to initialize and record a meta file, which stores the progress of the api-calling algorithm. A file is generated each day and has a line for each wikipedia article that is collected. This would keep track of your progress for if you want to download a massive amount of Wikipedia pages individually. If you really want to access all of Wikipedia efficiently, I would recommend [wikimedia data dumps](https://dumps.wikimedia.org/).

Finally, there are two simple methods to read and write a list to a `.txt` file in UTF-8 encoding. This is used to store a list of all of the pages that have been accessed, as well as all of the pages that still need to be accessed.
The restart method simply clears the `data` folder, which is where the `.json` files are stored.

### pull-data.py
This file runs an algorithm referencing the methods of `wiki-access.py` to indefinitely access wikipedia articles and store a `.json` file for each article in a folder named `data`. It starts with the page `"Cat"` and cascades from there. This program is intended to be run on an AWS EC2 instance so that it can run uninterrupted.

## Preprocessing
### process.py
Once enough pages have been collected in the `data` folder, the `cleanup()` method in this file can be called from the correct working directory to read all of the `.json` files and removes any special wikitext tags or text formatting, and converts them to `.txt` via regex searches. The output is essentially raw text files with header formatting and very few remaining wikidata artifacts. These simplified files will be stored in a folder called `process`.

An additional method, `consolidate()` can be run after the `cleanup()` method to compress all of the data into a single text file. This is the end of preprocessing.

### main.py
This file simply calls the methods from process.py. I have generated a conslidated data file with information from 3,122 wikipedia articles which can be accessed [here](http://noahtrenaman.com/media/data.txt). This is the raw text that will be fed into the Recurrent Neural Network.

## Processing
todo
