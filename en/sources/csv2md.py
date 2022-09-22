import pandas as pd
import sys
booknames = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", \
"Isaiah", "Jeremiah", "Ezekiel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Psalms", "Proverbs", "Job" , "Song of Songs", "Ruth", "Lamentations", "Ecclesiastes", "Esther", "Daniel", "Ezra", "Nehemiah", "1 Chronicles", "2 Chronicles"]
df=pd.read_csv("bible.csv", sep="\t")
df.columns = ["book", "chapter", "verse", "text"]
df["output"] = df.apply(lambda x: '  - "{}.{}": |\n      {}'.format(x["chapter"], x["verse"], x["text"]), axis = 1)
for book in set(df["book"]):
  bookname = booknames[book-1]
  with open(bookname+".md", "w+") as fout:
    fout.write("---\ntitle: {}\nlayout: bibletext\nid: {}\nverses:\n{}\n---\n".format(bookname, bookname,"\n".join(df[df["book"]==book]["output"])))