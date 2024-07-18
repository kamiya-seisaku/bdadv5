[folder structure]
(root: "c:\codes\bdadv4")
L[.]
L[scripts]
  L[ksgame]

["server.js" codes]
// to run the server: npm run devStart
const express = require('express');
const app = express();
const https = require('http').createServer(app);
const WebSocket = require('ws');
const wss = new WebSocket.Server({ server:https });

// deviated from:
//  https://github.com/websockets/ws/blob/master/examples/express-session-parse/index.js
//  https://github.com/websockets/ws/blob/master/examples/express-session-parse/public/app.js

wss.on('connection', function (ws, request) {
  // const userId = request.session.userId;
  // map.set(userId, ws);

  ws.on('error', console.error);


  ws.on('message', function (message) {
    //
    // Here we can now use session parameters.
    //
    console.log(`Received message ${message}`);
  });

  // ws.on('message', function (message) {
  //   //
  //   // Here we can now use session parameters.
  //   //
  //   console.log(`on-connection: Received message ${message}`);
  //   // ws.send("server.js:send-message:"+message);
  //   ws.emit('server.js:emit-message:', JSON.stringify(message));


  // });

  ws.on('close', function () {
    // map.delete(userId);
  });
});

wss.on('upgrade', function (request, socket, head) {
  console.log(`upgrade received`);

  if (!ws) {
    console.log('No WebSocket connection');
    return;
  };

  ws.send('Hello World!');
  console.log('Sent "Hello World!"');

  wss.removeListener('error', onSocketError);

  wss.handleUpgrade(request, socket, head, function (ws) {
    wss.emit('connection', ws, request);
  });
});

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
    // res.sendFile(__dirname + '/public/main.js');
});

https.listen(3000, () => console.log(`Lisening on port :3000`))


["scripts\CustomNodeGroup.py" codes]


["scripts\ksgame\__main__.py" codes]
# This code is written for a Blender indie game project "Uncirtain Days"
# This code is published with the MIT license, as is, no support obligation.
# Kamiya Seisaku, Kamiya Kei, 2024
import bpy
import os
import glob
#from flask_socketio import SocketIO, emit
#import threading
import os
import sys
import threading
dir = os.path.dirname(bpy.data.filepath)
libdir = os.path.join(dir, "scripts", "ksgame")
sys.path.append(libdir)

from flask_server import flask_server_wrapper
import shared_stuff as sf
from screen_share import ScreenShareCamera

## Utilities ##################################################################
previous_txt = ""
previous_frame = 0

# Receives:
#   input_key: 'A', 'D'
#   
# Returns:
#
#   "repeated_left"
#   "new_left"

def key_sm(): #key handling state machine
    pass

def showTxt(txt):
    global previous_txt
    global previous_frame
    text_obj_system = bpy.data.objects.get('ui.Text.system')
    text_obj_system.data.body = str(txt)    
    
    if bpy.data.scenes[0].frame_current - previous_frame >= 1:
        print(f"showTxt: txt={txt}")
        print(f"showTxt: previous_txt={previous_txt}")
        print(str(txt))
    previous_frame = bpy.data.scenes[0].frame_current

## modaltimer #############################################################
class ModalTimerOperator(bpy.types.Operator):
    bl_idname = "wm.modal_timer_operator"
    bl_label = "ks game"
    global fsw #flask server wrapper class

    def __init__(self):
        pass

    def modal(self, context, event):
        current_frame = bpy.context.scene.frame_current
        if isinstance(event, bpy.types.Event) == False:
            return {'PASS_THROUGH'}

        if event.type == 'ESC':
            self.cancel(context)
            return {'CANCELLED'}

        showTxt(f'1 in ModalTimerOperator/modal/if sf.key_input_g in A, D: sf.key_input_g = {sf.key_input_g}')
        if sf.key_input_g in {'A', 'D'}:
            showTxt(f'2 in ModalTimerOperator/modal/if sf.key_input_g in A, D: sf.key_input_g = {sf.key_input_g}')
            self.key_handling(context, event, sf.key_input_g)
            return {'PASS_THROUGH'}

        if event.type in {'A', 'D'}:
            sf.key_source_g = "blender event"
            sf.key_input_g = event.type
            self.key_handling(context, event, sf.key_input_g)
            return {'PASS_THROUGH'}

        return {'PASS_THROUGH'}

    def key_handling(self, context, event, key_input):
        showTxt(f"in key_handling: key_input(arg of key_handling)= {key_input}")
        bike_mover = bpy.data.objects.get('bike-mover')
        text_obj_toggle = bpy.data.objects.get('ui.Text.toggle')
        text_obj_fn = bpy.data.objects.get('ui.Text.FN')
        if text_obj_toggle.data.body == str(f"bike_mover is moving"):
            # bike_mover["is_moving"] = False
            text_obj_toggle.data.body = str(f"bike_mover is not moving")
        else:
            # bike_mover["is_moving"] = True
            text_obj_toggle.data.body = str(f"bike_mover is moving")
            et = event.type
            frame_number = bpy.context.scene.frame_current
            # to show the score in the 3D view, the body of the ui text object
            # is set according to the same object's custom property "score"
            text_obj_fn.data.body = str(f"FN:{frame_number}")
            # key event handling
            showTxt(key_input)
            if key_input == 'A':
                if bike_mover.location.x < 1:
                    bike_mover.location.x += 0.5
            if key_input == 'D':
                if bike_mover.location.x > -1:
                    bike_mover.location.x -= 0.5
            bpy.context.view_layer.objects.active = bike_mover #Need this to make location changes into blender data
            bpy.context.view_layer.update() #Need this for the change to be visible in 3D View
            
        return

    def execute(self, context):
        global previous_txt
        global previous_frame
        previous_txt = ""
        previous_frame = 0
        bike_mover = bpy.data.objects['bike-mover']
        bike_mover.location = [0, 0, 0]
        bpy.context.view_layer.objects.active = bike_mover #Need this to make location changes into blender data
        bpy.context.view_layer.update() #Need this for the change to be visible in 3D View

        wm = context.window_manager
        bpy.app.handlers.frame_change_post.append(self.modal)
        wm.modal_handler_add(self)

        bpy.context.window.workspace = bpy.data.workspaces['Scripting'] # Switch blender UI to modeling workspace

        # Switch 3D view shading to rendered
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].shading.type = 'RENDERED'

        score_obj = bpy.data.objects.get('ui.Text.score')
        score_obj["score"] = 0 # Reset game score
        # score = score_obj["score"] # Reset game score
        # score = 0
        bpy.ops.screen.animation_play() # Play active scene animation
 
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        bpy.app.handlers.frame_change_post.remove(self.modal)
        unregister()
#        self.fsw.socketio.stop()
        # wm = context.window_manager
        return {'PASS_THROUGH'}

###############################################################################
# BLender menu/operator registration ##########################################
# Register ModalTimerOperator in layout menu ##################################
###############################################################################
# Define the "view" menu in the 3D Viewport
def menu_func(self, context):
    self.layout.operator(ModalTimerOperator.bl_idname, text=ModalTimerOperator.bl_label)

# Register and add to the "view" menu (required to also use F3 search "Modal Timer Operator" for quick access).
def unregister():
    showTxt("unregister")
    global fsw
    fsw.socketio.stop()
    bpy.utils.unregister_class(ModalTimerOperator)
    bpy.types.VIEW3D_MT_view.remove(menu_func)

def register():
    showTxt("register")
    global fsw

    # Reload the screen_share module to ensure changes are reflected
    import screen_share
    import importlib
    importlib.reload(screen_share)
    from screen_share import ScreenShareCamera  # re-import ScreenShareCamera

    fsw = flask_server_wrapper()
    video_camera = ScreenShareCamera(0, 0, 800, 600)  # Adjust dimensions as needed

    # Start the web server in a separate thread
    threading.Thread(
        target=fsw.socketio.run,
        args=(fsw.app, '0.0.0.0', 3000),
        kwargs={'allow_unsafe_werkzeug': True}  # For development purposes
    ).start()

    bpy.utils.register_class(ModalTimerOperator)
    bpy.types.VIEW3D_MT_view.append(menu_func)

# Todo: comment out [debug codes]
#register()
#bpy.ops.wm.modal_timer_operator()
#init_bricks()
#unregister()

if __name__ == "__main__":
    register()
#    bpy.ops.wm.modal_timer_operator()


["scripts\ksgame\flask_server_wrapper.py" codes]
## flask #####################################################################
### global variables
import bpy
import sys
from flask import Flask
from flask_socketio import SocketIO

from os import path as p
sys.path.append(p.join(p.dirname(bpy.data.filepath), "scripts\ksgame"))
import utils

## Utils ##################################################################
import bpy
from screen_share import ScreenShareCamera

previous_txt = ""

def showTxt(txt):
    global previous_txt
    if previous_txt == txt:
        return
    previous_txt = txt
    print(str(txt))
    text_obj_key = bpy.data.objects.get('ui.Text.key')
    text_obj_key.data.body = str(txt)    

class flask_server_wrapper_class:
    key_source = ""
    key_input = ""

    showTxt("flask_server_wrapper")
    
    app = Flask(__name__)
    showTxt(str(app))
    socketio = SocketIO(app)
    testvar = 0
 
    def __init__(self):
        top, left, width, height = (
            self.monitor["top"],
            self.monitor["left"],
            self.monitor["width"],
            self.monitor["height"],
        )

        # Initialize the camera with positional arguments
        self.video_camera = ScreenShareCamera(top, left, width, height)

    @socketio.on('connect')
    def handle_connect():
        showTxt('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        showTxt('Client disconnected')

    @socketio.on('message')
    def handle_message(message):
#        import pdb; pdb.set_trace()
        global key_input, key_source
        key_source = "socketio"
        showTxt(f'in flask_server_wrapper/handle_message, Received message {message}')
        showTxt(f'in flask_server_wrapper/handle_message, initial global key_input: {key_input}')
        key_input = ''  # Reset key input
        if message[0:7]=='keyup':
            key_input = ''
        else:
        # elif message[0:7]=='keydown:':
            socket_key_input = message[8:9]
            if socket_key_input in {'a', 'd'}:
                key_input = socket_key_input.upper()
                showTxt(f'in flask_server_wrapper, global key_input set:{key_input}')
            else:
                showTxt(f'Received non-a/d-message {message}')
                showTxt(f'key_input:{key_input}')
        showTxt(f'in flask_server_wrapper/handle_message, exiting global key_input: {key_input}')

    @app.route('/')
    def index():
        return send_file('..\\public\\index.html')
#        return send_file('../../public/index.html')

# test code
#c = flask_server_wrapper_class()
#print(str(c))