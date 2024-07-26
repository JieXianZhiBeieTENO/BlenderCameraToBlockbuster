try:
    import bpy
    from bpy.types import  AddonPreferences, Operator
except:
    pass
from .Install import install_pyperclip as I
import webbrowser

class update_in_pref(Operator):
    bl_idname = 'pref.update_in_pref'
    bl_label= '下载必要部件'
    bl_description = "下载插件所需的库"
    def execute(self, context):
        I.install()
        return {"FINISHED"}

class download_in_pref(Operator):
    bl_idname = 'pref.download_in_pref'
    bl_label= '去下载'
    bl_description = "转到github去下载io_import_aperture_tracking"
    def execute(self, context):
        webbrowser.open("https://github.com/Chryfi/io_import_aperture_tracking")
        return {"FINISHED"}

class upd_in_pref(AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        BBscene = context.scene.BBtools

        col=self.layout.column()
        col.enabled=bpy.context.scene.BBtools.updateinUI
        col.operator(update_in_pref.bl_idname, icon="CONSOLE")
        col=self.layout.column(align=True)
        col.label(text="关于BB导BL的操作已移除，若想要此功能，请在这里下载")
        col.label(text="（如果进不去请打开加速器(这里推荐Watt Toolkit)）")
        col=self.layout.column()
        col.operator(download_in_pref.bl_idname, icon="NETWORK_DRIVE")


