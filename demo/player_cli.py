import requests
import sseclient
import argparse
import threading
import json

BASE_URL = "http://localhost:8080/api/v1"

class BlackJackCLI:
    def __init__(self, player_id=None, game_id=None):
        self.player_id = player_id
        self.game_id = game_id

    def create_game(self):
        response = requests.post(f"{BASE_URL}/game/create/by_player/{self.player_id}")
        if response.status_code == 201:
            game_info = response.json()
            self.game_id = game_info.get("game_id")
            print(f"Game created successfully. Game ID: {self.game_id}")
            return game_info
        else:
            print("Failed to create game:", response.json())
            return None

    def join_game(self):
        response = requests.post(f"{BASE_URL}/game/{self.game_id}/join/{self.player_id}")
        if response.status_code == 204:
            self._start_sse_listener()
            print("Join game successfully.")
        else:
            print("Failed to join game:", response.json())

    def start_game(self):
        response = requests.post(f"{BASE_URL}/game/{self.game_id}/start/by_player/{self.player_id}")
        if response.status_code == 204:
            self._start_sse_listener()
            print("Game started successfully.")
        else:
            print("Failed to start game:", response.json())

    def play_hit(self):
        response = requests.post(f"{BASE_URL}/game/{self.game_id}/{self.player_id}/play/hit")
        if response.status_code == 204:
            print("Played hit successfully.")
        else:
            print("Failed to play hit:", response.json())

    def play_stand(self):
        response = requests.post(f"{BASE_URL}/game/{self.game_id}/{self.player_id}/play/stand")
        if response.status_code == 204:
            print("Played stand successfully.")
        else:
            print("Failed to play stand:", response.json())

    def game_status(self):
        msgs = sseclient.SSEClient(f"{BASE_URL}/game/{self.game_id}/{self.player_id}/status")
        for msg in msgs:
            if msg.data == '':
                print('sse end')
                break
            output = json.loads(msg.data)
            self.display_game_status(output)

    def display_game_status(self, status):
        print(f"Game Status: {status['status']}")
        print(f"Dealer's Cards: {status['dealer']['cards']}, Final Score: {status['dealer']['final_score']}")
        print("Players:")
        headers = ["Player ID", "Status", "Cards", "Final Score"]
        player_ids = [player['id'] for player in status['players']]
        player_statuses = [player['status'] for player in status['players']]
        player_cards = [' '.join([f"{num}" for suit, num in player['cards']]) for player in status['players']]
        player_scores = [player['final_score'] for player in status['players']]
        
        print(f"{'Player ID':<15} {' '.join([f'{pid:<15}' for pid in player_ids])}")
        print(f"{'Status':<15} {' '.join([f'{status:<15}' for status in player_statuses])}")
        print(f"{'Cards':<15} {' '.join([f'{cards:<15}' for cards in player_cards])}")
        print(f"{'Final Score':<15} {' '.join([f'{score:<15}' for score in player_scores])}")
        
        if status['winners']:
            print(f"Winners: {', '.join(status['winners'])}")
        else:
            print("No winners yet.")
        print('-----------')

    def _start_sse_listener(self):
        threading.Thread(
            target=self.game_status,
            daemon=True).start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BlackJack CLI Player")
    parser.add_argument("--player_id", help="Player ID")
    parser.add_argument("--game_id", help="Game ID")

    args = parser.parse_args()

    cli = BlackJackCLI(player_id=args.player_id, game_id=args.game_id)
    is_head = False
    is_playing = False

    while True:
        if not cli.game_id:
            action = input("Enter action (create, join, quit): ").strip().lower()
            if action == "quit":
                break
            elif action == "create":
                if not cli.player_id:
                    cli.player_id = input("Enter player ID: ").strip()
                cli.create_game()
                is_head = True
            elif action == "join":
                if not cli.game_id:
                    cli.game_id = input("Enter game ID: ").strip()
                if not cli.player_id:
                    cli.player_id = input("Enter player ID: ").strip()
                cli.join_game()
        else:
            if is_head and not is_playing:
                action = input("Enter action (start): ").strip().lower()
                if action == "start":
                    cli.start_game()
                    is_playing = True
            else:
                action = input("Enter action (hit, stand, quit): ").strip().lower()
                if action == "quit":
                    break
                elif action == "hit":
                    cli.play_hit()
                elif action == "stand":
                    cli.play_stand()
