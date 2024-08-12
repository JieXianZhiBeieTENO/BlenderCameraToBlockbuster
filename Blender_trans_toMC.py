try:
    import bpy
    import pyperclip as pyp
except:
    pass
import math
from .Outing_error import Rl
#toools=bpy.context.scene.BBtools

class Blender_Camera_Output:
    def Output():
        for y_n in range(1):
            FPS=bpy.context.scene.render.fps
            toools=bpy.context.scene.BBtools
            MC_x=toools.B_x*toools.Mu_2 #以MC为准，输入每个位置关键帧所相加的值：x 
            MC_y=toools.B_y*toools.Mu_2 #以MC为准，输入每个位置关键帧所相加的值：y
            MC_z=toools.B_z*toools.Mu_2 #以MC为准，输入每个位置关键帧所相加的值：z
            if len(bpy.context.selected_objects)>>1:
                toools.error_thing="您选择了多个物体，请选择一个相机(只能选一个!)"
                #print(toools.error_thing) #for me!#blender窗口弹出
                Rl.rl()
                break
            if len(bpy.context.selected_objects)==0:
                toools.error_thing="您没有选择任何东西，请选择一个相机(只能选一个!)"
                #print(toools.error_thing) #for me!#blender窗口弹出
                Rl.rl()
                break
            try:
                if bpy.data.cameras[bpy.context.selected_objects[0].name].angle==0:
                    pass
            except:
                toools.error_thing="您选择了除相机以外的其它物体,请选择相机(只能选一个!)"
                #print(toools.error_thing) #for me!#blender窗口弹出
                Rl.rl()
                break
            sort_0=[]
            sort_1=[]
            sort_2=[]
            sort_3=[]
            sort_4=[]
            sort_5=[]
            sort_6=[]
            thing=bpy.context.selected_objects[0]
            Scene=bpy.context.scene
            i=0
            while True:
                behind=str(i)+"L"
                Scene.frame_current=int(i*(Scene.render.fps/20))+Scene.frame_start
                if Scene.frame_current>Scene.frame_end:
                    break
                bpy.ops.object.duplicate_move_linked()
                thing1=bpy.context.selected_objects[0].name
                thing2=bpy.context.selected_objects[0].data.name
                tt=bpy.data.objects[thing1]
                sort_0.append({"Value":str(-(tt.location[0]+MC_x))+"d","Tick":behind})
                sort_1.append({"Value":str(tt.location[2]+MC_y)+"d","Tick":behind})
                sort_2.append({"Value":str(tt.location[1]+MC_z)+"d","Tick":behind})
                sort_3.append({"Value":str(-(tt.rotation_euler[2]/math.pi*180))+"d","Tick":behind})
                sort_4.append({"Value":str(90-(tt.rotation_euler[0]/math.pi*180))+"d","Tick":behind})
                sort_5.append({"Value":str(tt.rotation_euler[1]/math.pi*180)+"d","Tick":behind})
                y=Scene.render.resolution_y
                x=Scene.render.resolution_x
                vertical=math.atan2(y/2,(x/2)/math.tan((bpy.data.cameras[thing2].angle)/2))/math.pi*180*2/1.1
                sort_6.append({"Value":str(vertical)+"d","Tick":behind})
                bpy.ops.object.delete(use_global=False, confirm=False)
                thing.select_set(True)
                i+=1
            final=str({0:sort_0,1:sort_1,2:sort_2,3:sort_3,4:sort_4,5:sort_5,6:sort_6})
            final=final.replace("\'","")
            pyp.copy(final)
            bpy.context.scene.render.fps=FPS


if __name__=="__main__":
    Blender_Camera_Output.Output()
