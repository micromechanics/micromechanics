import sys
import pathlib
current_path = pathlib.Path().resolve()
sys.path.append('%s\..\micromechanics\\'%current_path)
import indentation as indentation
import pandas as pd

def export(self, win):
    writer = pd.ExcelWriter("%s"%self.ui.lineEdit_ExportPath.text()) 
    df = pd.DataFrame([ 
                       ['Tested Material'],
                       ['%s'%win.ui.lineEdit_MaterialName_tabHE.text()],
                       ['%s'%win.ui.lineEdit_path_tabHE.text()],
                       ['%f'%win.ui.doubleSpinBox_Poisson_tabHE.value()],
                       ['Tip'],
                       ['%s'%win.ui.lineEdit_TipName_tabHE.text()],
                       ['%f'%win.ui.doubleSpinBox_E_Tip_tabHE.value()],
                       ['%f'%win.ui.doubleSpinBox_Poisson_Tip_tabHE.value()],
                       [' '],
                       ['%s'%win.ui.lineEdit_TAF1_tabHE.text()],
                       ['%s'%win.ui.lineEdit_TAF2_tabHE.text()],
                       ['%s'%win.ui.lineEdit_TAF3_tabHE.text()],
                       ['%s'%win.ui.lineEdit_TAF4_tabHE.text()],
                       ['%s'%win.ui.lineEdit_TAF5_tabHE.text()],
                       [' '],
                       ['%s'%win.ui.lineEdit_FrameCompliance_tabHE.text()],
                       ],
                      index=
                      [' ',
                       'Name of Tested Material',
                       'Path',
                       'Poisson\'s Ratio',
                       ' ',
                       'Tip Name',
                       'Young\'s Modulus of Tip [GPa]',
                       'Poisson\'s Ratio of Tip [GPa]',
                       'Terms of Tip Area Function (TAF)',
                       'C0',
                       'C1',
                       'C2',
                       'C3',
                       'C4',
                       ' ',
                       'Frame Compliance [µm/mN]',
                       ], columns=[' '])
    df.to_excel(writer,sheet_name='Experimental Parameters')
    writer.sheets['Experimental Parameters'].set_column(0, 1, 30) 
    writer.sheets['Experimental Parameters'].set_column(0, 2, 60) 

    for i in range(len(win.tabHE_testName_collect)):
        sheetName = win.tabHE_testName_collect[i]
        df = pd.DataFrame(
                         [win.tabHE_hc_collect[i],
                          win.tabHE_Pmax_collect[i],
                          win.tabHE_H_collect[i],
                          win.tabHE_E_collect[i],
                            ],
                          index =[
                                    'hc[µm]',
                                    'Pmax[mN]',
                                    'H[GPa]',
                                    'E[GPa]',
                                    ],
                        #   index=[x for x in range(1, len(win.tabHE_hc_collect[i])+1)]
                                    )
        df = df.T
        df.to_excel(writer,sheet_name=sheetName, index=False)
        for j in range(4):
            writer.sheets[sheetName].set_column(0, j, 20)
    writer.save()
    return