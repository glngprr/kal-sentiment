import pandas as pd
import re
import html

INPUT_FILE = "data/raw/comments.csv"
OUTPUT_FILE = "data/clean/clean_comments_v2.csv"

# LOAD DATA

df = pd.read_csv(INPUT_FILE)

# pastikan kolom comment ada
if "comment" not in df.columns:
    raise ValueError("Kolom 'comment' tidak ditemukan")

# hapus null
df = df.dropna(subset=["comment"])

# hapus duplicate komentar mentah
df = df.drop_duplicates(subset=["comment"])

# CLEANING FUNCTION

def clean_text(text):

    text = str(text)

    # decode html
    text = html.unescape(text)

    # lowercase
    text = text.lower()

    # hapus html tag
    text = re.sub(r"<[^>]+>", " ", text)

    # hapus url
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # hapus timestamp youtube
    text = re.sub(r"\b\d{1,2}:\d{2}(:\d{2})?\b", " ", text)

    # hapus mention
    text = re.sub(r"@\w+", " ", text)

    # hashtag -> simpan teksnya
    # #tolakblokir -> tolakblokir
    text = re.sub(r"#(\w+)", r"\1", text)

    # hapus emoji
    text = re.sub(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002700-\U000027BF"
        "\U000024C2-\U0001F251"
        "]+",
        " ",
        text,
    )

    # hapus karakter selain huruf, angka, spasi
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # rapikan spasi
    text = re.sub(r"\s+", " ", text).strip()

    return text

# APPLY CLEANING

df["clean_comment"] = df["comment"].apply(clean_text)

# FILTER

# hapus kosong
df = df[df["clean_comment"] != ""]

# hapus yang hanya angka
df = df[
    ~df["clean_comment"].str.match(
        r"^[0-9\s]+$",
        na=False
    )
]

# SAVE

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("Total data:", len(df))
print(df[["comment", "clean_comment"]].head())
