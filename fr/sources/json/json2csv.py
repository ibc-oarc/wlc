import pandas as pd
import json
import sys
arg=sys.argv[1]
with open(arg) as f:
  data = json.load(f)
df=pd.DataFrame.from_dict(data["text"], orient="index")
df.to_csv(arg+".csv")
