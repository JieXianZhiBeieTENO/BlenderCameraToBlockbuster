
#鎴I'鎴m 戝闃almos揩t craz鐤y簡！！-

import os,math,glob
try:
    import bpy
    import pyperclip as pyp
except:
    pass
from .Outing_error import Rl

class MC_Camera_And_Track_Input:
    def MC_input():
        toools=bpy.context.scene.BBtools
        for y_n in range(1):
            is_y_n=0
            doc_path=toools.MA_1 #批量导入的路径（若选）
            mode=toools.MA_2 #0为只导入一个相机或跟踪坐标（以剪贴板导入的模式），1为批量导入
            delete=toools.MA_3 #0为不归于原点，1则反之
            count_f=0
            count_f1=0
            cam_fps_m=[]
            tra_fps_m=[]
            camera=[]
            tracker=[]
            cam_name=0
            tra_name=0
            def update(na):
                sel=bpy.context.selected_objects[0]
                bpy.ops.object.duplicate_move_linked()
                sel_link=bpy.context.selected_objects[0]
                sel_link.select_set(False)
                sel.select_set(True)
                bpy.ops.object.delete()
                sel_link.select_set(True)
                sel_link.name=na
                
            if mode==0:
                #导入粘贴板
                p1=pyp.paste()
                p1__1=p1.split("\n")
                print(p1__1)
                try:
                    if p1__1[6]=="Camera Options\tZoom\r":
                        camera.append(p1__1)
                    elif p1__1[6]=="Transform\tOrientation\r":
                        tracker.append(p1__1)
                    else:
                        toools.error_thing="粘贴板内容不符合，请重新复制"
                        print(toools.error_thing) #for me!#blender窗口弹出
                        Rl.rl()
                        break
                except:
                    toools.error_thing="无法分析剪切板内的数据,请重新复制"
                    print(toools.error_thing) #for me!#blender窗口弹出
                    Rl.rl()
                    break
                cam_fps=int(float(p1__1[1][18:]))

                #导入文件夹
            else:
                try:
                    docs=glob.glob(os.path.join(doc_path, "*.txt"))
                except:
                    toools.error_thing="路径输入错误,请重输"
                    Rl.rl()
                    break
                if len(docs)==0:
                    toools.error_thing="文件夹内没有所需文件"
                    Rl.rl()
                    break
                for i in docs:
                    with open(i,"r+",encoding="utf8") as doc:
                        reading=doc.readlines()
                        try:
                            if reading[6]=="Camera Options\tZoom\n":
                                camera.append(reading)
                            elif reading[6]=="Transform\tOrientation\n":
                                tracker.append(reading)
                            else:
                                toools.error_thing="文件夹里有无关txt文件,请将其移至其他地方或删除"
                                print(toools.error_thing) #for me!#blender窗口弹出
                                is_y_n=1
                                camera=[]
                                tracker=[]
                                break
                        except:
                            toools.error_thing="无法分析文件内容,请确认指定文件夹内是否为正确的文件"
                            print(toools.error_thing) #for me!#blender窗口弹出
                            is_y_n=1
                            camera=[]
                            tracker=[]
                            break
                            
                if len(camera)>=1:
                    cam_fps=int(float(camera[0][1][18:]))
                    if len(camera)>>1:
                        for g in range(len(camera)):
                            cam_fps_m.append(int(float(camera[g][1][18:])))
                            if bool(count_f):
                                if cam_fps_m[0]!=cam_fps_m[1]:
                                    toools.error_thing="多个相机的fps不匹配,请参考视频修改"
                                    print(toools.error_thing) #for me!#blender窗口弹出
                                    is_y_n=1
                                    break
                                cam_fps_m.pop(0)
                            if count_f==0:
                                count_f=1
                if len(tracker)>=1:
                    tra_fps=int(float(camera[0][1][18:]))
                    for utt in range(len(tracker)):
                        tra_fps_m.append(int(float(tracker[utt][1][18:])))
                        if bool(count_f1):
                            if tra_fps_m[0]!=cam_fps_m[1]:
                                toools.error_thing="多个跟踪体的fps不匹配,请参考视频修改"
                                print(toools.error_thing) #for me!#blender窗口弹出
                                is_y_n=1
                                break
                            tra_fps_m.pop(0)
                        if count_f1==0:
                            count_f1=1
                try:
                    if tra_fps!=cam_fps and is_y_n!=1:
                        toools.error_thing="相机与跟踪体的fps不匹配,请参考视频修改"
                        print(toools.error_thing) #for me!#blender窗口弹出
                        is_y_n=1
                except:
                    pass
                if is_y_n==1:
                    Rl.rl()
                    break
                if len(camera)==0:
                    try:
                        bpy.context.scene.render.fps=tra_fps
                    except:
                        pass
            #转换相机数据
            for p1_1 in camera:
                cam_name+=1
                shell_zoom=[]
                #景深从缩放转水平
                count=0
                dy=int(p1_1[2][14:])/2
                for i in range(len(p1_1)):
                    length=8+i
                    try:
                        zoom_n=float(p1_1[length][2+len(str(count)):])
                        zoom_f=math.atan2(dy,zoom_n)*2
                        shell_zoom.append(zoom_f)
                    except:
                        break
                    count+=1
                    print(shell_zoom)
                print(length)
                #转换旋转与位置
                for y in range(len(p1_1)):
                    length+=1
                    if p1_1[length]=="Transform\tOrientation\r" or p1_1[length]=="Transform\tOrientation\n":
                        print(p1_1[length])
                        length+=2
                        print(length)
                        break

                c_p={}
                c_r={}

                judge=0
                judge1=0

                group4=[0,0,0]

                for i in range(len(p1_1)):
                    cache=p1_1[length+i].split("\t")
                    if len(cache)==1:
                        break
                    if len(cache)!=5:
                        judge+=1
                        continue
                    else:
                        cache.pop(0)
                    if judge==0:
                        rx=float(cache[1])+90
                        ry=float(cache[3][0:-1])-180
                        rz=-float(cache[2])
                        group1=[rx,ry,rz]
                        group3=[]
                        for ii in range(len(group1)):
                            if abs(group1[ii])!=group1[ii]:
                                group1[ii]+=360
                                if judge1==0:
                                    group3.append(group1[ii])
                            if abs(group2[ii]-group1[ii])>=180 and judge1==1:
                                if group2[ii]<=180:
                                    group4[ii]-=1
                                else:
                                    group4[ii]+=1
                            if judge==1:
                                group3.append(group1[ii]+360*group4[ii])

                        c_r[cache[0]]=[group3[0],group3[1],group3[2]]
                        group2=[rx,ry,rz]
                        judge1=1
                    else:
                        if judge==2:
                            cache1=[float(cache[1]),float(cache[3][0:-1]),float(cache[2])]
                            if delete==1:
                                del_x=cache1["0"][0]
                                del_y=cache1["0"][1]
                                del_z=cache1["0"][2]
                            else:
                                del_x=0
                                del_y=0
                                del_z=0
                            judge=4
                        if judge>>2:
                            c_p[cache[0]]=[-float(cache[1])-del_x,float(cache[3][0:-1])-del_z,float(cache[2])-del_y]
                    print("p=",c_p)
                    print("r=",c_r)
                


                #导入相机数据至Blender
                try:
                    if toools.MA_4==1:
                        vi_x=int(p1_1[2][14:])
                        vi_y=int(p1_1[3][15:])
                        bpy.context.scene.render.resolution_x=vi_x
                        bpy.context.scene.render.resolution_y=vi_y
                    bpy.context.scene.render.fps=cam_fps
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.ops.object.camera_add()
                    name_choose="Aperture_camera "+str(cam_name)
                    bpy.context.selected_objects[0].name=name_choose
                    bpy.context.selected_objects[0].data.name=name_choose
                    scene = bpy.context.scene
                    ks = scene.keying_sets.new(idname="frame_aperture_camera_input", name="frame_aperture_camera_input")
                    ks.bl_description = ''
                    ks.use_insertkey_needed = False
                    ks.use_insertkey_visual = False
                    ks.use_insertkey_xyz_to_rgb = True
                    id_0 = bpy.data.cameras[name_choose]
                    ksp = ks.paths.add(id_0, 'lens', index=-1)
                    for i in range(len(c_p)):
                        p=c_p[str(i)]
                        r=c_r[str(i)]
                        Scene=bpy.context.scene
                        Scene.frame_current=Scene.frame_start+i
                        bds_nc=bpy.data.objects[name_choose]
                        bds_nc.location[0]=p[0]
                        bds_nc.location[1]=p[1]
                        bds_nc.location[2]=p[2]
                        bds_nc.rotation_euler[0]=r[0]/180*math.pi
                        bds_nc.rotation_euler[1]=r[1]/180*math.pi
                        bds_nc.rotation_euler[2]=r[2]/180*math.pi
                        bpy.data.cameras[name_choose].angle=shell_zoom[i]
                        bpy.ops.anim.keyframe_insert_menu(type='__ACTIVE__')
                        bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")
                        update(name_choose)
                    
                    bpy.ops.anim.keying_set_remove()

                except:
                    print("NONE")

            #转换跟踪数据
            for p1_2 in tracker:
                tra_name+=1
                count_t=0
                t_r={}
                t_p={}
                t_s={}
                for i in range(8,len(p1_2)):
                    print("i=",i)
                    cache=p1_2[i].split("\t")
                    cache.pop(0)
                    print(cache)
                    try:
                        print(float(cache[0])) #勿删
                        if count_t==0:
                            t_r[cache[0]]=[float(cache[1]),float(cache[3][0:-1]),float(cache[2])]
                        elif count_t==2:
                            t_p[cache[0]]=[float(cache[1]),float(cache[3][0:-1]),float(cache[2])]
                        elif count_t==4:
                            t_s[cache[0]]=[float(cache[1])/100,float(cache[3][0:-1])/100,float(cache[2])/100]
                    except:
                        count_t+=1
                        print("count_t=",count_t)
                        if count_t==5:
                            break
    
                print(t_r)
                print(t_p)
                print(t_s)
                
                #导入跟踪数据至Blender
                try:
                    bpy.ops.object.empty_add()
                    name_choose1="tracker_"+str(tra_name)
                    for ki in range(len(t_p)):
                        bd=bpy.data
                        bpy.context.scene.frame_current=ki+1
                        bds_nc1=bd.objects[name_choose1]
                        bds_nc1.location[0]=t_p[0]
                        bds_nc1.location[1]=t_p[1]
                        bds_nc1.location[2]=t_p[2]
                        bds_nc1.rotation_euler[0]=t_r[0]/180*math.pi
                        bds_nc1.rotation_euler[1]=t_r[1]/180*math.pi
                        bds_nc1.rotation_euler[2]=t_r[2]/180*math.pi
                        bds_nc1.scale[0]=t_s[0]
                        bds_nc1.scale[1]=t_s[1]
                        bds_nc1.scale[2]=t_s[2]
                        bpy.ops.anim.keyframe_insert_by_name(type="LocRotScale")
                        update(name_choose1)


                except:
                    print("NONE")
            


if __name__=="__main__":
    MC_Camera_And_Track_Input.MC_input()
#print((math.atan2(a,b) / math.pi * 180)*2)

