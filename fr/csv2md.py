import pandas as pd
import sys
arg=sys.argv[1]
output=sys.argv[2]
df=pd.read_csv(arg)
df.columns=["index","text"]
df["chapter"]=df["index"].apply(lambda x: int(''.join(filter(str.isdigit, x.split(",")[0])))+1)
df["verse"]  =df["index"].apply(lambda x: int(''.join(filter(str.isdigit, x.split(",")[1])))+1)
df["output"] = df.apply(lambda x: '<span class="marginnote num" label="{}:{}" name="{}-{}"><strong>{}</strong>:1</span>\n{}'.format(x["chapter"], x["verse"], x["chapter"], x["verse"], x["chapter"], x["text"]) if x["verse"]==1 else '<span class="marginnote num" label="{}:{}" name="{}-{}">{}</span>\n{}'.format(x["chapter"], x["verse"], x["chapter"], x["verse"], x["verse"], x["text"]), axis = 1)
with open(output, "w+") as fout:
  fout.write("---\ntitle: {}\nlayout: default\n---\n".format(arg)+"\n\n".join(df["output"]))
