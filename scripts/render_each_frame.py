import bpy

@bpy.app.handlers.persistent
def save_opengl_render(scene):
    print("111")
    # Define the output path
    output_path = f"C:\\tmp\\ucd{scene.frame_current}.png"
    
    # Set the output format to PNG
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    
    # Set the output path
    bpy.context.scene.render.filepath = output_path
    
    # Render the current 3D view
    bpy.ops.render.opengl(write_still=True)
    print("222")

# Add the function to the frame change post handlers
bpy.app.handlers.frame_change_post.append(save_opengl_render)

# Start the animation
bpy.ops.screen.animation_play()
