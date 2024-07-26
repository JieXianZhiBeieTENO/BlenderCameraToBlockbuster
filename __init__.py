'''import sys,os,math,glob,json,subprocess
try:
    import bpy
    from bpy.props import (
        BoolProperty,
        IntProperty,
        FloatProperty,
        EnumProperty,
        FloatVectorProperty,
        CollectionProperty,
        PointerProperty,
        StringProperty
    )
    from bpy.types import PropertyGroup, AddonPreferences, Collection, Operator, Panel, Scene

except:
    pass
#sys.path.append("../")
from .Blender_trans_toMC import Blender_Camera_Output as B
from .MC_trans_AE_changing_toblender import MC_Camera_And_Track_Input as MA
from .MC_trans_chrify_changing_camerajust_toblender import MC_Camera_Only_Input as MCH
from .Install import install_pyperclip as I
from .Outing_error import Error,Rl,Tip
from . import UI,UI_pref
from .UI import uiTools'''
try:
    import bpy
    from bpy.props import PointerProperty
    from bpy.types import Scene

except:
    pass
from .Outing_error import UI_MT_error_menu,UI_MT_tip_menu
from . import UI,UI_pref

bl_info = {
    "name": "BBtools",
    "author": "尐贤之辈のTENO",
    "version": (1, 0),
    "blender": (3, 3, 0),
    "location": "View3D > BBtools",
    "description": "在Blender与MC间互相导入导出(Add tools between Blockbuster and Blender)",
    "warning": "因为是第一次制作插件,所以可能有不少Bug,若遇见请私信我。(There are a number of bugs in it probably because it's my first Plug-in. Please tell me if you meet any bugs. )",
    "doc_url": "",
    "tracker_url": "",
    "category": "Link Tools",
}

try:
    import pyperclip as pyp
    impo=(
        UI_pref.update_in_pref,
        UI_pref.download_in_pref,
        UI_pref.upd_in_pref,
        UI.BTM,
        UI.MTACT,
        UI.MTCT,
        UI.UI_PT_camtools1_panel,
        UI.UI_define,
        UI_MT_tip_menu,
        UI_MT_error_menu,
    )
except:
    impo=(
        UI.update_error,
        UI_pref.update_in_pref,
        UI_pref.download_in_pref,
        UI_pref.upd_in_pref,
        UI.UI_define,
        UI_MT_tip_menu,
        UI_MT_error_menu,
    )

def register():
    for impor in impo:
        bpy.utils.register_class(impor)
    Scene.BBtools=PointerProperty(type=UI.UI_define)

def unregister():
    try:
        import pyperclip as pyp
        impo=(
            UI_pref.update_in_pref,
            UI_pref.download_in_pref,
            UI_pref.upd_in_pref,
            UI.BTM,
            UI.MTACT,
            UI.MTCT,
            UI.UI_PT_camtools1_panel,
            UI.UI_define,
            UI_MT_tip_menu,
            UI_MT_error_menu,
        )
    finally:
        for impor in impo:
            bpy.utils.unregister_class(impor)
        del Scene.BBtools
if __name__=="__main__":
    register()