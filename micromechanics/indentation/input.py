"""All instrument specific input functions"""
import io, re, json
from pathlib import Path
from typing import TYPE_CHECKING, Any
from zipfile import ZipFile
import h5py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from .definitions import Method, Vendor, _DefaultSurface

if TYPE_CHECKING:
  from .core import Indentation


class IndentationInputMixin:
  """
  File loading and file iteration methods for :class:`Indentation`.
  """

  def _removeTooCloseInputPoints(self:'Indentation', h:np.ndarray|None=None, p:np.ndarray|None=None, # type: ignore[misc]
                                 t:np.ndarray|None=None, valid:np.ndarray|None=None) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray|None]:
    """
    Remove nearly duplicate time points from package-unit input arrays.
    """
    updateSelf = h is None or p is None or t is None
    if updateSelf:
      h, p, t, valid = self.h, self.p, self.t, self.valid
    assert h is not None and p is not None and t is not None
    if self.method == Method.CSM or len(t)<2:
      return h, p, t, valid
    gradTime = np.diff(t)
    maskTooClose = gradTime < np.percentile(gradTime,80)/1.e3
    t = t[1:][~maskTooClose]
    p = p[1:][~maskTooClose]
    h = h[1:][~maskTooClose]
    valid = None if valid is None else valid[1:][~maskTooClose]
    if updateSelf:
      self.t, self.p, self.h = t, p, h
      if valid is not None:
        self.valid = valid
    return h, p, t, valid


  def _setRawData(self:'Indentation', h:np.ndarray, p:np.ndarray, t:np.ndarray, valid:np.ndarray, # type: ignore[misc]
                  slope:np.ndarray|None=None, phase:np.ndarray|None=None,
                  provenance:dict[str, dict[str, Any]]|None=None, preserveReadResults:bool=False) -> None:
    """
    Store package-unit input arrays as raw data and expose a working copy on self.
    """
    self.raw.h = h.copy()
    self.raw.p = p.copy()
    self.raw.t = t.copy()
    self.raw.valid = valid.copy()
    self.raw.slope = np.array([], dtype=float) if slope is None else slope.copy()
    self.raw.phase = np.array([], dtype=float) if phase is None else phase.copy()
    if provenance is not None:
      self.provenance = provenance
    self.provenance.setdefault('raw', {})['state'] = 'loaded'
    self._restoreRaw()
    self.iLHU:list[list[int]] = []
    self.iDrift = [-1,-1]
    if not preserveReadResults:
      for name in ('k2p', 'hc', 'Ac', 'modulus', 'modulusRed', 'hardness'):
        setattr(self, name, np.array([], dtype=float))
    return

  def loadAgilent(self:'Indentation', fileName:str) -> bool: # type: ignore[misc]
    """
    Initialize G200 excel file for processing

    Args:
        fileName (str): file name

    Returns:
        bool: success
    """
    self.testList = []
    self.fileName = fileName    #one file can have multiple tests
    self.indicies:dict[str, str] = {}
    for sheetName in ['Required Inputs', 'Pre-Test Inputs']:
      try:
        workbook = pd.read_excel(fileName,sheet_name=sheetName)
        self.metaVendor.update( dict(workbook.iloc[-1]) )
        break
      except:
        pass #do nothing;
    if 'Poissons Ratio' in self.metaVendor and self.metaVendor['Poissons Ratio']!=self.nuMat and \
        self.output['verbose']>0:
      print("*WARNING*: Poisson Ratio different than in file.",self.nuMat,self.metaVendor['Poissons Ratio'])
    self.datafile = pd.read_excel(fileName, sheet_name=None)
    tagged:list[str] = []
    code = {"Load On Sample":"p", "Force On Surface":"p", "LOAD":"p", "Load":"p"\
          ,"_Load":"pRaw", "Raw Load":"pRaw","Force":"pRaw"\
          ,"Displacement Into Surface":"h", "DEPTH":"h", "Depth":"h"\
          ,"_Displacement":"hRaw", "Raw Displacement":"hRaw","Displacement":"hRaw"\
          ,"Time On Sample":"t", "Time in Contact":"t", "TIME":"t", "Time":"tTotal"\
          ,"Contact Area":"Ac", "Contact Depth":"hc"\
          ,"Harmonic Displacement":"hHarmonic", "Harmonic Load":"pHarmonic","Phase Angle":"phaseAngle"\
          ,"Load vs Disp Slope":"pVsHSlope","d(Force)/d(Disp)":"pVsHSlope", "_Column": "Column"\
          ,"_Frame": "Frame"\
          ,"Frame Stiffness": "frameStiffness"\
          ,"Harmonic Stiffness":"slopeInvalid"\
          ,"Harmonic Contact Stiffness":"slope", "STIFFNESS":"slope","Stiffness":"slope" \
          ,"Stiffness Squared Over Load":"k2p","Dyn. Stiff.^2/Load":"k2p"\
          ,"Hardness":"hardness", "H_IT Channel":"hardness","HARDNESS":"hardness"\
          ,"Modulus": "modulus", "E_IT Channel": "modulus","MODULUS":"modulus","Reduced Modulus":"modulusRed"\
          ,"Scratch Distance": "s", "XNanoPosition": "x", "YNanoPosition": "y"\
          ,"X Position": "xCoarse", "Y Position": "yCoarse","X Axis Position":"xCoarse"\
          ,"Y Axis Position":"yCoarse"\
          ,"TotalLateralForce": "L", "X Force": "pX", "_XForce": "pX", "Y Force": "pY", "_YForce": "pY"\
          ,"_XDeflection": "Ux", "_YDeflection": "Uy" }
          #"Support Spring Stiffness":"slopeSupport",
    self.fullData = ['h','p','t','pVsHSlope','hRaw','pRaw','tTotal']
    if self.output['verbose']>1:
      print("Open Agilent file: "+fileName)
    for idx, dfName in enumerate(self.datafile.keys()):
      if self.output['progressBar'] is not None:
        self.output['progressBar'](int(idx/len(self.datafile)*100), 'load')
      df    = self.datafile.get(dfName)
      if "Test " in dfName and not "Tagged" in dfName and not "Test Inputs" in dfName:
        self.testList.append(dfName)
        #print "  I should process sheet |",sheet.name,"|"
        if len(self.indicies)==0:               #find index of colums for load, etc
          for cell in df.columns:
            if cell in code:
              self.indicies[code[cell]] = cell
              if self.output['verbose']>2:
                print(f"     {cell:<30} : {code[cell]:<20} ")
            else:
              if self.output['verbose']>2:
                print(f" *** {cell:<30} NOT USED")
            if "Harmonic" in cell or "Dyn. Frequency" in cell:
              self.method = Method.CSM
          #reset to ensure default values are set
          if "p" not in self.indicies: self.indicies['p']=self.indicies['pRaw']
          if "h" not in self.indicies: self.indicies['h']=self.indicies['hRaw']
          if "t" not in self.indicies: self.indicies['t']=self.indicies['tTotal']
          #if self.output['verbose']: print("   Found column names: ",sorted(self.indicies))
      if "Tagged" in dfName: tagged.append(dfName)
    if len(tagged)>0 and self.output['verbose']>1: print("Tagged ",tagged)
    if "t" not in self.indicies or "p" not in self.indicies or \
      "h" not in self.indicies:
      print("*WARNING*: INDENTATION: Some index is missing (t,p,h) should be there")
    self.metaUser['measurementType'] = 'MTS, Agilent Indentation XLS'
    self.allTestList =  list(self.testList)
    return self.nextTest()


  def nextAgilentTest(self:'Indentation', newTest:bool=True) -> bool: # type: ignore[misc]
    """
    Go to next sheet in worksheet and prepare indentation data

    Data:

    - _Raw: without frame stiffness correction,
    - _Frame:  with frame stiffness correction (remove postscript finally)
    - only affects/applies directly depth (h) and stiffness (s)
    - modulus, hardness and k2p always only use the one with frame correction

    Args:
      newTest (bool): take next sheet (default)

    Returns:
      bool: success of going to next sheet
    """
    if self.vendor!=Vendor.Agilent: return False #cannot be used
    if len(self.testList)==0: return False   #no sheet left
    if newTest:
      self.testName = self.testList.pop(0)

    #read data and identify valid data points
    df     = self.datafile.get(self.testName)
    h       = np.array(df[self.indicies['h'    ]][1:-1], dtype=float)
    validFull = np.isfinite(h)
    if 'slope' in self.indicies:
      slope   = np.array(df[self.indicies['slope']][1:-1], dtype=float)
      self.valid =  np.isfinite(slope)
      self.valid[self.valid] = slope[self.valid] > 0.0  #only valid points if stiffness is positiv
    else:
      self.valid = validFull
    for value in self.indicies.values():
      data = np.array(df[value][1:-1], dtype=float)
      mask = np.isfinite(data)
      mask[mask] = data[mask]<1e99
      self.valid = np.logical_and(self.valid, mask)                       #adopt/reduce mask continously

    #Run through all items again and crop to only valid data
    parsed:dict[str, np.ndarray] = {}
    for index, value in self.indicies.items():
      data = np.array(df[value][1:-1], dtype=float)
      if not index in self.fullData:
        data = data[self.valid]
      else:
        data = data[validFull]
      parsed[index] = data
      setattr(self, index, data)
    validInput = self.valid[validFull]
    #  now all fields (incl. p) are full and defined

    #correct data and evaluate missing
    hInput = parsed['h']/1.e3 #from nm in um
    pInput = parsed['p']
    tInput = parsed['t']
    slopeInput = parsed['slope']/1.e3 if 'slope' in parsed else np.array([], dtype=float) #from N/m in mN/um
    phaseInput = parsed['phase']/1.e3 if 'phase' in parsed else np.array([], dtype=float)
    if "Ac" in self.indicies         : self.Ac /= 1.e6  #from nm in um
    if "slope" in self.indicies       : self.slope = slopeInput.copy()
    if 'hc' in self.indicies         : self.hc /= 1.e3  #from nm in um
    if 'hRaw' in self.indicies        : self.hRaw /= 1.e3  #from nm in um
    self.h, self.p, self.t, self.valid = hInput.copy(), pInput.copy(), tInput.copy(), validInput.copy()
    if "k2p" not in self.indicies and 'slope' in self.indicies:
      self.k2p = slopeInput * slopeInput / pInput[validInput]
    self._removeTooCloseInputPoints()
    prov = {'h': {'source': 'Agilent_loaded_depth', 'surface': False, 'drift': False, 'frameCompliance': False},
            'p': {'source': 'Agilent_loaded_load', 'tare': False},
            'slope': {'source': 'Agilent_loaded_stiffness', 'frameCompliance': False}}
    preserveReadResults = any(name in parsed for name in ('k2p', 'hc', 'Ac', 'modulus', 'modulusRed', 'hardness'))
    self._setRawData(self.h, self.p, self.t, self.valid, slopeInput if len(slopeInput)>0 else None,
                     phaseInput if len(phaseInput)>0 else None, prov, preserveReadResults=preserveReadResults)
    return True


  def loadHysitron(self:'Indentation', fileName:str, plotContact:bool=False) -> bool: # type: ignore[misc]
    """
    Load Hysitron hld or txt file for processing, only contains one test

    Args:
      fileName (str): file name
      plotContact (bool): plot intial contact identification (use this method for access)

    Returns:
      bool: success

    """
    from io import StringIO
    self.fileName = fileName
    with open(self.fileName, 'r',encoding='iso-8859-1') as inFile:
      #### HLD FILE ###
      if self.fileName.endswith('.hld'):
        line = inFile.readline()
        if not "File Version: Hysitron" in line:
          #not a Hysitron file
          return False
        if self.output['verbose']>1:
          print("Open Hysitron file: "+self.fileName)

        #read meta-data
        prefact                   = [0.0]*6
        segmentTime:list[float]   = []
        segmentDeltaP:list[float] = []
        segmentPoints:list[int]   = []
        numSegments = 0
        pStart = 0.0
        value = 0.0
        while True:
          line = inFile.readline()
          label = line.split(":")[0]
          try:
            lineParts = line.split(":")[1].split(" ")
            value = float(lineParts[1])
          except:
            if label == "Time Stamp":
              self.timeStamp = ":".join(line.rstrip().split(":")[1:])
            continue
          #pylint: disable=multiple-statements
          if label == "Sample Approach Data Points": break
          if label == "Machine Comp": self.compliance = value #assume nm/uN = um/mN
          if label == "Tip C0":       prefact[0] = value #nm^2/nm^2
          if label == "Tip C1":       prefact[1] = value #nm^2/nm
          if label == "Tip C2":       prefact[2] = value #nm^2/nm^0.5
          if label == "Tip C3":       prefact[3] = value #nm^2/nm^0.25
          if label == "Tip C4":       prefact[4] = value #nm^2/nm^0.125
          if label == "Tip C5":       prefact[5] = value #nm^2/nm^0.0625
          if label == "Contact Threshold":
            print(f'**INFO** The vendor uses contact threshold {value/1.e3} mN.') #uN
          if label == "Drift Rate":   self.metaVendor['drift_rate'] = value/1.e3 #um/s
          if label == "Number of Segments"  : numSegments  = int(value)
          if label == "Segment Begin Time"  : segmentTime.append(value)
          if label == "Segment Begin Demand": pStart     = value
          if label == "Segment End Demand"  : segmentDeltaP.append( (value-pStart)/1.e3 ) #to mN
          if label == "Segment Points"      : segmentPoints.append(int(value))
          #pylint: enable=multiple-statements
        self.tip.prefactors = prefact+['iso']
        if (numSegments!=len(segmentTime)) or (numSegments!=len(segmentDeltaP)):
          print("**ERROR**", numSegments,len(segmentTime),len(segmentDeltaP ) )
        #read approach data
        line = inFile.readline() #Time_s  MotorDisp_mm    Piezo Extension_nm"
        data = ""
        for _ in range(int(value)):
          data +=inFile.readline()

        #read drift data
        numDrift = int(inFile.readline().split(":")[1])
        line = inFile.readline()  #Time_s	Disp_nm",value
        data = ""
        for idx in range(numDrift):
          data +=inFile.readline()
        if len(data)>1:
          self.dataDrift = np.loadtxt( StringIO(str(data))  )
          self.dataDrift[:,1] /= 1.e3  #into um

        #read test data
        #Time_s	Disp_nm	Force_uN	LoadCell_nm	PiezoDisp_nm	Disp_V	Force_V	Piezo_LowV
        numTest = int(inFile.readline().split(":")[1])
        line = inFile.readline()
        data = ""
        for idx in range(numTest):
          data +=inFile.readline()
        dataTest = np.loadtxt( StringIO(str(data))  )
        #store data
        self.t = dataTest[:,0]
        self.h = dataTest[:,1]/1.e3
        self.p = dataTest[:,2]/1.e3
        self.valid=np.ones_like(self.h, dtype=bool)

      #### TXT FILE ###
      if self.fileName.endswith('.txt'):
        line0 = inFile.readline()
        line1 = inFile.readline()
        line2 = inFile.readline()
        line3 = inFile.readline()
        self.metaUser = {'measurementType': 'Hysitron Indentation TXT', 'dateMeasurement':line0.strip()}
        if line1 != "\n" or "Number of Points" not in line2 or not "Depth (nm)" in line3:
          return False #not a Hysitron file
        if self.output['verbose']>1: print("Open Hysitron file: "+self.fileName)
        dataTest = np.loadtxt(inFile)
        #store data
        self.t = dataTest[:,2]
        self.h = dataTest[:,0]/1.e3
        self.p = dataTest[:,1]/1.e3
        #set unknown values
        self.valid = np.ones_like(self.h, dtype=bool)
    self._removeTooCloseInputPoints()
    prov = {'h': {'source': 'Hysitron_loaded_depth', 'surface': False, 'drift': False, 'frameCompliance': False},
            'p': {'source': 'Hysitron_loaded_load', 'tare': False},
            'slope': {'source': 'not_provided', 'frameCompliance': False}}
    self._setRawData(self.h, self.p, self.t, self.valid, None, self.phase if self.phase is not None else None, prov)
    return True



  def loadMicromaterials(self:'Indentation', fileName:str|io.TextIOWrapper) -> bool: # type: ignore[misc]
    """
    Load Micromaterials txt/zip file for processing, contains only one test

    Args:
        fileName (str): file name or file-content

    Returns:
        bool: success
    """
    if isinstance(fileName, io.TextIOWrapper) or fileName.endswith('.txt'):
      #if singe file or file in zip-archive
      try:            #file-content given
        dataTest = np.loadtxt(fileName)  #exception caught
        if not isinstance(fileName, io.TextIOWrapper):
          self.fileName = fileName
          if self.output['verbose']>1: print("Open Micromaterials file: "+self.fileName)
          self.metaUser = {'measurementType': 'Micromaterials Indentation TXT'}
      except:
        if self.output['verbose']>1:
          print("Is not a Micromaterials file")
        return False
      t = dataTest[:,0]
      h = dataTest[:,1]/1.e3
      p = dataTest[:,2]
      h, p, t, _ = self._removeTooCloseInputPoints(h, p, t)
      valid = np.ones_like(t, dtype=bool)
      prov = {'h': {'source': 'Micromaterials_loaded_depth', 'surface': False, 'drift': False, 'frameCompliance': False},
              'p': {'source': 'Micromaterials_loaded_load', 'tare': False},
              'slope': {'source': 'not_provided', 'frameCompliance': False}}
      self._setRawData(h, p, t, valid, provenance=prov)
    elif fileName.endswith('.zip'):
      #if zip-archive of multilpe files: datafile has to remain open
      #    next pylint statement for github actions
      self.datafile = ZipFile(fileName)  # pylint: disable=consider-using-with
      self.testList = self.datafile.namelist()
      if len(np.nonzero([not i.endswith('txt') for i in self.datafile.namelist()])[0])>0:
        print('Not a Micromaterials zip of txt-files')
        return False
      if self.output['verbose']>1:
        print("Open Micromaterials zip of txt-files: "+fileName)
      self.allTestList =  list(self.testList)
      self.fileName = fileName
      self.metaUser = {'measurementType': 'Micromaterials Indentation ZIP'}
      self.nextTest()
    return True


  def nextMicromaterialsTest(self:'Indentation') -> bool: # type: ignore[misc]
    """
    Go to next file in zip or hdf5-file

    Returns:
        bool: success of going to next sheet
    """
    if self.vendor!=Vendor.Micromaterials: #cannot be used
      return False
    if len(self.testList)==0: #no sheet left
      return False
    self.testName = self.testList.pop(0)
    myFile = self.datafile.open(self.testName)
    txt = io.TextIOWrapper(myFile, encoding="utf-8")
    success = self.loadMicromaterials(txt)
    return success


  def loadFischerScope(self:'Indentation', fileName:str) -> bool: # type: ignore[misc]
    """
    Initialize txt-file from Fischer-Scope for processing

    Args:
      fileName (str): file name

    Returns:
      bool: success
    """
    self.metaVendor:dict[str,Any] = {'date':[], 'shape correction':[], 'coordinate x':[], 'coordinate y':[],
            'work elastic':[], 'work nonelastic':[], 'EIT/(1-vs^2) [GPa]':[], 'HIT [N/mm]':[],
            'HUpl [N/mm]': [], 'hr [um]':[], 'hmax [um]':[], 'Compliance [um/N]':[],
            'epsilon':[], 'fit range': []}
    self.workbook = []
    self.testList = []
    self.fileName = fileName
    block = None
    with open(fileName,'r',encoding='iso-8859-1') as fIn:
      # read initial lines and initialialize
      line = fIn.readline()
      if ".hap	Name of the application" not in line:
        print("Not a Fischer Scope")
        return False
      if self.output['verbose']>1:
        print("Open Fischer Scope file: "+fileName)
      identifier = line.split()[0]
      _ = fIn.readline()
      self.metaVendor['Indent_Type'] = fIn.readline().split()[0]
      self.metaVendor['Indent_F'] = ' '.join( fIn.readline().split()[2:] )
      self.metaVendor['Indent_C'] = ' '.join( fIn.readline().split()[2:] )
      self.metaVendor['Indent_R'] = ' '.join( fIn.readline().split()[2:] )
      #read all lines after initial lines
      for line in fIn:
        pattern = identifier+r"   \d\d\.\d\d\.\d\d\d\d  \d\d:\d\d:\d\d"
        dataInLineStr = line.replace(',','.').split()
        dataInLine = [float(item) if self.isfloat(item) else None for item in dataInLineStr]
        if re.match(pattern, line) is not None:
          ## finish old individual measurement
          if block is not None:
            if np.array(block).shape[1]==5:
              df = pd.DataFrame(np.array(block), columns=['F','h','t','HMu','HM'] )
            else:
              df = pd.DataFrame(np.array(block), columns=['F','h','t'] )
            self.workbook.append(df)
          ## start new  individual measurement
          block = []
          self.metaVendor['date'] += [' '.join(line.split()[-2:])]
          self.testList.append('_'.join(line.split()[-2:]))
        elif line.startswith('Indenter shape correction:'):
          self.metaVendor['shape correction'] += [line.split()[-1]]
        elif 'x=  ' in line and 'y=  ' in line:
          self.metaVendor['coordinate x'] += [float(line.split()[1])]
          self.metaVendor['coordinate y'] += [float(line.split()[3])]
        elif line.startswith('We	['):
          self.metaVendor['work elastic'] += [line.split()[-1]]
        elif line.startswith('Wr	['):
          self.metaVendor['work nonelastic'] += [line.split()[-1]]
        elif line.startswith('EIT/(1-vs^2)	[GPa]') and not line.endswith('------\n'):
          self.metaVendor['EIT/(1-vs^2) [GPa]'] += [float(line.split()[-1])]
        elif line.startswith('HIT	[N/mm') and not line.endswith('------\n'):
          self.metaVendor['HIT [N/mm]'] += [float(line.split()[-1])]
        elif line.startswith('HUpl	[N/mm') and not line.endswith('------\n'):
          self.metaVendor['HUpl [N/mm]'] += [float(line.split()[-1])]
        elif line.startswith('hr	[') and not line.endswith('------\n'):
          self.metaVendor['hr [um]'] += [float(line.split()[-1])]
        elif line.startswith('hmax	[') and not line.endswith('------\n'):
          self.metaVendor['hmax [um]'] += [float(line.split()[-1])]
        elif line.startswith('Compliance	[') and not line.endswith('------\n'):
          self.metaVendor['Compliance [um/N]'] += [float(line.split()[-1])]
        elif 'Epsilon =' in line:
          self.metaVendor['epsilon'] += [float(line.split()[-1])]
          self.metaVendor['fit range'] += [' '.join(line.split()[:-3])]
        elif ( len(dataInLine)==3 or len(dataInLine)==5 ) and not None in dataInLine:
          block.append( dataInLine )
      ## add last dataframe
      if np.array(block).shape[1]==5:
        df = pd.DataFrame(np.array(block), columns=['F','h','t','HMu','HM'] )
      else:
        df = pd.DataFrame(np.array(block), columns=['F','h','t'] )
      self.workbook.append(df)
    if self.output['verbose']>2:
      print("Meta information:",self.metaVendor)
      print("Number of measurements read:",len(self.workbook))
    self.metaUser['measurementType'] = 'Fischer-Scope Indentation TXT'
    if self.metaVendor['Indent_F'].startswith('ESP'):
      self.method = Method.MULTI
    else:
      self.method = Method.ISO
    self.nextTest()
    return True


  def nextFischerScopeTest(self:'Indentation') -> bool: # type: ignore[misc]
    """
    Go to next test

    Returns:
        bool: success
    """
    df = self.workbook.pop(0)
    self.testName = self.testList.pop(0)
    t = np.array(df['t'])
    h = np.array(df['h'])
    p = np.array(df['F'])
    h, p, t, _ = self._removeTooCloseInputPoints(h, p, t)
    valid = np.ones_like(t, dtype=bool)
    prov = {'h': {'source': 'FischerScope_loaded_depth', 'surface': False, 'drift': False, 'frameCompliance': False},
            'p': {'source': 'FischerScope_loaded_load', 'tare': False},
            'slope': {'source': 'not_provided', 'frameCompliance': False}}
    self._setRawData(h, p, t, valid, provenance=prov)
    return True


  def loadHDF5(self:'Indentation', fileName:str) -> bool: # type: ignore[misc]
    """
    Initialize hdf5-file that all converters are producing

    Args:
      fileName (str): file name

    Returns:
      bool: success
    """
    self.datafile = h5py.File(fileName, mode='r') #mode='r+', locking=False)
    if self.output['verbose']>1:
      print("Open hdf5-file: "+fileName)
    self.fileName = fileName
    self.metaVendor = {}
    self.testList = []
    if 'version' not in self.datafile.attrs or self.datafile.attrs['version'] not in ['2.0',b'2.0']:
      print("**ERROR** Only hdf5 version 2 supported. ", self.datafile.attrs.get('version') )
      return False
    #read surface and convert to dictionary
    try:
      if self.surface==_DefaultSurface and \
        'post_test_analysis' in self.datafile and \
        'com_github_micromechanics' in self.datafile['post_test_analysis'] and \
        'config' in self.datafile['post_test_analysis']['com_github_micromechanics'].attrs:
        surfaceConfig = self.datafile['post_test_analysis']['com_github_micromechanics'].attrs['config']
        self.surface = json.loads(surfaceConfig)
    except:
      pass
    for key in self.datafile:
      if re.match(r'test_\d+',key):
        self.testList.append(key)
    for key in self.datafile['instrument'].attrs:
      if isinstance(self.datafile['instrument'].attrs[key], dict):
        self.metaVendor = self.datafile['instrument'].attrs[key]
      else:
        self.metaVendor[key] = self.datafile['instrument'].attrs[key]
    if 'uri' not in self.datafile.attrs:
      print("**ERROR** HDF5 file does not contain converter uri metadata")
      return False
    converter = self.datafile.attrs['uri']
    converter = converter.decode('utf-8') if isinstance(converter, bytes) else converter
    converter = converter.split('/')[-1]
    #                 converter:   Vendor, Human readable description
    converterList:dict[str, tuple[Vendor, str]] = {'hap2hdf.py':(Vendor.FischerScopeHDF5, 'Fischer Scope Indentation HDF5'),
                    'Micromaterials2hdf.py': (Vendor.MicromaterialsHDF5, 'Micromaterials Indentation HDF5'),
                    'xls2hdf.py': (Vendor.AgilentHDF5, 'MTS Indentation HDF5'),
                    'nmd2hdf.py': (Vendor.KLAHDF5, 'KLA G200X Indentation HDF5'),
                    'converter_femtotools.py': (Vendor.FemtotoolsHDF5, 'Femtotools Indentation HDF5'),
                    'dat2hdf.py':(Vendor.SurfaceHDF5, 'SURFACE Indentation HDF5'),
                    }
    if converter not in converterList:
      print("**ERROR** Unsupported HDF5 converter:", converter)
      return False
    self.vendor = converterList[converter][0]
    self.metaUser = {'measurementType':converterList[converter][1] }
    if 'json' in self.metaVendor:
      metaVendor = json.loads(self.metaVendor['json'])
      if 'SAMPLE' in metaVendor:  #G200X data
        templateName = metaVendor['SAMPLE']['@TEMPLATENAME']
        if 'Dynamic' in templateName or 'Essential' in templateName or 'Displacement' in templateName:
          self.method = Method.CSM
    self.fillVendorDefaults()
    self.allTestList = list(self.testList)
    self.nextTest()
    return True


  def nextHDF5Test(self:'Indentation') -> bool: # type: ignore[misc]
    """
    Go to next branch in HDF5 file

    Returns:
        bool: success
    """
    #organize general data
    if len(self.testList)==0: #no sheet left
      return False
    while len(self.testList)>0:
      self.testName = self.testList.pop(0)
      if self.testName not in self.surface or 'surfaceIdx' in self.surface[self.testName]:
        break
    if self.testName in self.surface and 'surfaceIdx' not in self.surface[self.testName]:  #handle last test
      return False
    branch = self.datafile[self.testName]['data']
    inFile = list(branch.keys())
    for attrib in ['slope', 'k2p', 'hc', 'Ac', 'modulus', 'modulusRed', 'hardness', 'phase']:
      setattr(self, attrib, [])
    with open(Path(__file__).parent/'terms.json', encoding='utf-8') as fIn:
      nameDict   = json.load(fIn)
    measurementType = self.metaUser['measurementType'] if isinstance(self.metaUser['measurementType'], str) else '__ERRORR__'
    if measurementType.split()[0] in nameDict:
      nameDict = nameDict[measurementType.split()[0]]
    else:
      print("**ERROR** instrument not in terms.json:", measurementType.split()[0])
      return False


    #determine valid masks: loop through all entries and ensure that they all make sense
    valid = None
    validFull = None
    for key in nameDict:
      if key in ['__ignore__','__note__']:
        continue
      for name, _ in nameDict[key]:
        if name in branch:
          data = np.array(branch[name], dtype=float)
          mask = np.logical_and(np.isfinite(data), data<1e99)
          if valid is None:
            valid = mask
          else:
            valid = np.logical_and(valid, mask) #adopt/reduce mask continuously
          if key=='slope':
            valid = np.logical_and(valid, data>0.0)
          if key=='h':
            validFull = np.isfinite(np.array(branch[name], dtype=float))
          break

    if valid is None or validFull is None:
      print('**ERROR** Missing information for',measurementType.split()[0],': h or valid data')
      print('Keys exist',inFile)
      return False

    #Run through all items again and crop to only valid data
    parsed:dict[str, np.ndarray] = {}
    for key in nameDict:
      if key in ['__ignore__','__note__']:
        continue
      for name, multiplyer in nameDict[key]:
        if name in branch:
          data = np.array(branch[name], dtype=float)
          if key in ['h','p','t']:
            data = data[validFull]
          else:
            data = data[valid]
          parsed[key] = data*multiplyer
          setattr(self, key, data*multiplyer)
          inFile.remove(name)
          break

    # Test if essential items exist
    for attrib in ['h','t','p']:
      if attrib not in parsed or len(parsed[attrib])==0:
        print('**ERROR** Missing information for',measurementType.split()[0],': ',attrib)
        print('Keys exist',inFile)
        return False
    validInput = valid[validFull]
    hInput = parsed['h']
    pInput = parsed['p']
    tInput = parsed['t']
    slopeInput = parsed['slope'] if 'slope' in parsed else np.array([], dtype=float)
    phaseInput = parsed['phase'] if 'phase' in parsed else np.array([], dtype=float)
    preserveReadResults = any(name in parsed for name in ('k2p', 'hc', 'Ac', 'modulus', 'modulusRed', 'hardness'))
    self._setRawData(hInput, pInput, tInput, validInput,
                     slopeInput if len(slopeInput)>0 else None,
                     phaseInput if len(phaseInput)>0 else None,
                     preserveReadResults=preserveReadResults)

    #cleaning
    converter = self.datafile.attrs['uri']
    converter = converter.decode('utf-8') if isinstance(converter, bytes) else converter
    converter = converter.split('/')[-1]
    if converter == 'hap2hdf.py':
      ## Old and correct approach
      #Fischer-Scope reset the time multiple times
      resetPoints = np.where((self.t[1:]-self.t[:-1])<0)[0]
      if len(resetPoints)>0:
        self._setRawData(self.raw.h[resetPoints[-1]:], self.raw.p[resetPoints[-1]:],
                         self.raw.t[resetPoints[-1]:], np.ones_like(self.raw.t[resetPoints[-1]:], dtype=bool),
                         self.raw.slope[resetPoints[-1]:] if len(self.raw.slope)==len(self.raw.t) else self.raw.slope,
                         self.raw.phase[resetPoints[-1]:] if len(self.raw.phase)==len(self.raw.t) else self.raw.phase)
    else:
      self._setRawData(self.raw.h, self.raw.p-self.raw.p[0], self.raw.t, self.raw.valid,
                       self.raw.slope, self.raw.phase)
    if hasattr(self, 'slope') and np.ndim(self.slope)>0 and len(self.slope)>60: #if more than 30: CSM
      self.method = Method.CSM
    if self.output['plotLoadHoldUnload']:
      self.plotTestingMethod()
    self._removeTooCloseInputPoints()
    source = self.vendor.name
    self._setRawData(self.h, self.p, self.t, self.valid,
                     self.slope if isinstance(self.slope, np.ndarray) else None,
                     self.phase if isinstance(self.phase, np.ndarray) else None, {
      'h': {'source': f'{source}_loaded_depth', 'surface': False, 'drift': False, 'frameCompliance': False},
      'p': {'source': f'{source}_loaded_load', 'tare': False},
      'slope': {'source': f'{source}_loaded_stiffness', 'frameCompliance': False}
    }, preserveReadResults=preserveReadResults)
    return True


  @staticmethod
  def isfloat(value:str) -> bool:
    """
    Determine if value is float

    Args:
      value (float): number to be tested

    Returns:
      bool: result
    """
    try:
      float(value)
      return True
    except ValueError:
      return False


  def restartFile(self:'Indentation') -> None: # type: ignore[misc]
    """
    Restart processing the current file by resetting all values back to the initial
    """
    self.testList = list(self.allTestList)
    self.nextTest()
    return
