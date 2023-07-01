import asyncio
import websockets
from auth import validate_jwt_token, getIdUser
import json
import requests
from pydantic import BaseModel


class messageOBJ(BaseModel):
    id_user_sender: str
    id_user_recipient: str
    creation_date: str
    content: str
    id_chat: str
    

connections = list()

def removeConnection(websocket):
    for el in connections:
        if el[1] == websocket:
            connections.remove(el)


async def handle_client(websocket):
    token = await websocket.recv()
    print(f"Token ricevuto: {token}")
    
    if validate_jwt_token(token):
        connections.append([getIdUser(token=token), websocket])
        print("Connessione stabilita con il client", websocket.remote_address)
        try:
            # Attiviamo un ciclo infinito per ascoltare i messaggi dal client
            async for message in websocket:
                message_dict = json.loads(message)
                print(message_dict)
                for connection in connections:
                    if message_dict.get('id_user_recipient') == connection[0] or message_dict.get('sender') == connection[0]:
                        print('messaggio inoltrato a ' + str(connection[0])) 
                        await connection[1].send(message)
                        break
                await websocket.send(message)
                {}
                msg = {
                    "id_chat": message_dict.get('id_chat'),
                    "id_user_recipient": message_dict.get('id_user_recipient'),
                    "id_user_sender": message_dict.get('id_user_sender'),
                    "creation_date": message_dict.get('creation_date'),
                    "content": message_dict.get('content')
                }
                x = requests.post("http://localhost:8000/chat/new_message", json = msg)
                print(x)
                
        finally:
        # Rimuoviamo la connessione dalla lista delle connessioni attive
            removeConnection(websocket)
            print("Connessione chiusa con il client", websocket.remote_address)
    else:
        await websocket.send("Token non valido")
        await websocket.close()
        print("Token non valido. Connessione chiusa.")

start_server = websockets.serve(handle_client, "localhost", 8765)

# Avviamo il server
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


