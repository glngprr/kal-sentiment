import pandas as pd

df = pd.read_csv("data/clean/sample_labeling.csv")

df.to_excel(
    "data/clean/sample_labeling.xlsx",
    index=False
)

print("Convert selesai")