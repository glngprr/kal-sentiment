import pandas as pd
from sklearn.model_selection import train_test_split

# load data
df = pd.read_csv(
    "data/clean/clean_comments.csv",
    encoding="utf-8",
    quoting=1,
    on_bad_lines="skip"
)

# hapus data label kosong
df = df.dropna(subset=["label"])

print(df["label"].unique())
print(df.columns)
print(df.head())
print(len(df))

# encode label
label_map = {
    "negative": 0,
    "neutral": 1,
    "positive": 2
}

df["label_id"] = df["label"].map(label_map)

# split dataset
train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["label_id"]
)

# save
train_df.to_csv(
    "data/train.csv",
    index=False,
    encoding="utf-8-sig"
)

test_df.to_csv(
    "data/test.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Train size:", len(train_df))
print("Test size:", len(test_df))

print("\nDistribusi label:")
print(df["label"].value_counts())