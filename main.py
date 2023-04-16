from machine import Pin
import network
from boot import do_connect
from microdot_asyncio import Microdot, Response, send_file, asyncio
from microdot_utemplate import render_template

print("starting")

app = Microdot()
Response.default_content_type = 'text/html'

outputs = [14, 26, 25, 13, 12, 27, 33, 32, 23]
inputs  = [16, 17,  4, 19,  5, 18, None, None, None]
labels = ["R3", "R5", "R6", "R1", "R2", "R4", "R7", "R8", "LED"]
functions = ["USB", "Charge", "Light", "Fridge", "Fan", "Fan Top", "none", "RPi", "LED"]

state = {}
for i, o, l, f in zip(inputs, outputs, labels, functions):
    state[l] = {
        "in": i,
        "out": o,
        "pin": Pin(o, Pin.OUT),
        "label": l,
        "func": f,
        "val": 0
    }
    state[l]["pin"].off()
    
def update(so):
    print(so)
    if so["val"]:
        so["pin"].off()
        return 0
    else:
        so["pin"].on()
        return 1

@app.route('/')
async def index(request):
    print(state)
    return render_template('index.html', state=state)

@app.route('/toggle/<relay>')
async def toggle(request, relay):
    s = state[relay]
    print("Receive Toggle Request for Output", s["out"], s["func"])
    s["val"] = update(s)
    return "OK"

@app.route('/state/<relay>')
async def getstate(request, relay):
    s = state[relay]
    print("get state", relay, s["val"])
    return Response(body={"val": s["val"]})

@app.route('/static/<path:path>')
def static(request, path):
    print("static", path)
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)

print("run app")


async def poll_buttons():
    while True:
        for r, s in state.items():
            if s["in"] is None:
                continue
            pi = Pin(s["in"], Pin.IN, Pin.PULL_DOWN)
            
            val = pi.value()
            if val:
                s["val"] = update(s)
                await asyncio.sleep(1)
            
            await asyncio.sleep(0.01)


async def checkConnection():
    await asyncio.sleep(10)
    sta_if = network.WLAN(network.STA_IF)
    while sta_if.isconnected():
        await asyncio.sleep(10)
    else:
        do_connect()


async def main():
    print("Starting Server...")
    asyncio.create_task(app.start_server(port=80))
    print("Start Polling...")
    asyncio.create_task(poll_buttons())
    print("Start Connection Checker...")
    asyncio.create_task(checkConnection())
    print("Running...")
    while True:
        await asyncio.sleep(10)

asyncio.run(main())
