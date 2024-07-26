import math,json
try:
    import bpy
    import pyperclip as pyp
except:
    pass
from .Outing_error import Rl

class MC_Camera_Only_Input:
    def exchange():
        FPS=bpy.context.scene.render.fps
        toools=bpy.context.scene.BBtools
        for y_n in range(1):
            if bpy.context.scene.render.fps!=20:
                toools.error_thing="您的blender的帧率不为20,会在导入时修改且在导入后恢复先前帧率"
                #print(toools.error_thing) #for me!#blender窗口弹出
                Rl.rl()
                bpy.context.scene.render.fps=20
            content=pyp.paste()
            try:
                d=json.loads(content)
            except:
                toools.error_thing="无法分析剪切板内的数据,请重新复制"
                #print(toools.error_thing) #for me!#blender窗口弹出
                Rl.rl()
                break
            cam_trans=d["camera_tracking"]
            cam_info=d["information"]
            cam_res=cam_info["resolution"]

    #转换垂直fov为水平fov
            #print(cam_trans[1])
            for o in range(len(cam_trans)):
                i=cam_trans[o]
                vertical=i["angle"][0]
                level=math.atan2(cam_res[0]/2,(cam_res[1]/2)/math.tan(math.radians(vertical/2)))*2
                #print(level)
                cam_trans[o]["angle"][0]=level
            #print(d)

    #相机数据导入Blender
            if toools.MCH_1==1:
                vi_x=cam_res[0]
                vi_y=cam_res[1]
                bpy.context.scene.render.resolution_x=vi_x
                bpy.context.scene.render.resolution_y=vi_y

            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.camera_add()
            name="Aperture_camera"
            bpy.context.selected_objects[0].name=name
            bpy.context.selected_objects[0].data.name=name
            bpy.context.scene.render.fps=int(cam_info["fps"])

            scene = bpy.context.scene
            ks = scene.keying_sets.new(idname="frame_aperture_camera_input", name="frame_aperture_camera_input")
            ks.bl_description = ''
            ks.use_insertkey_needed = False
            ks.use_insertkey_visual = False
            ks.use_insertkey_xyz_to_rgb = True
            id_0 = bpy.data.cameras[name]
            ksp = ks.paths.add(id_0, 'lens', index=-1)

            dic=[]
            bdo_n=bpy.data.objects[name]
            for i in range(len(cam_trans)):
                p=cam_trans[i]["position"]
                r=cam_trans[i]["angle"]
                bpy.context.scene.frame_current=i+1
                bdo_n.location[0]=-p[0]*toools.Mu_1
                bdo_n.location[1]=p[2]*toools.Mu_1
                bdo_n.location[2]=p[1]*toools.Mu_1
                bdo_n.rotation_euler[0]=(90-r[3])/180*math.pi
                bdo_n.rotation_euler[1]=r[1]/180*math.pi
                bdo_n.rotation_euler[2]=-r[2]/180*math.pi
                bpy.context.scene.frame_current=i+1
                bpy.data.cameras[name].angle=cam_trans[i]["angle"][0]
                dic.append([bdo_n.location[0],bdo_n.location[1],bdo_n.location[2],bdo_n.rotation_euler[0],bdo_n.rotation_euler[1],bdo_n.rotation_euler[2],bpy.data.cameras[name].lens])
            Lo_dr=bdo_n.driver_add('location')
            Ro_dr=bdo_n.driver_add('rotation_euler')
            Le_dr=bpy.data.cameras[name].driver_add('lens')
            bpy.types.Scene.BB_chr_var=dic

            def Location0():
                time=bpy.context.scene.frame_current-bpy.context.scene.frame_start
                return bpy.context.scene.BB_chr_var[time][0]
            def Location1():
                time=bpy.context.scene.frame_current-bpy.context.scene.frame_start
                return bpy.context.scene.BB_chr_var[time][1]
            def Location2():
                time=bpy.context.scene.frame_current-bpy.context.scene.frame_start
                return bpy.context.scene.BB_chr_var[time][2]
            def Rotation0():
                time=bpy.context.scene.frame_current-bpy.context.scene.frame_start
                return bpy.context.scene.BB_chr_var[time][3]
            def Rotation1():
                time=bpy.context.scene.frame_current-bpy.context.scene.frame_start
                return bpy.context.scene.BB_chr_var[time][4]
            def Rotation2():
                time=bpy.context.scene.frame_current-bpy.context.scene.frame_start
                return bpy.context.scene.BB_chr_var[time][5]
            def Lens():
                time=bpy.context.scene.frame_current-bpy.context.scene.frame_start
                return bpy.context.scene.BB_chr_var[time][6]
            
            expr=(Location0,Location1,Location2,Rotation0,Rotation1,Rotation2,Lens)
            expr_str='Location0,Location1,Location2,Rotation0,Rotation1,Rotation2,Lens'.split(',')
            
            for i in range(7):
                bpy.app.driver_namespace[expr_str[i]]=expr[i]

            bpy.context.scene.frame_current=bpy.context.scene.frame_start

            for i in range(3):
                Lo_dr[i].driver.expression=f"Location{i}()"
                Ro_dr[i].driver.expression=f"Rotation{i}()"
            Le_dr.driver.expression="Lens()"

            for i in range(len(dic)):
                bpy.context.scene.frame_current=i+bpy.context.scene.frame_start
                bpy.ops.anim.keyframe_insert_menu(type='__ACTIVE__')
                bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")

            bdo_n.driver_remove('location')
            bdo_n.driver_remove('rotation_euler')
            bpy.data.cameras[name].driver_remove('lens')

            if toools.Chr_fr_end:
                bpy.context.scene.frame_end=len(dic)+bpy.context.scene.frame_start

            if toools.Is_cle_cach:
                bpy.app.driver_namespace.clear()
                
            bpy.ops.anim.keying_set_remove()
            bpy.context.scene.render.fps=FPS






if __name__=="__main__":
    MC_Camera_Only_Input.exchange()


