import sys
import numpy as np
import pathlib
current_path = pathlib.Path().resolve()
sys.path.append('%s\..\micromechanics\\'%current_path)
import indentation as indentation
from PySide6.QtWidgets import *
from PySide6.QtGui import *

def Calculate_TipRadius(self):
        fileName = f"{self.ui.lineEdit_path_tabTipRadius.text()}"
        E_Mat = self.ui.doubleSpinBox_E_tabTipRadius.value()
        Poisson = self.ui.doubleSpinBox_Poisson_tabTipRadius.value()
        E_Tip = self.ui.doubleSpinBox_E_Tip_tabTipRadius.value()
        Poisson_Tip = self.ui.doubleSpinBox_Poisson_Tip_tabTipRadius.value()
        unloaPMax = self.ui.doubleSpinBox_Start_Pmax_tabTipRadius.value()
        unloaPMin = self.ui.doubleSpinBox_End_Pmax_tabTipRadius.value()
        zeroGradDelta = self.ui.doubleSpinBox_zeroGradDelta_tabTipRadius.value()
        min_size_fluctuation = self.ui.spinBox_min_size_fluctuation_tabTipRadius.value()
        UsingRate2findSurface = self.ui.checkBox_UsingRate2findSurface_tabTipRadius.isChecked()
        Rate2findSurface = self.ui.doubleSpinBox_Rate2findSurface_tabTipRadius.value()
        FrameCompliance=float(self.ui.lineEdit_FrameCompliance_tabTipRadius.text())
        Tip = indentation.Tip(compliance=FrameCompliance)
        surfaceFind={}
        if UsingRate2findSurface:
            surfaceFind={"abs(dp/dh)":Rate2findSurface,"median filter":5}
        #Reading Inputs 
        self.i_tabTipRadius = indentation.Indentation(fileName=fileName, tip=Tip, nuMat= Poisson, verbose=2, unloadPMax=unloaPMax, unloadPMin=unloaPMin, zeroGradDelta=zeroGradDelta, min_size_fluctuation=min_size_fluctuation,UsingRate2findSurface=UsingRate2findSurface,surfaceFind=surfaceFind)
        self.i_tabTipRadius.nuTip      = Poisson_Tip
        self.i_tabTipRadius.modulusTip = E_Tip
        Method=self.i_tabTipRadius.method.value

        #show Test method
        self.ui.comboBox_method_tabCalibration.setCurrentIndex(Method-1)

        #plot load-depth of test 1
        self.static_ax_load_depth_tab_inclusive_frame_stiffness_tabTipRadius.cla()
        self.static_ax_load_depth_tab_inclusive_frame_stiffness_tabTipRadius.set_title('%s'%self.i_tabTipRadius.testName)
        self.i_tabTipRadius.stiffnessFromUnloading(self.i_tabTipRadius.p, self.i_tabTipRadius.h, plot=self.static_ax_load_depth_tab_inclusive_frame_stiffness_tabTipRadius)
        self.static_canvas_load_depth_tab_inclusive_frame_stiffness_tabTipRadius.figure.set_tight_layout(True)
        self.static_canvas_load_depth_tab_inclusive_frame_stiffness_tabTipRadius.draw()

        def funct(depth, prefactor, h0):
            diff = depth-h0
            if isinstance(diff, np.float64):
                diff = max(diff,0.0)
            else:
                diff[diff<0.0] = 0.0
            return prefactor* (diff)**(3./2.)
        
        fPopIn, certainty = self.i_tabTipRadius.popIn(plot=False, correctH=False)
        iJump = np.where(self.i_tabTipRadius.p>=fPopIn)[0][0]
        iMin  = np.where(self.i_tabTipRadius.h>=0)[0][0]
        ax1 = self.static_ax_HertzianFitting_tabTipRadius
        ax1.cla()
        ax1.plot(self.i_tabTipRadius.h,self.i_tabTipRadius.p,marker='.',alpha=0.8)
        fitElast = [certainty['prefactor'],certainty['h0']]
        ax1.plot(self.i_tabTipRadius.h[iMin:int(1.2*iJump)], funct(self.i_tabTipRadius.h[iMin:int(1.2*iJump)],*fitElast), color='tab:red', label='fitted loading')
        ax1.axvline(self.i_tabTipRadius.h[iJump], color='tab:orange', linestyle='dashed', label='Depth at pop-in')
        ax1.axhline(fPopIn, color='k', linestyle='dashed', label='Force at pop-in')
        ax1.set_xlim(left=-0.0001,right=4*self.i_tabTipRadius.h[iJump])
        ax1.set_ylim(top=1.5*self.i_tabTipRadius.p[iJump], bottom=-0.0001)
        ax1.set_xlabel('Depth [µm]')
        ax1.set_ylabel('Force [mN]')
        ax1.set_title('%s'%self.i_tabTipRadius.testName)
        ax1.legend()
        self.static_canvas_HertzianFitting_tabTipRadius.draw()

        fPopIn, certainty = self.i_tabTipRadius.popIn(plot=False, correctH=False)

        #calculate TipRadius
        fPopIn_collect=[]
        prefactor_collect=[]
        Notlist=[]
        testName_collect=[]
        test_Index_collect=[]
        i = self.i_tabTipRadius
        test_Index=1
        while True:
            i.h -= i.tip.compliance*i.p
            try:
                fPopIn, certainty = i.popIn(plot=False, correctH=False)
            except:
                test_Index+=1
                i.nextTest()
            else:
                # progressBar_Value=int((2*len(self.i_tabHE.allTestList)-len(self.i_tabHE.testList))/(2*len(self.i_tabHE.allTestList))*100)
                # progressBar.setValue(progressBar_Value)
                if i.testName not in Notlist:
                    if i.testName not in self.i_tabTipRadius.success_identified_PopIn:
                        self.i_tabTipRadius.success_identified_PopIn.append(i.testName)
                    fPopIn_collect.append(fPopIn)
                    prefactor_collect.append(certainty["prefactor"])
                    testName_collect.append(i.testName)
                    test_Index_collect.append(test_Index)
                    if not i.testList:
                        break
                test_Index+=1
                i.nextTest()
        
        Er = self.i_tabTipRadius.ReducedModulus(modulus=E_Mat)
        self.ui.lineEdit_reducedModulus_tabTipRadius.setText("%.10f"%Er)
        prefactor_collect = np.asarray(prefactor_collect)
        TipRadius = ( 3*prefactor_collect/(4*Er) )**2

        ax2 = self.static_ax_CalculatedTipRadius_tabTipRadius
        ax2.cla()
        ax2.plot(test_Index_collect,TipRadius,'o')
        ax2.axhline(np.mean(TipRadius), color='k', linestyle='-', label='mean Value')
        ax2.axhline(np.mean(TipRadius)+np.std(TipRadius,ddof=1), color='k', linestyle='dashed', label='standard deviation')
        ax2.axhline(np.mean(TipRadius)-np.std(TipRadius,ddof=1), color='k', linestyle='dashed')
        self.ui.lineEdit_TipRadius_tabTipRadius.setText("%.10f"%np.mean(TipRadius))
        self.ui.lineEdit_TipRadius_errorBar_tabTipRadius.setText("%.10f"%np.std(TipRadius,ddof=1))
        self.static_canvas_CalculatedTipRadius_tabTipRadius.draw()


        #listing Test
        self.ui.tableWidget_tabTipRadius.setRowCount(0)
        self.ui.tableWidget_tabTipRadius.setRowCount(len(self.i_tabTipRadius.allTestList))
        for k in range(len(self.i_tabTipRadius.allTestList)):
            self.ui.tableWidget_tabTipRadius.setItem(k,0,QTableWidgetItem("%s"%self.i_tabTipRadius.allTestList[k]))
            if "%s"%self.i_tabTipRadius.allTestList[k] in self.i_tabTipRadius.success_identified_TestList:
                self.ui.tableWidget_tabTipRadius.setItem(k,1,QTableWidgetItem("Yes"))
            else:
                self.ui.tableWidget_tabTipRadius.setItem(k,1,QTableWidgetItem("No"))
                self.ui.tableWidget_tabTipRadius.item(k,1).setBackground(QColor(125,125,125))
            if "%s"%self.i_tabTipRadius.allTestList[k] in self.i_tabTipRadius.success_identified_PopIn:
                self.ui.tableWidget_tabTipRadius.setItem(k,2,QTableWidgetItem("Yes"))
            else:
                self.ui.tableWidget_tabTipRadius.setItem(k,2,QTableWidgetItem("No"))
                self.ui.tableWidget_tabTipRadius.item(k,2).setBackground(QColor(125,125,125))


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