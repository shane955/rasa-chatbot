import asyncio
import websockets
import requests
import json

async def handler(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        
        # Parse the incoming message if needed
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format")
            continue  # Skip processing if the message is not valid JSON
        
        # Make a POST request to the Rasa server
        response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"sender": "test_user", "message": message})
        for res in response.json():
            print(res['text'])
        
        
        # Check if the response is successful
        if response.status_code != 200:
            print(f"Error: Failed to get response from Rasa server (Status code: {response.status_code})")
            continue  # Skip processing if the response is not successful
        
        # Get the response from Rasa server
        try:
            responses = response.json()
        except json.JSONDecodeError:
            print("Error: Failed to decode Rasa server response")
            continue  # Skip processing if response is not valid JSON
        
        # Send responses back to the client
        for resp in responses:
            await websocket.send(json.dumps(resp))
            print(f"Sent message: {resp}")

# Start the WebSocket server
start_server = websockets.serve(handler, "localhost", 8000)

# Run the server
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
