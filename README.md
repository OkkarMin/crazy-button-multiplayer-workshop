# Crazy Buton workshop for SCSE Freshman 2021

## End product

![GIF of end product]()

We are going to build a platform

- Has a button
- That button moves to a random location when another player press the button on their side
- Keep count of the the players score

## What you will learn

You will understand

- Client - Server architecture
- WebSocket concept
- How to build and manipulate a webpage using HTML + CSS + JavaScript
- How to build Python websocket server

# Client Server Architecture

![Client Server Model image taken from StackOverflow](https://i.stack.imgur.com/qUyFW.png)

1. Client REQUEST from server (Client ➡️ Server)
2. Server RESPONSE to client (Server ➡️ Client)
3. Client make use of data from Server (Text, Image, Video etc...)
4. Repeat 1 through 3

**Server RESPONSE with data when Client REQUEST**

## Daily Example:

You visit YouTube

1. Your laptop (client) request to YouTube (server) asking for data
2. YouTube (server) respond to your laptop with data
3. Your laptop (client) shows you the home page of YouTube
4. You click on a video, repeat 1 through 3

[Image taken from StackOverflow](https://stackoverflow.com/questions/14703627/websockets-protocol-vs-http)

# WebSocket

![WebSocket Model image taken from StackOverflow](https://i.stack.imgur.com/ReJux.png)

1. Client REQUEST for handshake (Client ➡️ Server)
2. Sever RESPONSE with handshake confirmation (Server ➡️ Client)
3. Client - Server socket connection established (Client ↔️ Server)
4. Connect is established till Client or Server close the connection

**Server push data to Client, without Client asking for it**

## Daily Example:

You visit Facebook

1. Your laptop (client) request to Facebook (server) asking for handshake
2. Facebook (server) respond to your laptop with handshake confirmation
3. Your laptop (client) and Facebook (server) WebSocket connection established
4. You get a notification when somebody message you, new post etc...

# Our Crazy Button architecture

![Crazy Button Model image]()

1. Your laptop make request to server for handshake
2. Server respond with handshake confirmation
3. Server push data to your client when:
   - a new player join
   - the button was clicked
   - a player has left
4. Your laptop process on data received from server

# Building button page

- TODO: Write about building button page
