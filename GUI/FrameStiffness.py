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
        relForceRateNoise = eval('self.ui.doubleSpinBox_relForceRateNoise_%s.value()'%tabName)
        max_size_fluctuation = eval('self.ui.spinBox_max_size_fluctuation_%s.value()'%tabName)
        UsingRate2findSurface = eval('self.ui.checkBox_UsingRate2findSurface_%s.isChecked()'%tabName)
        Rate2findSurface = eval('self.ui.doubleSpinBox_Rate2findSurface_%s.value()'%tabName)
        
        Model = {
                    'unloadPMax':unloaPMax,        # upper end of fitting domain of unloading stiffness: Vendor-specific change
                    'unloadPMin':unloaPMin,         # lower end of fitting domain of unloading stiffness: Vendor-specific change
                    'relForceRateNoise':relForceRateNoise, # threshold of dp/dt use to identify start of loading: Vendor-specific change
                    'maxSizeFluctuations': max_size_fluctuation # maximum size of small fluctuations that are removed in identifyLoadHoldUnload
                    }
        
        def guiProgressBar(value, location):
            if location=='load':
                value = value/2
            if location=='calibrateStiffness':
                value = (value/2 + 1/2) *100
            progressBar.setValue(value)

        Output = {
                    'progressBar': guiProgressBar,   # function to use for plotting progress bar
                    }

        Surface = {}
        if UsingRate2findSurface:
            Surface = {
                        "abs(dp/dh)":Rate2findSurface, "median filter":5
                        }
        
        i_FrameStiffness = indentation.Indentation(fileName=fileName, surface=Surface, model=Model, output=Output)

        #plot load-depth of test 1
        ax_load_depth = eval('self.static_ax_load_depth_tab_inclusive_frame_stiffness_%s'%tabName)
        canvas_load_depht = eval('self.static_canvas_load_depth_tab_inclusive_frame_stiffness_%s'%tabName)
        ax_load_depth.cla()
        ax_load_depth.set_title('%s'%i_FrameStiffness.testName)
        i_FrameStiffness.output['ax'] = ax_load_depth
        i_FrameStiffness.stiffnessFromUnloading(i_FrameStiffness.p, i_FrameStiffness.h, plot=True)
        canvas_load_depht.figure.set_tight_layout(True)
        canvas_load_depht.draw()
        i_FrameStiffness.output['ax'] = None

        #calculate FrameStiffness
        ax = eval('self.static_ax_%s'%tabName)
        ax.cla()
        i_FrameStiffness.output['ax'] = ax
        frameCompliance = eval('i_FrameStiffness.calibrateStiffness(critDepth=self.ui.doubleSpinBox_critDepthStiffness_%s.value(), critForce=self.ui.doubleSpinBox_critForceStiffness_%s.value(), plotStiffness=False )'%(tabName,tabName))
        exec('self.static_canvas_%s.draw()'%tabName)
        i_FrameStiffness.output['ax'] = None
        exec('self.ui.lineEdit_FrameCompliance_%s.setText("%.10f")'%(tabName,frameCompliance))
        exec('self.ui.lineEdit_FrameStiffness_%s.setText("%.10f")'%(tabName,1/frameCompliance))
        exec('self.i_%s = i_FrameStiffness'%tabName)  

        #listing Test
        tableWidget=eval('self.ui.tableWidget_%s'%tabName)
        tableWidget.setRowCount(0)
        tableWidget.setRowCount(len(i_FrameStiffness.allTestList))
        for k in range(len(i_FrameStiffness.allTestList)):
            tableWidget.setItem(k,0,QTableWidgetItem("%s"%i_FrameStiffness.allTestList[k]))
            if "%s"%i_FrameStiffness.allTestList[k] in i_FrameStiffness.output['successTest']:
                tableWidget.setItem(k,1,QTableWidgetItem("Yes"))
            else:
                tableWidget.setItem(k,1,QTableWidgetItem("No"))
        Method=i_FrameStiffness.method.value
        exec('self.ui.comboBox_method_%s.setCurrentIndex(Method-1)'%tabName)