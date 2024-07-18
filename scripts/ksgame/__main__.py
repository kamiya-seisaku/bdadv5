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

# key_sm: key handling state machine
# Receives:
#   input_key: 'A', 'D'
# Returns:
#   input_key, only if it is a non-repeated key input
previous_input_key = ""
def key_sm(input_key): #key handling state machine
    showTxt(f"in key_sm, input_key={input_key}")
    global previous_input_key
    if input_key == "":
        previous_input_key = ""
        showTxt("in key_sm, returning blank (previous was blank)")
        return ""
    else:
        if previous_input_key == input_key:
            previous_input_key = ""
            showTxt("in key_sm, returning blank (repeated key input)")
            return ""
        else:
            previous_input_key = input_key
            showTxt(f"in key_sm, returning {input_key} (new non-blank key input)")
            return input_key

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

#        showTxt(f'1 in ModalTimerOperator/modal/if sf.key_input_g in A, D: sf.key_input_g = {sf.key_input_g}')

        if sf.key_input_g in {'A', 'D'}:
#            showTxt(f'2 in ModalTimerOperator/modal/if sf.key_input_g in A, D: sf.key_input_g = {sf.key_input_g}')
            self.key_handling(context, event, sf.key_input_g)
            return {'PASS_THROUGH'}

        if event.type in {'A', 'D'}:
            sf.key_source_g = "blender event"
            sf.key_input_g = event.type
            self.key_handling(context, event, sf.key_input_g)
            return {'PASS_THROUGH'}

        return {'PASS_THROUGH'}

    def key_handling(self, context, event, key_input):
        processed_key = key_sm(key_input)
        showTxt(f"in key_handling: processed_key={processed_key}")
        if processed_key == "":
            showTxt(f"in key_handling: repeated key")
            return
        # showTxt(f"in key_handling: key_input(arg of key_handling)= {key_input}")
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
        args=(fsw.app, '0.0.0.0', 6999),
        kwargs={
            'allow_unsafe_werkzeug': True,
            'debug': False,
        }  # For development purposes
    ).start()
    # fsw.socketio.run(fsw.app, host='0.0.0.0', port=6999, debug=False)


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
