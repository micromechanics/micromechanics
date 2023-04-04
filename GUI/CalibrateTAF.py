import sys
import numpy as np
import pathlib
current_path = pathlib.Path().resolve()
sys.path.append('%s\..\micromechanics\\'%current_path)
import indentation as indentation
from PySide6.QtWidgets import *

def click_OK_calibration(self):
        #set Progress Bar
        self.ui.progressBar_calibration.setValue(0)
        #get Inputs
        fileName = f"{self.ui.lineEdit_path_tabCalibration.text()}"
        E_target = self.ui.doubleSpinBox_E_tabCalibration.value()
        Poisson = self.ui.doubleSpinBox_Poisson_tabCalibration.value()
        E_Tip = self.ui.doubleSpinBox_E_Tip_tabTAF.value()
        Poisson_Tip = self.ui.doubleSpinBox_Poisson_Tip_tabTAF.value()
        unloaPMax = self.ui.doubleSpinBox_Start_Pmax_tabCalibration.value()
        unloaPMin = self.ui.doubleSpinBox_End_Pmax_tabCalibration.value()
        zeroGradDelta = self.ui.doubleSpinBox_zeroGradDelta_tabCalibration.value()
        min_size_fluctuation = self.ui.spinBox_min_size_fluctuation_tabCalibration.value()
        number_of_TAFterms = self.ui.spinBox_number_of_TAFterms.value()
        UsingRate2findSurface = self.ui.checkBox_UsingRate2findSurface_tabTAF.isChecked()
        Rate2findSurface = self.ui.doubleSpinBox_Rate2findSurface_tabTAF.value()
        surfaceFind={}
        if UsingRate2findSurface:
            surfaceFind={"abs(dp/dh)":Rate2findSurface,"median filter":5}
        #Reading Inputs 
        self.i_tabTAF = indentation.Indentation(fileName=fileName, nuMat= Poisson, verbose=0, unloadPMax=unloaPMax, unloadPMin=unloaPMin, zeroGradDelta=zeroGradDelta, min_size_fluctuation=min_size_fluctuation,progressBar_calibration=self.ui.progressBar_calibration,UsingRate2findSurface=UsingRate2findSurface,surfaceFind=surfaceFind)
        self.i_tabTAF.nuTip      = Poisson_Tip
        self.i_tabTAF.modulusTip = E_Tip
        Method=self.i_tabTAF.method.value
        
        #show Test method
        self.ui.comboBox_method_tabCalibration.setCurrentIndex(Method-1)

        #plot load-depth of test 1
        self.static_ax_load_depth_tab_inclusive_frame_stiffness_tabTAF.cla()
        self.static_ax_load_depth_tab_inclusive_frame_stiffness_tabTAF.set_title('%s'%self.i_tabTAF.testName)
        print(self.i_tabTAF.h)
        self.i_tabTAF.stiffnessFromUnloading(self.i_tabTAF.p, self.i_tabTAF.h, plot=self.static_ax_load_depth_tab_inclusive_frame_stiffness_tabTAF)
        self.static_canvas_load_depth_tab_inclusive_frame_stiffness_tabTAF.figure.set_tight_layout(True)
        self.static_canvas_load_depth_tab_inclusive_frame_stiffness_tabTAF.draw()

        #calculate frameStiffness and Tip Area Function
        self.static_ax_tabFrameStiffness.cla()
        hc, Ac = self.i_tabTAF.calibration(critDepthStiffness=self.ui.doubleSpinBox_critDepthStiffness_tabCalibration.value(), critForce=self.ui.doubleSpinBox_critForceStiffness_tabCalibration.value(),plotStiffness=self.static_ax_tabFrameStiffness,numPolynomial=number_of_TAFterms,returnArea=True, eTarget=E_target)
        self.static_canvas_tabFrameStiffness.draw()

        #listing Test
        self.ui.tableWidget_tabTAF.setRowCount(0)
        self.ui.tableWidget_tabTAF.setRowCount(len(self.i_tabTAF.allTestList))
        for k in range(len(self.i_tabTAF.allTestList)):
            self.ui.tableWidget_tabTAF.setItem(k,0,QTableWidgetItem("%s"%self.i_tabTAF.allTestList[k]))
            if "%s"%self.i_tabTAF.allTestList[k] in self.i_tabTAF.success_identified_TestList:
                self.ui.tableWidget_tabTAF.setItem(k,1,QTableWidgetItem("Yes"))
            else:
                self.ui.tableWidget_tabTAF.setItem(k,1,QTableWidgetItem("No"))
        self.ui.lineEdit_FrameCompliance_Calibration.setText("%.10f"%self.i_tabTAF.tip.compliance)
        self.ui.lineEdit_FrameStiffness_Calibration.setText("%.10f"%(1/self.i_tabTAF.tip.compliance))
        for j in range(5):
            lineEdit = eval('self.ui.lineEdit_TAF%i_tabTAF'%(j+1))
            lineEdit.setText("0")
        for j in range(number_of_TAFterms):
            lineEdit = eval('self.ui.lineEdit_TAF%i_tabTAF'%(j+1))
            lineEdit.setText("%.10f"%self.i_tabTAF.tip.prefactors[j])
        self.plot_TAF(hc,Ac)

def plot_TAF(self,hc,Ac):
    self.static_ax_tabTipAreaFunction.cla()
    self.static_ax_tabTipAreaFunction.scatter(hc,Ac,color='b',label='data')
    hc_new = np.arange(0,hc.max()*1.05,hc.max()/100)
    Ac_new = self.i_tabTAF.tip.areaFunction(hc_new)
    self.static_ax_tabTipAreaFunction.plot(hc_new,Ac_new,color='r',label='fitted Tip Area Function')
    self.static_ax_tabTipAreaFunction.legend()
    self.static_ax_tabTipAreaFunction.set_xlabel('Contact Depth hc [µm]')
    self.static_ax_tabTipAreaFunction.set_ylabel('Contact Area Ac [µm$^2$]')
    self.static_canvas_tabTipAreaFunction.draw()