import bpy

def init_bricks():
    
    # Instead of using a class and store data in it, 
    #   (which was a failed attempt, since random and frequent data losses) 
    #   this function stores data as objects.
    sequence = [1, 2, 0, 3, 0, 2, 0, 3, 0, 2, 1, 2, 0, 1, 2, 0, 0, 3, 0, 4, 0, 3, 4, 3, 2, 1]
    # path_brick = bpy.data.objects.get('path_brick')
    rectangles = []

    # Delete existing bricks first, then make copies
    brick_names = [f"path_brick.{i:03d}" for i in range(1, 30)]
#    brick_names_hit = [name + "_hit" for name in brick_names]
#    all_brick_names = brick_names + brick_names_hit
#    for name in brick_names:
#        if name in bpy.data.objects:
#            bpy.ops.object.select_all(action="DESELECT")
#            bpy.data.objects[name].select_set(True)
#            bpy.ops.object.delete()

    original_brick = bpy.data.objects.get("path_brick")
#    bpy.context.view_layer.objects.active = original_brick # Explicitly set the active object
#    bpy.context.view_layer.update() #Force refrect data changes to view
    for i in range(1, len(sequence)):
#        # then (re)create the brick copy
        brick_name = f"path_brick.{i:03d}"
#        bpy.ops.object.select_all(action="DESELECT")
#        original_brick.select_set(True)
#        bpy.ops.object.duplicate()
#        bpy.ops.object.select_all(action='DESELECT')
        brick = bpy.data.objects.get(brick_name)
#        bpy.context.view_layer.objects.active = brick
#        bpy.context.view_layer.update()
        print(brick_name)
        if brick is not None:
            rectangles.append(brick)
            print("rectangles appended")

    # Position the bricks according to the sequence
#    for i, x in enumerate(sequence):
#        if i < len(rectangles): #runs only up to rectangles length, even when sequence was longer 
#            new_rect = rectangles[i]
            new_rect = brick
            interval = -4.0
            offset = -2.0
            new_rect.location.x = sequence[i]
            new_rect.location.y = offset + i * interval
            new_rect.location.z = 4
            # new_rect.parent = original_brick
            bpy.context.view_layer.objects.active = new_rect
            bpy.context.view_layer.update()
#            bpy.context.collection.objects.link(new_rect) # Link the new rectangle to the current scene
            new_rect.keyframe_insert(data_path="location", frame=i)

init_bricks()