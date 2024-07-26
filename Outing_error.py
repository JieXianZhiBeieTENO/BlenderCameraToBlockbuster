import bpy
class UI_MT_error_menu(bpy.types.Menu):
    bl_label = "错误"
    bl_idname = "UI_MT_error_menu"

    def draw(self, context):
        layout = self.layout
        layout.label(text=bpy.context.scene.BBtools.error_thing,icon="ERROR")

    def draw_item(self, context):
        layout = self.layout
        layout.menu(UI_MT_error_menu.bl_idname)

class UI_MT_tip_menu(bpy.types.Menu):
    bl_label = "提示"
    bl_idname = "UI_MT_tip_menu"

    def draw(self, context):
        layout = self.layout
        layout.label(text=bpy.context.scene.BBtools.tiptip,icon="CONSOLE")

    def draw_item(self, context):
        layout = self.layout
        layout.menu(UI_MT_tip_menu.bl_idname)
class Rl:
    def rl(naming=UI_MT_error_menu):
        bpy.ops.wm.call_menu(name=naming.bl_idname)