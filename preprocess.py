import pandas as pd
import re

df = pd.read_csv("data/raw/comments.csv")

# hapus duplicate
df.drop_duplicates(subset=["comment"], inplace=True)

# lowercase
df["clean_comment"] = df["comment"].str.lower()

# hapus url
df["clean_comment"] = df["clean_comment"].apply(
    lambda x: re.sub(r"http\S+|www\S+", "", str(x))
)

# hapus HTML tag
df["clean_comment"] = df["clean_comment"].apply(
    lambda x: re.sub(r"<.*?>", "", str(x))
)

import html
# decode HTML entities
df["clean_comment"] = df["clean_comment"].apply(
    lambda x: html.unescape(str(x))
)

# hapus line break
df["clean_comment"] = df["clean_comment"].str.replace(
    r"\n|\r|<br>",
    " ",
    regex=True
)

# hapus entity html tersisa
df["clean_comment"] = df["clean_comment"].apply(
    lambda x: re.sub(r"&\w+;", "", str(x))
)

# hapus karakter aneh
df["clean_comment"] = df["clean_comment"].apply(
    lambda x: re.sub(r"[^a-zA-Z0-9\s]", "", x)
)

# hapus spasi berlebih
df["clean_comment"] = df["clean_comment"].apply(
    lambda x: re.sub(r"\s+", " ", x).strip()
)

# hapus kosong
df = df[df["clean_comment"] != ""]

# simpan
df.to_csv(
    "data/clean/clean_comments.csv",
    index=False,
    encoding="utf-8-sig"
)

print(df.head())
print("Total data:", len(df))