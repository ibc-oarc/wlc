
##############################
#######  Start here ##########
##############################


books=["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "Isaiah", "Jeremiah", "Ezekiel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Psalms", "Proverbs", "Job", "Song of Songs", "Ruth", "Lamentations", "Ecclesiastes", "Esther", "Daniel", "Ezra", "Nehemiah", "1 Chronicles", "2 Chronicles"]




import pandas as pd
print('Loading indexing information...\r',end="")    
index=pd.read_csv("_data/temp.csv",sep="\t")
# 23211	39	36	21
# number	book	chapter	verse

print('Loading verses...\r',end="")    
df=pd.read_csv("_data/TBESH_formatted.csv",sep="\t").fillna("")
df.columns = ["strongNumber", "void1", "hebWord", "lang", "void2", "void3", "void4", "root", "etym1", "etymWord1", "etym2", "etymWord2", "etym3", "etymWord3", "void5", "etymDesc", "void6", "occurences", "variants", "morphology", "heading", "content", "phonemes"]

#  0	strongNumber
#  1	void1
#  2	hebWord
#  3	lang
#  4	void2
#  5	void3
#  6	void4
#  7	root
#  8	etym1
#  9	etymWord1
# 10	etym2
# 11	etymWord2
# 12	etym3
# 13	etymWord3
# 14	void5
# 15	etymDesc
# 16	void6
# 17	occurences
# 18	variants
# 19	morphology
# 20	heading
# 21	content
# 22	phonemes



##############################
#### Preparing links #########
##############################

df["occurences"]=df["occurences"].apply(lambda x: x.split(","))
one_occurence_by_line=df[["strongNumber","occurences"]].explode("occurences")
one_occurence_by_line["occurences"]=one_occurence_by_line["occurences"].apply(force_to_int)

links_fetched = one_occurence_by_line.merge(index,left_on="occurences",right_on="number").dropna(axis=0)
links_fetched["link"]=links_fetched[["number","chapter","verse"]].apply(lambda x: """<span id="toc"><span style="color:darkgray;"> </span><a class="shadow" href="https://bh.seveleu.com/v/{}.html">{}:{}</a></span>""".format(x["number"],x["chapter"],x["verse"]).format(x["chapter"],x["verse"]), axis=1)
links_fetched=links_fetched.drop(["occurences","number","chapter","verse"], axis=1)

links_by_book = links_fetched.groupby(["strongNumber","book"])["link"].apply(", ".join)
links_by_book=links_by_book.reset_index(level=1)
links_by_book["book"]=links_by_book["book"].apply(lambda x: """<span id="toc" style="font-family:sans-serif;">{}</span>""".format(books[x-1]))
links_by_book["link"]=links_by_book["book"]+links_by_book["link"]
links_by_book=links_by_book.drop(["book"], axis=1)

links_by_Strong_number = pd.DataFrame({"links": links_by_book["link"].groupby("strongNumber").apply(" ".join)})

df=df.merge(links_by_Strong_number, left_on="strongNumber", right_index=True, how="left").fillna({"links":""})

#############################
#### Generating files #######
#############################




df["htmlcontent"]=df[["phonemes", "hebWord", "heading", "strongNumberInt", "root", "nav_prev", "nav_next", "lang", "etymDesc", "placeholder1", "placeholder2", "placeholder3", "placeholder4", "placeholder5", "links"]].apply(lambda x: lexiconEntryTemplate.format( x["etymDesc"], x["placeholder1"] , x["placeholder2"], x["placeholder3"] , x["placeholder4"] , x["placeholder5"] ,
 x["links"]), axis=1)





df=df.sort_values(by=["strongNumber"], axis=0)

massIndividualEntry="""<span id="toc"><span style="color:darkgray;">{}</span><a class="shadow" href="/w/{}.html">{} <span id="bh">{}</span></a></span>"""

df["MassLexiconLayout"]=df[["strongNumberInt","phonemes","hebWord"]].apply(lambda x: massIndividualEntry.format(x["strongNumberInt"],x["strongNumberInt"],x["phonemes"],x["hebWord"]), axis=1)


with open("LexiconMassTemplate.html", "r") as fin:
    lexiconMassTemplate = fin.read()

lexiconcontent = lexiconMassTemplate.format("".join(list(df["MassLexiconLayout"])))

with open("lexicon.html","w+") as fout:
    fout.write(lexiconcontent)

