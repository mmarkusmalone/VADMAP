import requests
import csv
import time

access_token = ""
headers = {
    "Authorization": f"bearer {access_token}",
    "User-Agent": "ChangeMeClient/0.1"
}

url = "https://oauth.reddit.com/r/diaryofaredditor/new"
params = {"limit": 100}
after = None

csv_path = "/Users/mayamarkus-malone/Documents/VADMAP/data/reddit_posts.csv"

# Open CSV in append mode (do not write header)
with open(csv_path, "a", encoding="utf-8", newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    fetched = 0
    for _ in range(10):  # 10 requests × 100 posts = 1000 posts
        if after:
            params["after"] = after
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        posts = data.get("data", {}).get("children", [])
        if not posts:
            print("No more posts found.")
            break
        for post in posts:
            selftext = post["data"].get("selftext", "")
            content = (selftext).strip()
            csv_writer.writerow([content, ""])
            fetched += 1
        after = data.get("data", {}).get("after", None)
        if not after:
            print("Reached end of listing.")
            break
        time.sleep(2)  # Be nice to Reddit's API

print(f"Fetched and appended {fetched} posts.")