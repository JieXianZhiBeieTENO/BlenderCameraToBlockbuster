import sys,os,math,glob,json,subprocess
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
    from bpy.types import PropertyGroup, AddonPreferences, Collection, Operator, Panel, Menu
    import pyperclip as pyp

except:
    pass
from .Blender_trans_toMC import Blender_Camera_Output as B
from .MC_trans_AE_changing_toblender import MC_Camera_And_Track_Input as MA
from .MC_trans_chrify_changing_camerajust_toblender import MC_Camera_Only_Input as MCH
from .UI_pref import update_in_pref
from .Outing_error import Rl

class UI_define(PropertyGroup):
    ui1_1="轴附加偏移"
    ui1_2="以MC坐标轴为准的"

    Mu_1: FloatProperty(
        name ='乘积倍数',
        description = '导入时位置所乘的倍数',
        default = 1)

    Mu_2: FloatProperty(
        name ='乘积倍数',
        description = '导出时位置所乘的倍数',
        default = 1)

    B_x: FloatProperty(
        name = 'x'+ui1_1,
        description = ui1_2+'x'+ui1_1,
        default = 0)
    B_y: FloatProperty(
        name = 'y'+ui1_1,
        description = ui1_2+'y'+ui1_1,
        default = 0)
    B_z: FloatProperty(
        name = 'z'+ui1_1,
        description = ui1_2+'z'+ui1_1,
        default = 0)
    
    MA_1: StringProperty(
        name="文件路径(若勾选“批量导入”)",
        subtype='DIR_PATH',
        default="")
    MA_2: BoolProperty(
        name="批量导入",
        description="若选,批量导入文件;若不选,按剪切板导入内容")
    MA_3: BoolProperty(
        name="归于原点",
        description="若选,则相机的第一个坐标固定为0;若不选,按原样导入")

    MCH_1: BoolProperty(
        name="校对分辨率",
        description="若选,则Blender分辨率与所识别的文件匹配",
        default=True)

    Chr_fr_end: BoolProperty(
        name="对齐时间轴结束点",
        description="使时间轴结束点与文本所对应的关键帧个数匹配",
        default=True)

    Is_cle_cach: BoolProperty(
        name="清除缓存表达式",
        description="清除驱动器的缓存表达式(注:这可能使某些插件运行不正常)",
        default=False)

    try:
        import pyperclip as pyp
        import mediapipe as med        
        updateinUI: BoolProperty(default=False)
    except:
        updateinUI: BoolProperty(default=True)
    
    error_thing:StringProperty()
    tiptip:StringProperty()
    
class BTM(Operator):
    bl_idname = 'cam.btm'
    bl_label= 'BL相机转BB'
    bl_description = "复制blender相机数据至剪贴板(只需要在aperture的关键帧面板上粘贴数据就行了)"
    def execute(self, context):
        B.Output()
        return {"FINISHED"}

class MTACT(Operator):
    bl_idname = 'cam.mtact'
    bl_label= 'BB的AE数据转BL'
    bl_description = "将minema导出的AE数据导入到blender(包括相机数据与跟踪数据)"
    def execute(self, context):
        MA.MC_input()
        return {"FINISHED"}

class MTCT(Operator):
    bl_idname = 'cam.mtct'
    bl_label= 'BB的chrify相机转BL'
    bl_description = "将minema导出的chrify数据导入到blender(仅相机)"
    def execute(self, context):
        MCH.exchange()
        return {"FINISHED"}


class uiTools:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BBtools"

class update_error(uiTools,Panel):
    bl_idname = "ui.bbtools0"
    bl_label = "错误"
    def draw(self,context):
        layout=self.layout
        layout.label(text="请在此处或在编辑-偏好设置-插件中找到并下拉本插件菜单,点击“下载必要组件”")
        row = layout.row()
        row.enabled=bpy.context.scene.BBtools.updateinUI
        row.operator(update_in_pref.bl_idname,icon="CONSOLE")    

class UI_PT_camtools1_panel(uiTools,Panel):
    bl_idname = "UI_PT_camtools1_panel"
    bl_label = "Blender相机导出至MC"

    def draw(self, context):
        layout = self.layout
        BBscene = context.scene.BBtools

        '''layout.use_property_split = True
        layout.use_property_decorate = False'''
        split = layout.split()
        col = split.column(align=True)
        col.prop(BBscene, "B_x")
        col.prop(BBscene, "B_y")
        col.prop(BBscene, "B_z")
        row=layout.row()
        row.prop(BBscene,"Mu_2")
        layout.operator(BTM.bl_idname)

"""class Camtools2(uiTools,Panel):   #因太难写被废弃
    bl_idname = "ui.bbtools2"
    bl_label = "导入MC导出的AE相机与跟踪"

    def draw(self, context):
        layout = self.layout
        BBscene = context.scene.BBtools

        '''split = layout.split(factor=0.85)
        box = split.box()'''
        split = layout.split()
        box = split.box()
        bocol = box.column(align=True)
        bocol.prop(BBscene, "MA_2")
        row=bocol.row(align=True)
        row.enabled=bpy.context.scene.BBtools.MA_2
        row.prop(BBscene, "MA_1")
        bocol.prop(BBscene, "MA_3")
        layout.operator(MTACT.bl_idname)"""

class UI_PT_camtools3_panel(uiTools,Panel):
    bl_idname = "UI_PT_camtools3_panel"
    bl_label = "导入MC导出的Chrify相机"

    def draw(self, context):
        layout = self.layout
        BBscene = context.scene.BBtools
        col=layout.row().column()
        col.prop(BBscene,"Chr_fr_end")
        col.prop(BBscene,"MCH_1")
        col.prop(BBscene,"Is_cle_cach")
        col.prop(BBscene,"Mu_1")
        layout.operator(MTCT.bl_idname)






