import pandas as pd
from sklearn.model_selection import train_test_split

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv(
    "data/labeled/labeled_comments.csv",
    encoding="utf-8",
    quoting=1,
    on_bad_lines="skip"
)

# =====================================
# CEK DATA
# =====================================

df = df.dropna(subset=["label"])

print("Total data:", len(df))
print("\nLabel tersedia:")
print(df["label"].value_counts())

# =====================================
# ENCODE LABEL
# =====================================

label_map = {
    "negative": 0,
    "positive": 1
}

df["label_id"] = df["label"].map(label_map)

# hapus jika ada label aneh
df = df.dropna(subset=["label_id"])

df["label_id"] = df["label_id"].astype(int)

# =====================================
# TRAIN TEST SPLIT
# =====================================

train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["label_id"]
)

# =====================================
# SAVE
# =====================================

train_df.to_csv(
    "data/split-Inset/train.csv",
    index=False,
    encoding="utf-8-sig"
)

test_df.to_csv(
    "data/split-Inset/test.csv",
    index=False,
    encoding="utf-8-sig"
)

# =====================================
# REPORT
# =====================================

print("\n========== HASIL SPLIT ==========")
print("Train size :", len(train_df))
print("Test size  :", len(test_df))

print("\nDistribusi TRAIN:")
print(train_df["label"].value_counts())

print("\nDistribusi TEST:")
print(test_df["label"].value_counts())

print("\nPersentase TRAIN:")
print(
    train_df["label"].value_counts(normalize=True) * 100
)

print("\nPersentase TEST:")
print(
    test_df["label"].value_counts(normalize=True) * 100
)

print(train_df["label"].value_counts())
print(test_df["label"].value_counts())