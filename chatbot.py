import requests

while True:
    user = input("You: ")

    if user.lower() == "exit":
        break

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": user,
            "stream": False
        }
    )

    print("Bot:", response.json()["response"])