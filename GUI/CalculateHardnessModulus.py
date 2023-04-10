import sys
import numpy as np
import pathlib
current_path = pathlib.Path().resolve()
sys.path.append('%s\..\micromechanics\\'%current_path)
import indentation as indentation
from PySide6.QtWidgets import *

def Calculate_Hardness_Modulus(self):
        
        #set Progress Bar
        progressBar = self.ui.progressBar_tabHE
        progressBar.setValue(0)

        #Reading Inputs 
        fileName = f"{self.ui.lineEdit_path_tabHE.text()}"
        Poisson = self.ui.doubleSpinBox_Poisson_tabHE.value()
        E_Tip = self.ui.doubleSpinBox_E_Tip_tabHE.value()
        Poisson_Tip = self.ui.doubleSpinBox_Poisson_Tip_tabHE.value()
        unloaPMax = self.ui.doubleSpinBox_Start_Pmax_tabHE.value()
        unloaPMin = self.ui.doubleSpinBox_End_Pmax_tabHE.value()
        relForceRateNoise = self.ui.doubleSpinBox_relForceRateNoise_tabHE.value()
        max_size_fluctuation = self.ui.spinBox_max_size_fluctuation_tabHE.value()
        UsingRate2findSurface = self.ui.checkBox_UsingRate2findSurface_tabHE.isChecked()
        Rate2findSurface = self.ui.doubleSpinBox_Rate2findSurface_tabHE.value()
       
        TAF_terms = []
        for j in range(5):
            lineEdit = eval('self.ui.lineEdit_TAF%i_tabHE'%(j+1))
            TAF_terms.append(float(lineEdit.text()))
        TAF_terms.append('iso')
        FrameCompliance=float(self.ui.lineEdit_FrameCompliance_tabHE.text())
        Tip = indentation.Tip(compliance= FrameCompliance, shape=TAF_terms)

        Model = {
                    'nuTip':      Poisson_Tip,
                    'modulusTip': E_Tip,      # GPa from Oliver,Pharr Method paper
                    'unloadPMax':unloaPMax,        # upper end of fitting domain of unloading stiffness: Vendor-specific change
                    'unloadPMin':unloaPMin,         # lower end of fitting domain of unloading stiffness: Vendor-specific change
                    'relForceRateNoise':relForceRateNoise, # threshold of dp/dt use to identify start of loading: Vendor-specific change
                    'maxSizeFluctuations': max_size_fluctuation # maximum size of small fluctuations that are removed in identifyLoadHoldUnload
                    }
        
        def guiProgressBar(value, location):
            if location=='load':
                value = value/2
            progressBar.setValue(value)

        Output = {
                    'progressBar': guiProgressBar,   # function to use for plotting progress bar
                    }

        Surface = {}
        if UsingRate2findSurface:
            Surface = {
                        "abs(dp/dh)":Rate2findSurface, "median filter":5
                        }
        
        
        self.i_tabHE = indentation.Indentation(fileName=fileName, tip=Tip, nuMat= Poisson, surface=Surface, model=Model, output=Output)

        #show Test method
        Method=self.i_tabHE.method.value
        self.ui.comboBox_method_tabHE.setCurrentIndex(Method-1)

        #plot load-depth of test 1
        self.static_ax_load_depth_tab_inclusive_frame_stiffness_tabHE.cla()
        self.static_ax_load_depth_tab_inclusive_frame_stiffness_tabHE.set_title('%s'%self.i_tabHE.testName)
        self.i_tabHE.output['ax'] = self.static_ax_load_depth_tab_inclusive_frame_stiffness_tabHE
        self.i_tabHE.stiffnessFromUnloading(self.i_tabHE.p, self.i_tabHE.h, plot=True)
        self.static_canvas_load_depth_tab_inclusive_frame_stiffness_tabHE.figure.set_tight_layout(True)
        self.static_canvas_load_depth_tab_inclusive_frame_stiffness_tabHE.draw()
        self.i_tabHE.output['ax'] = None
            
        #calculate Hardnss and Modulus for all Tests
        hc_collect=[]
        Pmax_collect=[]
        H_collect=[]
        E_collect=[]
        Notlist=[]
        testName_collect=[]
        i = self.i_tabHE
        while True:
            i.analyse()
            progressBar_Value=int((2*len(self.i_tabHE.allTestList)-len(self.i_tabHE.testList))/(2*len(self.i_tabHE.allTestList))*100)
            progressBar.setValue(progressBar_Value)
            if i.testName not in Notlist:
                Pmax_collect.append(i.Ac*i.hardness)
                hc_collect.append(i.hc)
                H_collect.append(i.hardness)
                E_collect.append(i.modulus)
                testName_collect.append(i.testName)
                if not i.testList:
                    break
            i.nextTest()
        self.tabHE_hc_collect=hc_collect
        self.tabHE_Pmax_collect=Pmax_collect
        self.tabHE_H_collect=H_collect
        self.tabHE_E_collect=E_collect
        self.tabHE_testName_collect=testName_collect
        #listing Test
        self.ui.tableWidget_tabHE.setRowCount(0)
        self.ui.tableWidget_tabHE.setRowCount(len(self.i_tabHE.allTestList))
        for k in range(len(self.i_tabHE.allTestList)):
            self.ui.tableWidget_tabHE.setItem(k,0,QTableWidgetItem("%s"%self.i_tabHE.allTestList[k]))
            if "%s"%self.i_tabHE.allTestList[k] in self.i_tabHE.output['successTest']:
                self.ui.tableWidget_tabHE.setItem(k,1,QTableWidgetItem("Yes"))
            else:
                self.ui.tableWidget_tabHE.setItem(k,1,QTableWidgetItem("No"))
        self.static_ax_H_hc_tabHE.cla()
        self.static_ax_E_hc_tabHE.cla()
        self.static_ax_H_Index_tabHE.cla()
        self.static_ax_E_Index_tabHE.cla()
        for j in range(len(hc_collect)):
            self.static_ax_H_hc_tabHE.plot(hc_collect[j],H_collect[j],'o-', linewidth=1)
            self.static_ax_E_hc_tabHE.plot(hc_collect[j],E_collect[j],'o-', linewidth=1)

        self.static_ax_H_Index_tabHE.plot(np.arange(1,len(testName_collect)+1,1),H_collect,'o', linewidth=1)
        self.static_ax_H_Index_tabHE.errorbar(np.arange(1,len(testName_collect)+1,1),np.mean(H_collect,axis=1),yerr=np.std(H_collect,axis=1,ddof=1),marker='s', markersize=10, capsize=10, capthick=5,elinewidth=2, color='black',alpha=0.7,linestyle='')
        self.static_ax_E_Index_tabHE.plot(np.arange(1,len(testName_collect)+1,1),E_collect,'o', linewidth=1)
        self.static_ax_E_Index_tabHE.errorbar(np.arange(1,len(testName_collect)+1,1),np.mean(E_collect,axis=1),yerr=np.std(E_collect,axis=1,ddof=1),marker='s', markersize=10, capsize=10, capthick=5,elinewidth=2, color='black',alpha=0.7,linestyle='')
        
        self.static_ax_H_hc_tabHE.set_xlabel('Contact depth [nm]')
        self.static_ax_H_hc_tabHE.set_ylabel('Hardness [GPa]')
        self.static_ax_H_Index_tabHE.set_xlabel('Indents\'s Nummber')
        self.static_ax_H_Index_tabHE.set_ylabel('Hardness [GPa]')
        self.static_ax_E_hc_tabHE.set_xlabel('Contact depth [nm]')
        self.static_ax_E_hc_tabHE.set_ylabel('Young\'s Modulus [GPa]')
        self.static_ax_E_Index_tabHE.set_xlabel('Indents\'s Nummber')
        self.static_ax_E_Index_tabHE.set_ylabel('Young\'s Modulus [GPa]')
        self.static_canvas_H_hc_tabHE.figure.set_tight_layout(True)
        self.static_canvas_E_hc_tabHE.figure.set_tight_layout(True)
        self.static_canvas_H_Index_tabHE.figure.set_tight_layout(True)
        self.static_canvas_E_Index_tabHE.figure.set_tight_layout(True)
        self.static_canvas_H_hc_tabHE.draw()
        self.static_canvas_E_hc_tabHE.draw()
        self.static_canvas_H_Index_tabHE.draw()
        self.static_canvas_E_Index_tabHE.draw()
