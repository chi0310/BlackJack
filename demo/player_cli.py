import requests
import sseclient
import argparse
import threading
import json


BASE_URL = "http://localhost:8080/api/v1"

def create_game(player_id):
    response = requests.post(f"{BASE_URL}/game/create/by_player/{player_id}")
    if response.status_code == 201:
        game_info = response.json()
        game_id = game_info.get("game_id")
        print(f"Game created successfully. Game ID: {game_id}")
        return game_info
    else:
        print("Failed to create game:", response.json())
        return None

def join_game(game_id, player_id):
    response = requests.post(f"{BASE_URL}/game/{game_id}/join/{player_id}")
    if response.status_code == 204:
        print("Joined game successfully.")
    else:
        print("Failed to join game:", response.json())

def start_game(game_id, player_id):
    response = requests.post(f"{BASE_URL}/game/{game_id}/start/by_player/{player_id}")
    if response.status_code == 204:
        print("Game started successfully.")
    else:
        print("Failed to start game:", response.json())

def play_hit(game_id, player_id):
    response = requests.post(f"{BASE_URL}/game/{game_id}/{player_id}/play/hit")
    if response.status_code == 204:
        print("Played hit successfully.")
    else:
        print("Failed to play hit:", response.json())

def play_stand(game_id, player_id):
    response = requests.post(f"{BASE_URL}/game/{game_id}/{player_id}/play/stand")
    if response.status_code == 204:
        print("Played stand successfully.")
    else:
        print("Failed to play stand:", response.json())

def game_status(game_id, player_id):
    # response = requests.get(
    #     f"{BASE_URL}/game/{game_id}/{player_id}/status",
    #     stream=True,
    #     headers={"Accept": "text/event-stream"}
    # )
    # client = sseclient.SSEClient(f"{BASE_URL}/game/{game_id}/{player_id}/status")
    # client = sseclient.SSEClient(response)
    msgs = sseclient.SSEClient(f"{BASE_URL}/game/{game_id}/{player_id}/status")
    # for event in client.events():
    #     print(event.data)
    print('asdasdzxczxczx')
    print('-' * 20)
    for msg in msgs:
        print('--- sse ---')
        print(msg.data)
        print('-----------')
        if msg.data == '':
            print('sse end')
            break
        outputJS = json.loads(msg.data)
        print(outputJS)
        print('-----------')

def sse_listener(game_id, player_id):
    threading.Thread(
        target=game_status,
        args=(game_id, player_id),
        daemon=True).start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BlackJack CLI Player")
    parser.add_argument("--player_id", help="Player ID")
    parser.add_argument("--game_id", help="Game ID")

    args = parser.parse_args()

    player_id = args.player_id
    game_id = args.game_id

    while True:
        action = input("Enter action (create, join, start, hit, stand, status, quit): ").strip().lower()
        if action == "quit":
            break
        elif action == "create":
            if not player_id:
                player_id = input("Enter player ID: ").strip()
            game_info = create_game(player_id)
            if game_info:
                game_id = game_info.get("game_id")
        elif action == "join":
            if not game_id:
                game_id = input("Enter game ID: ").strip()
            if not player_id:
                player_id = input("Enter player ID: ").strip()
            join_game(game_id, player_id)
        elif action == "start":
            if not game_id:
                game_id = input("Enter game ID: ").strip()
            if not player_id:
                player_id = input("Enter player ID: ").strip()
            start_game(game_id, player_id)
        elif action == "hit":
            if not game_id:
                game_id = input("Enter game ID: ").strip()
            if not player_id:
                player_id = input("Enter player ID: ").strip()
            play_hit(game_id, player_id)
        elif action == "stand":
            if not game_id:
                game_id = input("Enter game ID: ").strip()
            if not player_id:
                player_id = input("Enter player ID: ").strip()
            play_stand(game_id, player_id)
        elif action == "status":
            if not game_id:
                game_id = input("Enter game ID: ").strip()
            if not player_id:
                player_id = input("Enter player ID: ").strip()
            sse_listener(game_id, player_id)
