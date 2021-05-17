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
@sio.event
async def connect(sid, _):
    playerList[sid] = 0

    await sio.emit('player_connected', {'playerList': playerList})


@sio.event
async def disconnect(sid):
    # remove player from playerList
    playerList.pop(sid)

    await sio.emit('player_disconnected', {'playerList': playerList})


@sio.event
async def button_pressed(sid):
    # get randomTop, randonLeft a value between [0, 1]
    randomTop = uniform(0, 1)
    randomLeft = uniform(0, 1)

    # increase player score count
    playerList[sid] += 1

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