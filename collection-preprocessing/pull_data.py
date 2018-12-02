from wiki_access import *

restart()

saved = read_list("saved")
to_save = read_list("to_save")
to_save.append("Cat")

# begin collecting data
if not os.path.exists("data"):
    os.mkdir("data")

i = 0

for page in to_save:
    if page not in saved:
        meta = init_meta_file()
        result = search(page)
        if result != None:
            (data, references) = result
            for reference in references:
                if reference not in to_save and reference not in saved:
                    to_save.append(reference)
            f = open("data/{}.json".format(page), "w")
            f.write(data)
            record_meta_file(meta, page)
            #print(json.loads(data)["parse"]["wikitext"]["*"])
            meta.close()
        saved.append(page)
        to_save.remove(page)
        i = i + 1
    if i % 1000 == 0:
        write_list("saved", saved)
        write_list("to_save", to_save)