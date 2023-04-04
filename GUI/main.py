import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import *
from PySide6.QtCore import (QCoreApplication)

# from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

import numpy as np
from ui_myui import Ui_MainWindow
from ui_DialogExport import Ui_DialogExport

import importlib
import pathlib

current_path = pathlib.Path().resolve()
sys.path.append('%s\..\micromechanics\\'%current_path)
import indentation as indentation         


class DialogExport(QDialog):
    from Export import export
    def __init__(self, parent = None):
        super().__init__()
        self.ui = Ui_DialogExport()
        self.ui.setupUi(self)    
        self.ui.pushButton_selectPath.clicked.connect(self.selectPath)
        self.ui.pushButton_OK.clicked.connect(self.go2export)
    def selectPath(self):       
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.ui.lineEdit_ExportPath.setText(file)
    def go2export(self):
        self.export(win)
    
    

        
class MainWindow(QMainWindow):
    from TipRadius import Calculate_TipRadius
    from CalculateHardnessModulus import Calculate_Hardness_Modulus
    from CalibrateTAF import click_OK_calibration, plot_TAF
    from FrameStiffness import FrameStiffness
    from load_depth import plot_load_depth
    def __init__(self, parent = None) :

        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)        

        #clicked.connect
        self.ui.OK_path_tabCalibration.clicked.connect(self.click_OK_calibration)
        self.ui.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness.clicked.connect(self.click_pushButton_plot_chosen_test_tab_inclusive_frame_stiffness)
        self.ui.pushButton_Calculate_tabTipRadius_FrameStiffness.clicked.connect(self.click_pushButton_Calculate_tabTipRadius_FrameStiffness)
        self.ui.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness.clicked.connect(self.click_pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius)
        self.ui.pushButton_Calculate_tabHE_FrameStiffness.clicked.connect(self.click_pushButton_Calculate_tabHE_FrameStiffness)
        self.ui.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE_FrameStiffness.clicked.connect(self.click_pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE_FrameStiffness)
        self.ui.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE.clicked.connect(self.click_pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE)
        self.ui.Copy_TAF_tabHE.clicked.connect(self.Copy_TAF)
        self.ui.Copy_FrameCompliance_tabHE.clicked.connect(self.Copy_FrameCompliance)
        self.ui.Copy_FrameCompliance_tabTipRadius.clicked.connect(self.Copy_FrameCompliance_tabTipRadius)
        self.ui.Calculate_tabHE.clicked.connect(self.Calculate_Hardness_Modulus)
        self.ui.pushButton_Calculate_tabTipRadius.clicked.connect(self.Calculate_TipRadius)
        self.ui.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius.clicked.connect(self.click_pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius)
        self.ui.actionExport.triggered.connect(self.show_DialogExport)

        self.tabHE_hc_collect=[]
        self.tabHE_Pmax_collect=[]
        self.tabHE_H_collect=[]
        self.tabHE_E_collect=[]
        self.tabHE_testName_collect=[]

        #graphicsView
        graphicsView_list = ['load_depth_tab_inclusive_frame_stiffness_tabTAF',  
                             'tabFrameStiffness',                                #Frame_stiffness_TabTAF
                             'tabTipAreaFunction',
                             'load_depth_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness',
                             'tabTipRadius_FrameStiffness',
                             'tabHE_FrameStiffness',
                             'load_depth_tab_inclusive_frame_stiffness_tabHE_FrameStiffness',
                             'load_depth_tab_inclusive_frame_stiffness_tabHE',
                             'H_hc_tabHE',
                             'H_Index_tabHE',
                             'E_hc_tabHE',
                             'E_Index_tabHE',
                             'load_depth_tab_inclusive_frame_stiffness_tabTipRadius',
                             'HertzianFitting_tabTipRadius',
                             'CalculatedTipRadius_tabTipRadius',
                             ]
        for graphicsView in graphicsView_list:
            self.matplotlib_canve_ax(graphicsView=graphicsView)

    def show_DialogExport(self):
        if not win_DialogExport.isVisible():
            win_DialogExport.show()
    

    def matplotlib_canve_ax(self,graphicsView='load_depth_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness'):
        #graphicsView_load_depth_tab_inclusive_frame_stiffness_TipRadius
        layout = eval('QtWidgets.QVBoxLayout(self.ui.graphicsView_%s)'%graphicsView)
        exec('self.static_canvas_%s = FigureCanvas(Figure(figsize=(5, 3)))'%graphicsView)
        exec('layout.addWidget(NavigationToolbar(self.static_canvas_%s, self))'%graphicsView)
        exec('layout.addWidget(self.static_canvas_%s)'%graphicsView)
        exec('self.static_ax_%s = self.static_canvas_%s.figure.subplots()'%(graphicsView,graphicsView))

    

    def Copy_TAF(self):
        self.ui.lineEdit_TipName_tabHE.setText(self.ui.lineEdit_TipName_tabTAF.text())
        self.ui.doubleSpinBox_E_Tip_tabHE.setValue(self.ui.doubleSpinBox_E_Tip_tabTAF.value())
        self.ui.doubleSpinBox_Poisson_Tip_tabHE.setValue(self.ui.doubleSpinBox_Poisson_Tip_tabTAF.value())
        for j in range(5):
            lineEdit = eval('self.ui.lineEdit_TAF%i_tabHE'%(j+1))
            exec('lineEdit.setText(self.ui.lineEdit_TAF%i_tabTAF.text())'%(j+1))

    def Copy_FrameCompliance(self):
        self.ui.lineEdit_FrameCompliance_tabHE.setText(self.ui.lineEdit_FrameCompliance_tabHE_FrameStiffness.text())

    def Copy_FrameCompliance_tabTipRadius(self):
        self.ui.lineEdit_FrameCompliance_tabTipRadius.setText(self.ui.lineEdit_FrameCompliance_tabTipRadius_FrameStiffness.text())

    def click_pushButton_plot_chosen_test_tab_inclusive_frame_stiffness(self):
        self.plot_load_depth(tabName='tabTAF')
    
    def click_pushButton_Calculate_tabTipRadius_FrameStiffness(self):
        self.FrameStiffness(tabName='tabTipRadius_FrameStiffness')

    def click_pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius(self):
        self.plot_load_depth(tabName='tabTipRadius_FrameStiffness')

    def click_pushButton_Calculate_tabHE_FrameStiffness(self):
        self.FrameStiffness(tabName='tabHE_FrameStiffness')

    def click_pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE_FrameStiffness(self):
        self.plot_load_depth(tabName='tabHE_FrameStiffness')
    
    def click_pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE(self):
        self.plot_load_depth(tabName='tabHE')
    
    def click_pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius(self):
        self.plot_load_depth(tabName='tabTipRadius')
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.setWindowTitle("GUI for steffen's code")
    win.show()
    win.activateWindow()
    win.raise_()
    win_DialogExport = DialogExport()
    # win_DialogExport.setWindowTitle("GUI for steffen's code")
    # win_DialogExport.show()
    # win_DialogExport.activateWindow()
    # win_DialogExport.raise_()
    app.exit(app.exec_())
