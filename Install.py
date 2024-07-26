import os,subprocess,sys
try:
    import bpy
    from bpy.types import Scene
    from bpy.props import PointerProperty
except:
    pass
from . import UI
from .Outing_error import Rl,UI_MT_tip_menu
class install_pyperclip:
    def install():
        toools=bpy.context.scene.BBtools
        try:
            import pyperclip as pyp
        except:
            bpy.ops.wm.console_toggle()
            python_exe=os.path.join(sys.prefix,'bin','python.exe')
            subprocess.call([python_exe,'-m','ensurepip'])
            subprocess.call([python_exe,'-m','pip','install','mediapipe','-i','https://pypi.mirrors.ustc.edu.cn/simple/'])
            subprocess.call([python_exe,'-m','pip','install','pyperclip','-i','https://pypi.mirrors.ustc.edu.cn/simple/'])
            bpy.ops.wm.console_toggle()
        try:
            import pyperclip as pyp
            try:
                bpy.utils.unregister_class(UI.update_error)
                impo=(
                UI.BTM,
                UI.MTACT,
                UI.MTCT,
                UI.UI_PT_camtools1_panel,
                )
                for impor in impo:
                    bpy.utils.register_class(impor)
                bpy.context.scene.BBtools.updateinUI=0
            except:
                toools.tiptip="已完成安装(好吧,这个窗口本不该出现的)"
                Rl.rl(UI_MT_tip_menu)
        except:
            try:
                import pyperclip as pyp
            except:
                judge_errorthing1=1
                judge_errorthing2=0
            if judge_errorthing1 and judge_errorthing2:
                toools.error_thing="貌似因为一些原因没有下载成功pyperclip和mediapipe……"
            elif judge_errorthing1==1:
                toools.error_thing="貌似因为一些原因没有下载成功pyperclip……"
            Rl.rl()
            

if __name__=="__main__":
    install_pyperclip.install()