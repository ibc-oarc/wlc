import pandas as pd
import re
import sys
booknames = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", \
"Isaiah", "Jeremiah", "Ezekiel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Psalms", "Proverbs", "Job" , "Song of Songs", "Ruth", "Lamentations", "Ecclesiastes", "Esther", "Daniel", "Ezra", "Nehemiah", "1 Chronicles", "2 Chronicles"]
df=pd.read_csv("nrt-bti.csv", sep="\t")
df.columns = ["id", "translation", "book", "chapter", "verse", "text"]
df = df[df["translation"] == "ntr"].drop(["id", "translation"], axis = 1)
## ntr : New Russian Translation
## bti : Kulakov's translation
df["text"] = df["text"].apply(lambda x: re.sub(r'◊\[([^\]]*)\]([^µ]*)µ', r'<span class="notespan"><span class="marginnote note" label="note-\1">\2</span></span>', x))
df["output"] = df.apply(lambda x: '  - "{}.{}": |\n      {}'.format(x["chapter"], x["verse"], x["text"]), axis = 1)
for bookname in booknames:
  with open(bookname+".md", "w+") as fout:
    fout.write("---\ntitle: {}\nlayout: bibletext\nid: {}\nverses:\n{}\n---\n".format(bookname, bookname,"\n".join(df[df["book"]==bookname]["output"])))