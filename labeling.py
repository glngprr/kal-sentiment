import pandas as pd
import re

# =====================
# LOAD DATASET
# =====================

df = pd.read_csv(
    "data/clean/clean_comments_v2.csv"
)

# =====================
# LOAD INSET
# =====================

positive = pd.read_csv(
    "lexicon/positive.tsv",
    sep="\t"
)

negative = pd.read_csv(
    "lexicon/negative.tsv",
    sep="\t"
)

# gabung lexicon
lexicon = {}

for _, row in positive.iterrows():
    lexicon[str(row["word"]).lower()] = int(row["weight"])

for _, row in negative.iterrows():
    lexicon[str(row["word"]).lower()] = int(row["weight"])

# =====================
# NEGATION WORDS
# =====================

NEGATIONS = {
    "tidak",
    "tak",
    "gak",
    "ga",
    "gk",
    "nggak",
    "enggak",
    "bukan"
}

# =====================
# SENTIMENT SCORING
# =====================

def calculate_sentiment(text):

    text = str(text).lower()

    score = 0

    # -----------------
    # cek frasa dahulu
    # -----------------

    for phrase, weight in lexicon.items():

        if " " in phrase:

            if phrase in text:

                score += weight

    # -----------------
    # tokenisasi
    # -----------------

    tokens = text.split()

    for i, token in enumerate(tokens):

        if token not in lexicon:
            continue

        weight = lexicon[token]

        # -----------------
        # negasi
        # tidak bagus
        # gak suka
        # -----------------

        if i > 0 and tokens[i - 1] in NEGATIONS:

            weight = -weight

        score += weight

    return score

# =====================
# LABELING
# =====================

def assign_label(score):

    if score > 0:
        return "positive"

    elif score < 0:
        return "negative"

    else:
        return "unknown"

# =====================
# APPLY
# =====================

df["score"] = df["clean_comment"].apply(
    calculate_sentiment
)

df["label"] = df["score"].apply(
    assign_label
)

# =====================
# DISTRIBUSI LABEL
# =====================

print("\nDistribusi Label:")
print(df["label"].value_counts())

# =====================
# HAPUS UNKNOWN
# =====================

df = df[
    df["label"] != "unknown"
]

# =====================
# ENCODE LABEL
# =====================

label_map = {
    "negative": 0,
    "positive": 1
}

df["label_id"] = df["label"].map(
    label_map
)

# =====================
# SAVE
# =====================

output_path = "data/labeled/labeled_comments.csv"

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("\nTotal Data:")
print(len(df))

print("\nDistribusi Final:")
print(df["label"].value_counts())

print("\nSaved:")
print(output_path)