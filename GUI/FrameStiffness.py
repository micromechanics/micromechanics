import sys
import numpy as np
import pathlib
current_path = pathlib.Path().resolve()
sys.path.append('%s\..\micromechanics\\'%current_path)
import indentation as indentation
from PySide6.QtWidgets import *

def FrameStiffness(self,tabName):
        #set Progress Bar
        progressBar = eval('self.ui.progressBar_%s'%tabName)
        progressBar.setValue(0)
        # Reading files
        fileName =eval('f"{self.ui.lineEdit_path_%s.text()}"'%tabName)
        unloaPMax = eval('self.ui.doubleSpinBox_Start_Pmax_%s.value()'%tabName)
        unloaPMin = eval('self.ui.doubleSpinBox_End_Pmax_%s.value()'%tabName)
        zeroGradDelta = eval('self.ui.doubleSpinBox_zeroGradDelta_%s.value()'%tabName)
        min_size_fluctuation = eval('self.ui.spinBox_min_size_fluctuation_%s.value()'%tabName)
        UsingRate2findSurface = eval('self.ui.checkBox_UsingRate2findSurface_%s.isChecked()'%tabName)
        Rate2findSurface = eval('self.ui.doubleSpinBox_Rate2findSurface_%s.value()'%tabName)
        surfaceFind={}
        if UsingRate2findSurface:
            surfaceFind={"abs(dp/dh)":Rate2findSurface,"median filter":5}
        i_FrameStiffness = indentation.Indentation(fileName=fileName, verbose=0, unloadPMax=unloaPMax, unloadPMin=unloaPMin, zeroGradDelta=zeroGradDelta, min_size_fluctuation=min_size_fluctuation,surfaceFind=surfaceFind, progressBar_FrameStiffness=progressBar)

        #plot load-depth of test 1
        ax_load_depth = eval('self.static_ax_load_depth_tab_inclusive_frame_stiffness_%s'%tabName)
        canvas_load_depht = eval('self.static_canvas_load_depth_tab_inclusive_frame_stiffness_%s'%tabName)
        ax_load_depth.cla()
        ax_load_depth.set_title('%s'%i_FrameStiffness.testName)
        i_FrameStiffness.stiffnessFromUnloading(i_FrameStiffness.p, i_FrameStiffness.h, plot=ax_load_depth)
        canvas_load_depht.figure.set_tight_layout(True)
        canvas_load_depht.draw()

        #calculate FrameStiffness
        ax = eval('self.static_ax_%s'%tabName)
        ax.cla()
        frameCompliance = eval('i_FrameStiffness.calibrateStiffness(critDepth=self.ui.doubleSpinBox_critDepthStiffness_%s.value(), critForce=self.ui.doubleSpinBox_critForceStiffness_%s.value(), plotStiffness=ax)'%(tabName,tabName))
        exec('self.static_canvas_%s.draw()'%tabName)
        exec('self.ui.lineEdit_FrameCompliance_%s.setText("%.10f")'%(tabName,frameCompliance))
        exec('self.ui.lineEdit_FrameStiffness_%s.setText("%.10f")'%(tabName,1/frameCompliance))
        exec('self.i_%s = i_FrameStiffness'%tabName)  

        #listing Test
        tableWidget=eval('self.ui.tableWidget_%s'%tabName)
        tableWidget.setRowCount(0)
        tableWidget.setRowCount(len(i_FrameStiffness.allTestList))
        for k in range(len(i_FrameStiffness.allTestList)):
            tableWidget.setItem(k,0,QTableWidgetItem("%s"%i_FrameStiffness.allTestList[k]))
            if "%s"%i_FrameStiffness.allTestList[k] in i_FrameStiffness.success_identified_TestList:
                tableWidget.setItem(k,1,QTableWidgetItem("Yes"))
            else:
                tableWidget.setItem(k,1,QTableWidgetItem("No"))
        Method=i_FrameStiffness.method.value
        exec('self.ui.comboBox_method_%s.setCurrentIndex(Method-1)'%tabName)