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