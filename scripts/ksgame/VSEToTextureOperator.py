import bpy

class VSEToTextureOperator(bpy.types.Operator):
    bl_idname = "render.vse_to_texture"
    bl_label = "Render VSE to Texture"

    def execute(self, context):
        # Render the current frame
        bpy.ops.render.render()

        # Get the rendered image
        rendered_image = bpy.data.images['Viewer Node']

        # Create a new image using the rendered image's pixel data
        new_image = bpy.data.images.new("Rendered Image", width=rendered_image.size[0], height=rendered_image.size[1])
        new_image.pixels = rendered_image.pixels[:]

        # Create a new material and assign the new image as a texture
        material = bpy.data.materials.new("Rendered Material")
        texture = bpy.data.textures.new("Rendered Texture", 'IMAGE')
        texture.image = new_image
        slot = material.texture_slots.add()
        slot.texture = texture

        # Assign the new material to the active object
        bpy.context.active_object.data.materials.append(material)

        return {'FINISHED'}

class VSEToTexturePanel(bpy.types.Panel):
    bl_label = "VSE to Texture"
    bl_idname = "OBJECT_PT_vse_to_texture"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout

        # Add the operator button
        layout.operator("render.vse_to_texture")

def register():
    bpy.utils.register_class(VSEToTextureOperator)
    bpy.utils.register_class(VSEToTexturePanel)

def unregister():
    bpy.utils.unregister_class(VSEToTextureOperator)
    bpy.utils.unregister_class(VSEToTexturePanel)

if __name__ == "__main__":
    register()
