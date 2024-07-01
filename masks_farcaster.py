# masks_farcaster.py
import requests
from dappykit import DappyKit

class MasksFrame(DappyKit.Frame):
    def __init__(self):
        super().__init__()
        self.title = "Masks Tips & Data"
        self.description = "Display account balance, recent tips, and ranking from Masks API"
        self.refresh_rate = 60000  # Refresh every 60 seconds
        self.fid = 535389

    def fetch_data(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            self.add_message(f"Failed to retrieve data from {url}.")
            return None

    def render(self):
        # Fetch and display account balance
        balance_url = f"https://app.masks.wtf/api/balance?fid={self.fid}"
        balance_data = self.fetch_data(balance_url)
        if balance_data:
            self.add_text(f"Account Balance: {balance_data.get('balance', 'N/A')} $MASKS")
            self.add_separator()

        # Fetch and display recent tips
        tips_url = f"https://app.masks.wtf/api/tips/recent?fid={self.fid}"
        tips_data = self.fetch_data(tips_url)
        if tips_data:
            self.add_text("Recent Tips Sent:")
            for tip in tips_data.get('sent', []):
                self.add_text(f"Tip: {tip['tip']} to {tip['recipient']}")
            self.add_separator()

            self.add_text("Recent Tips Received:")
            for tip in tips_data.get('received', []):
                self.add_text(f"Tip: {tip['tip']} from {tip['sender']}")
            self.add_separator()

        # Fetch and display ranking
        rank_url = f"https://app.masks.wtf/api/rank?fid={self.fid}"
        rank_data = self.fetch_data(rank_url)
        if rank_data:
            self.add_text(f"User Rank: {rank_data.get('rank', 'N/A')}")
            self.add_separator()

        # Fetch and display leaderboard
        leaderboard_url = "https://app.masks.wtf/api/leaderboard"
        leaderboard_data = self.fetch_data(leaderboard_url)
        if leaderboard_data:
            self.add_text("Top 10 Users:")
            for user in leaderboard_data[:10]:
                self.add_text(f"User {user['fid']} - Balance: {user['balance']} $MASKS")
            self.add_separator()

if __name__ == "__main__":
    frame = MasksFrame()
    frame.run()
