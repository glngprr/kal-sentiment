from googleapiclient.discovery import build
import pandas as pd

API_KEY = ""

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

# baca excel
df_video = pd.read_excel("data-video-yt.xlsx")

all_comments = []

for url in df_video["url"]:

    # ambil video id
    if "watch?v=" in url:
        video_id = url.split("v=")[1].split("&")[0]

    elif "shorts/" in url:
        video_id = url.split("shorts/")[1].split("?")[0]

    else:
        print("Format URL tidak dikenali:", url)
        continue

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )

    response = request.execute()

    for item in response["items"]:

        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]

        all_comments.append({
            "video_id": video_id,
            "comment": comment
        })

# simpan csv
df = pd.DataFrame(all_comments)

df.to_csv(
    "data/raw/comments.csv",
    index=False
)

print(df.head())
print("Total komentar:", len(df))
