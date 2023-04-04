import sys
import pathlib
current_path = pathlib.Path().resolve()
sys.path.append('%s\..\micromechanics\\'%current_path)
import indentation as indentation


def plot_load_depth(self,tabName,If_inclusive_frameStiffness='inclusive'):
    i = eval('self.i_%s'%tabName)
    i.testList = list(i.allTestList)
    ax=eval('self.static_ax_load_depth_tab_%s_frame_stiffness_%s'%(If_inclusive_frameStiffness,tabName))      
    static_canvas=eval('self.static_canvas_load_depth_tab_%s_frame_stiffness_%s'%(If_inclusive_frameStiffness,tabName)) 
    exec('self.static_ax_load_depth_tab_%s_frame_stiffness_%s.cla()'%(If_inclusive_frameStiffness,tabName))
    showFindSurface = eval('self.ui.checkBox_showFindSurface_tab_%s_frame_stiffness_%s.isChecked()'%(If_inclusive_frameStiffness,tabName)) 
    selectedTests=eval('self.ui.tableWidget_%s.selectedItems()'%tabName)
    show_iLHU=eval('self.ui.checkBox_iLHU_%s_frame_stiffness_%s.isChecked()'%(If_inclusive_frameStiffness,tabName))
    for Test in selectedTests:
        row=Test.row()
        column=Test.column()
        if column==0:
            i.testName=Test.text()
            if i.vendor == indentation.definitions.Vendor.Agilent:
                i.nextAgilentTest(newTest=False,plot_identifyLoadHoldUnload=show_iLHU)
                i.nextTest(newTest=False,plotSurface=showFindSurface)
            ax.set_title('%s'%i.testName)
            i.stiffnessFromUnloading(i.p, i.h, plot=ax)
    static_canvas.figure.set_tight_layout(True)
    static_canvas.draw()