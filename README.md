# Crazy Buton workshop for SCSE Freshman 2021

Curated with ❤️ by [Okkar Min](https://okkarm.in), [Ying Sheng](https://yeowys.com) and [Jiayin](https://github.com/lhinjy)

## End product

![GIF of end product](/static/end_product.gif)

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

# What is Client Server Architecture?

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

# What is WebSocket?

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

[Image taken from StackOverflow](https://stackoverflow.com/questions/14703627/websockets-protocol-vs-http)

# Our Crazy Button architecture

1. Your laptop make request to server for handshake
2. Server respond with handshake confirmation
3. Server push data to your client when:
   - a new player join
   - the button was clicked
   - a player has left
4. Your laptop process on data received from server

## Initial connection

![Initial connection](/static/initial.png)

## A new player connected

![Player connected](/static/player_connected.png)

## The button was pressed

![Button pressed](/static/button_pressed.png)

## A player disconnected

![Player disconnected](/static/player_disconnected.png)

# Building our Crazy Button page

Button page requirements

1. A Button for players to click

   - Button should move randomly on every player screen when one player has clicked

2. Leaderboard that show list of connected players

   - current player should be at the top of the list
   - should show player score

## index.html

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>🤡 Crazy Button Workshop</title>
  </head>

  <!-- loads styling library -->
  <link
    href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css"
    rel="stylesheet"
    type="text/css"
  />

  <!-- loads socket.io javascript library -->
  <script
    src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"
    crossorigin="anonymous"
  ></script>

  <!-- start of helper functions -->
  <script>
    function clearPlayerList() {
      document.getElementById("playerListDisplay").textContent = "";
    }

    function drawPlayerList(playerListData) {
      for (sid in playerListData) {
        // extract playerID and playerScore
        let playerID = sid.slice(0, 4); //sid is too long, we take the first 4 characters
        let playerScore = playerListData[sid];

        // get the place we want to put the textToDislay
        let playerListDisplay = document.getElementById("playerListDisplay");

        // create a list element to insert textToDisplay
        let listElement = document.createElement("li");

        // craft the text to display
        let textToDisplay;

        // it is you!
        if (socket.id == sid) {
          textToDisplay = playerID + " 🤪 " + "[" + playerScore + "]";
          listElement.appendChild(document.createTextNode(textToDisplay)); // insert text to display into list element
          playerListDisplay.prepend(listElement); // insert at top of the list
        } else {
          // it is not you!
          textToDisplay = playerID + "[" + playerScore + "]";
          listElement.appendChild(document.createTextNode(textToDisplay)); // insert text to display into list element
          playerListDisplay.append(listElement); // insert anywhere
        }
      }
    }

    function reDrawPlayerList(playerListData) {
      clearPlayerList();
      drawPlayerList(playerListData);
    }

    // given randomTop and randomLeft values,
    // move button to new location using random values
    function moveButtonToLocation(randomTop, randomLeft) {
      // to adapt button position to screen size;
      let maxHeight = window.innerHeight;
      let maxWidth = window.innerWidth;

      // x and y offset of button relative to the browser
      // screen size
      // randomTop and randomLeft are value between [0, 1] sent from server

      // e.g for laptop with 1200 x 800 resolution and 0.5 for randomTop and randomLeft
      // top_offset = 800 * 0.5 = 400
      // left_offset = 1200 * 0.5 = 600

      // e.g for mobile with 400 x 800 resolution and 0.5 for randomTop and randomLeft
      // top_offset = 400 * 0.5 = 400
      // left_offset = 800 * 0.5 = 600
      let top_offset = maxHeight * randomTop;
      let left_offset = maxWidth * randomLeft;

      // set new button location
      let button = document.getElementById("button");
      button.style.top = top_offset + "px";
      button.style.left = left_offset + "px";
    }
  </script>

  <!-- end of helper functions -->

  <!-- start of socket logic -->
  <script>
    const socket = io.connect("http://localhost:8080");

    // new player connected
    socket.on("player_connected", (data) => {
      reDrawPlayerList(data.playerList);
    });

    // current player disconnected
    socket.on("player_disconnected", (data) => {
      reDrawPlayerList(data.playerList);
    });

    // button was pressed and server emits new_button_location event
    socket.on("new_button_location", (data) => {
      moveButtonToLocation(data.randomTop, data.randomLeft);
      reDrawPlayerList(data.playerList);
    });

    function handleButtonClick() {
      socket.emit("button_pressed");
    }
  </script>
  <!-- end of socket logic -->

  <body>
    <div class="container">
      <button
        id="button"
        class="
          absolute
          flex-auto
          bg-red-500
          hover:bg-red-400
          text-white
          font-bold
          py-2
          px-4
          border-b-4 border-red-700
          hover:border-red-500
          rounded
        "
        onclick="handleButtonClick()"
      >
        Catch Me! 🤡
      </button>

      <p>Connected players 🔗</p>
      <ul id="playerListDisplay"></ul>
    </div>
  </body>
</html>
```

# Building our WebSocket server

WebSocket server requirements

1. Should emit `player_connected` event when a new player connect to the server

   - should sent the following data to client
     - current connected `playerList`

2. Should emit `player_disconnected` event when a player disconnect from the server (player close tab|browser)

   - should sent the following data to client
     - current connected `playerList`

3. Should emit `new_button_locaton` event when a player has clicked the button

   - should keep track of which player clicked the button, so that we can show the score
   - should calculate random values for the button to move
   - should sent the following data to client

     - randomTop, randomLeft a number between 0 to 1 [0, 1]
     - current connected `playerList`

4. Current connected `playerList` should contain
   - playerID and
   - playerScore

## server.py

```python server.py
### server.py ###
# import libraries that will help us with creating the server
import socketio
from aiohttp import web
from random import uniform

# create a Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

# keep track of list of connected players
# {  player1_id: score,
#    player2_id: score,
#    player3_id: score,
#    ...
# }
playerList = {}


# start of event handlers
# a player has joined
@sio.event
async def connect(sid, _):
    # print when new player has connected
    print('new player : ', sid)

    # add player to playerList with initial score of 0
    playerList[sid] = 0

    # announce to everybody connected that a new player has connected
    # with payload of playerList
    await sio.emit('player_connected', {'playerList': playerList})


# a player has left
@sio.event
async def disconnect(sid):
    # remove player from playerList
    playerList.pop(sid)

    # announce to everybody connected that a player has disconnected
    # with payload of playerList
    await sio.emit('player_disconnected', {'playerList': playerList})


# a player has pressed the button
@sio.event
async def button_pressed(sid):
    # randomTop and randonLeft is value between [0, 1]
    randomTop = uniform(0, 1)
    randomLeft = uniform(0, 1)

    # increase player score by 1
    playerList[sid] += 1

    # announce to everybody connected that a player has pressed the button
    # with payload of randomTop, randomLeft to move button on all players screen
    # and playerList to update the score on the player screen
    await sio.emit(
        'new_button_location', {
            'randomTop': randomTop,
            'randomLeft': randomLeft,
            'playerList': playerList,
        })


# end of event handlers

# start server
if __name__ == '__main__':
    web.run_app(app)
```

# Serving index.html and starting WebSocket server

> put `index.html` and `server.py` in same folder

## Library/Dependencies

1. [Python 3.6 and above](https://www.python.org/)

2. [python-socketio](https://python-socketio.readthedocs.io/en/latest/server.html)

```bash
pip install python-socketio #see https://python-socketio.readthedocs.io/en/latest/server.html
```

3. [aiohttp](https://docs.aiohttp.org/en/stable/)

```bash
pip install aiohttp #see https://docs.aiohttp.org/en/stable/
```

## Running server

```bash
cd [to-directory-where-index.html-is-in]
python server.py
# or
python3 server.py
```

## Serving index.html

```bash
cd [to-directory-where-server.py-is-in]
python3 -m http.server 80
```

go to http://localhost:80 to see index.html, our Crazy Button in action

Open two or more browser windows to see the button moving in realtime and scores being updated
