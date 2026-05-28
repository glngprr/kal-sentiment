import pandas as pd

df = pd.read_csv("data/clean/clean_comments.csv")

sample_df = df.sample(
    n=2665,
    random_state=42
)

sample_df.to_csv(
    "data/clean/labeling.csv",
    index=False,
    encoding="utf-8-sig"
)

print(sample_df.head())
print("Total sample:", len(sample_df))