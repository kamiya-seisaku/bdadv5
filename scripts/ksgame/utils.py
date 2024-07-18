## Utils ##################################################################
import bpy

previous_txt = ""

def showTxt(txt):
    global previous_txt
    if previous_txt == txt:
        return
    previous_txt = txt
    print(str(txt))
    text_obj_key = bpy.data.objects.get('ui.Text.key')
    text_obj_key.data.body = str(txt)    

