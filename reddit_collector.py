"""Read-only Reddit collector for aggregated cryptocurrency research."""
import os
from collections import Counter
import requests

USER_AGENT = "windows:crypto-lab-reddit-research:1.0 (by /u/Mean-Top-7533)"
SUBREDDITS = ["CryptoCurrency", "Bitcoin", "ethereum", "solana"]
ASSETS = {
    "BTC": ["bitcoin", "btc"], "ETH": ["ethereum", "eth"],
    "SOL": ["solana", "sol"], "SUI": ["sui"],
    "HYPE": ["hyperliquid", "hype"],
}

class RedditCollector:
    def __init__(self):
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        if not self.client_id or not self.client_secret:
            raise RuntimeError("Reddit API credentials must be provided through environment variables.")
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.access_token = None

    def authenticate(self):
        response = self.session.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=(self.client_id, self.client_secret),
            data={"grant_type": "client_credentials"}, timeout=15)
        response.raise_for_status()
        self.access_token = response.json()["access_token"]
        self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})

    def fetch_new_posts(self, subreddit, limit=50):
        if not self.access_token:
            self.authenticate()
        response = self.session.get(
            f"https://oauth.reddit.com/r/{subreddit}/new",
            params={"limit": min(limit, 100), "raw_json": 1}, timeout=15)
        response.raise_for_status()
        return [{
            "subreddit": subreddit,
            "title": c["data"].get("title", ""),
            "text": c["data"].get("selftext", ""),
            "created_utc": c["data"].get("created_utc"),
            "score": c["data"].get("score", 0),
            "num_comments": c["data"].get("num_comments", 0),
        } for c in response.json()["data"]["children"]]

    @staticmethod
    def aggregate_mentions(posts):
        mentions = Counter()
        for post in posts:
            text = f"{post['title']} {post['text']}".lower()
            for symbol, keywords in ASSETS.items():
                if any(keyword in text for keyword in keywords):
                    mentions[symbol] += 1
        return dict(mentions)

    def collect(self):
        posts = []
        for subreddit in SUBREDDITS:
            posts.extend(self.fetch_new_posts(subreddit))
        return {"posts_analyzed": len(posts), "asset_mentions": self.aggregate_mentions(posts)}

if __name__ == "__main__":
    print(RedditCollector().collect())
