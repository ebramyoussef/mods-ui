import sys
import PyQt5
import os
import json
from PyQt5.uic import loadUi
from os import path
from qtpy import QtCore
from pydm import Display
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QDoubleValidator, QValidator
from pydm.widgets import PyDMEmbeddedDisplay, PyDMShellCommand
from pydm.utilities import connection
from ophyd import EpicsSignal, EpicsSignalRO
"""
    
"""


class Injection_diagram(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(Injection_diagram, self).__init__(parent=parent, args=args, macros=macros)
        self.ui.INJ_MP1_MR1.clicked.connect(self.gotocontrol)#that is use as Expert Screen
        self.ui.expertscreen.clicked.connect(self.gotoexpert)# func tool partial
        self.ui.expertscreen_2.clicked.connect(self.gotoexpert)
        self.ui.BlockPump.clicked.connect(self.gotopump)
        self.ui.BlockATM.clicked.connect(self.gotoatm)
        self.ui.out.clicked.connect(self.goout)
        #print(self.ui.embeddedControl.__dict__)
        self.ui.embeddedControl.embedded_widget.tip_mm.clicked.connect(self.emb_tip_mm)
        self.ui.embeddedControl.embedded_widget.tip_m.clicked.connect(self.emb_tip_m)
        self.ui.embeddedControl.embedded_widget.tip_p.clicked.connect(self.emb_tip_p)
        self.ui.embeddedControl.embedded_widget.tip_pp.clicked.connect(self.emb_tip_pp)
        self.ui.embeddedControl.embedded_widget.tilt_mm.clicked.connect(self.emb_tilt_mm)
        self.ui.embeddedControl.embedded_widget.tilt_m.clicked.connect(self.emb_tilt_m)
        self.ui.embeddedControl.embedded_widget.tilt_p.clicked.connect(self.emb_tilt_p)
        self.ui.embeddedControl.embedded_widget.tilt_pp.clicked.connect(self.emb_tilt_pp)
        self.ui.tip_step_size = EpicsSignalRO('LM1K2:MCS2:01:m1:STEP_COUNT', name = 'm1_step_size')
        self.ui.tilt_step_size = EpicsSignalRO('LM1K2:MCS2:01:m2:STEP_COUNT', name = 'm2_step_size')
        self.ui.tip_total_step = EpicsSignal('LM1K2:MCS2:01:m1:TOTAL_STEP_COUNT', write_pv = "LM1K2:MCS2:01:m1:SET_TOTAL_STEP_COUNT", name = 'tip_steps')
        self.ui.tilt_total_step = EpicsSignal('LM1K2:MCS2:01:m2:TOTAL_STEP_COUNT', write_pv = "LM1K2:MCS2:01:m2:SET_TOTAL_STEP_COUNT", name = 'tilt_steps')
        self.max_step_tip = 1000
        self.max_step_tilt = 1000
        self.INJ_DP2_MR1_pos = EpicsSignal('LM1K2:MCS2:01:m3.DRBV', write_pv = "LM1K2:MCS2:01:m3.VAL", name = 'DP2_MR1_pos')
        
    def emb_tip_mm(self):
        newnumber = self.ui.tip_total_step.get() - self.ui.tip_step_size.get()
        if newnumber <= 0:
            self.ui.tip_total_step.put(0)
        else:
            self.ui.tip_total_step.put(newnumber)
    def emb_tip_m(self):
        newnumber = self.ui.tip_total_step.get() - 1
        if newnumber <= 0:
            self.ui.tip_total_step.put(0)
        else:
            self.ui.tip_total_step.put(newnumber)
    def emb_tip_p(self):
        newnumber = self.ui.tip_total_step.get() + 1
        if newnumber >= self.max_step_tip :
            self.ui.tip_total_step.put(self.max_step_tip)
        else:
            self.ui.tip_total_step.put(newnumber)
    def emb_tip_pp(self):
        newnumber = self.ui.tip_total_step.get() + self.ui.tip_step_size.get()
        if newnumber >= self.max_step_tip:
            self.ui.tip_total_step.put(self.max_step_tip)
        else:
            self.ui.tip_total_step.put(newnumber)
    def emb_tilt_mm(self):
        newnumber = self.ui.tilt_total_step.get() - self.ui.tilt_step_size.get()
        if newnumber <= 0:
            self.ui.tilt_total_step.put(0)
        else:
            self.ui.tilt_total_step.put(newnumber)
    def emb_tilt_m(self):
        newnumber = self.ui.tilt_total_step.get() - 1
        if newnumber <= 0:
            self.ui.tilt_total_step.put(0)
        else:
            self.ui.tilt_total_step.put(newnumber)
    def emb_tilt_p(self):
        newnumber = self.ui.tilt_total_step.get() + 1
        if newnumber >= self.max_step_tilt:
            self.ui.tilt_total_step.put(self.max_step_tilt)
        else:
            self.ui.tilt_total_step.put(newnumber)
    def emb_tilt_pp(self):
        newnumber = self.ui.tilt_total_step.get() + self.ui.tilt_step_size.get()
        if newnumber >= self.max_step_tilt:
            self.ui.tilt_total_step.put(self.max_step_tilt)
        else:
            self.ui.tilt_total_step.put(newnumber)

    def ui_filename(self):
        return "Injection_diagram.ui"

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())


    def gotoexpert(self):#(self, equip_name)
        expertscreen = Expert()
        expertscreen.setModal(True)
        expertscreen.show()

    def gotopump(self):
        self.INJ_DP2_MR1.setGeometry(880,230,181,41)
        self.purpleVert.setGeometry(880,170,141,201)
        self.redVert.setGeometry(951,140,20,121)
        self.redcamera2.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
        self.purplecamera2.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        #new_pos = self.INJ_DP2_MR1_pos.get - 1
        self.INJ_DP2_MR1_pos.put(2)

    def gotoatm(self):
        self.INJ_DP2_MR1.setGeometry(870,230,181,41)
        self.purpleVert.setGeometry(880,200,141,51)
        self.redVert.setGeometry(951,140,20,111)
        self.redcamera2.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
        self.purplecamera2.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
        #new_pos = self.INJ_DP2_MR1_pos.get - 1.5
        self.INJ_DP2_MR1_pos.put(1.5)

    def goout(self):
        self.INJ_DP2_MR1.setGeometry(920,230,181,41)
        self.purpleVert.setGeometry(880,170,141,201)
        self.redVert.setGeometry(951,140,20,211)
        self.redcamera2.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.purplecamera2.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        #new_pos = self.INJ_DP2_MR1_pos.get - 1
        self.INJ_DP2_MR1_pos.put(3)

    def mirrortext(self):
        self.mirrorwords.setText("No number")


    def gotocontrol(self):
        self.controlfile = mirrorscreen()
        self.controlfile.setModal(True)
        self.controlfile.exec()
        #controlfile.show()
 
class mirrorscreen(QDialog):
    def __init__(self):#, parent=None, args=None, macros=None):
        super(mirrorscreen, self).__init__()#parent=parent, args=args, macros=macros)
        loadUi("littlecontrol.ui", self)
        self.tip_step= int(self.initialtip.text())
        self.tilt_step= int(self.initialtilt.text())
        self.tip_large_step = int(self.TipLargeStep.text())
        self.tilt_large_step = int(self.TiltLargeStep.text())
        self.ChangeStep.clicked.connect(self.changeCurrentSetup)
        ## four lineEdit
        ##do not have to write enterpressed to fire (dont know the connect work, maybe comments aboved solved it)

        self.small_step = 1
        # just for ramdon try, will be connected to the channel
        self.max_step_tip = int(self.TipRange.text())#12030 
        self.max_step_tilt = int(self.TiltRange.text())#2550
        # large step will now be pulg in by hand

        self.tip_mm.clicked.connect(self.mm_tip)
        self.tip_m.clicked.connect(self.m_tip)
        self.tip_p.clicked.connect(self.p_tip)
        self.tip_pp.clicked.connect(self.pp_tip)
        self.tilt_mm.clicked.connect(self.mm_tilt)
        self.tilt_m.clicked.connect(self.m_tilt)
        self.tilt_p.clicked.connect(self.p_tilt)
        self.tilt_pp.clicked.connect(self.pp_tilt)

    #def ui_filename(self):
    #    return "littlecontrol.ui"

    #def ui_filepath(self):
    #    return path.join(path.dirname(path.realpath(__file__)), self.ui_filename)

    def changeCurrentSetup(self):
        # max step will remove later
        #self.max_step_tip = int(self.TipRange.text()) 
        #self.max_step_tilt = int(self.TiltRange.text())
        self.tip_step= int(float(self.initialtip.text()))
        self.initialtip.setText(str(self.tip_step))
        self.tilt_step= int(float(self.initialtilt.text()))
        self.initialtilt.setText(str(self.tilt_step))
        self.tip_large_step = int(float(self.TipLargeStep.text()))
        self.TipLargeStep.setText(str(self.tip_large_step))
        self.tilt_large_step = int(float(self.TiltLargeStep.text()))
        self.TiltLargeStep.setText(str(self.tilt_large_step))
            
        
##################### for Tip Buttons  
    def mm_tip(self):
        newnumber = self.tip_step - self.tip_large_step
        if newnumber <= 0:
            self.tip_step = 0
        else:
            self.tip_step = newnumber
        self.initialtip.setText(str(self.tip_step))
            
    def m_tip(self):
        newnumber = self.tip_step - self.small_step
        if newnumber <= 0:
            self.tip_step = 0
        else:
            self.tip_step = newnumber
        self.initialtip.setText(str(self.tip_step))
                
    def p_tip(self):
        newnumber = self.tip_step + self.small_step
        if newnumber >= self.max_step_tip:
            self.tip_step = self.max_step_tip
        else:
            self.tip_step = newnumber
        self.initialtip.setText(str(self.tip_step))
                
    def pp_tip(self):
        newnumber = self.tip_step + self.tip_large_step
        if newnumber >= self.max_step_tip:
            self.tip_step = self.max_step_tip
        else:
            self.tip_step = newnumber
        self.initialtip.setText(str(self.tip_step))
##################### for Tilt Buttons
    def mm_tilt(self):
        newnumber = self.tilt_step - self.tilt_large_step
        if newnumber <= 0:
            self.tilt_step = 0
        else:
            self.tilt_step = newnumber
        self.initialtilt.setText(str(self.tilt_step))
            
    def m_tilt(self):
        newnumber = self.tilt_step - self.small_step
        if newnumber <= 0:
            self.tilt_step = 0
        else:
            self.tilt_step = newnumber
        self.initialtilt.setText(str(self.tilt_step))
                
    def p_tilt(self):
        newnumber = self.tilt_step + self.small_step
        if newnumber >= self.max_step_tilt:
            self.tilt_step = self.max_step_tilt
        else:
            self.tilt_step = newnumber
        self.initialtilt.setText(str(self.tilt_step))
                
    def pp_tilt(self):
        newnumber = self.tilt_step + self.tilt_large_step
        if newnumber >= self.max_step_tilt:
            self.tilt_step = self.max_step_tilt
        else:
            self.tilt_step = newnumber
        self.initialtilt.setText(str(self.tilt_step))
##################### Tilt Buttons Above
        

class Expert(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(Expert, self).__init__(parent=parent, args=args, macros=macros)
        self.value.returnPressed.connect(self.applynumber)
        self.apply.clicked.connect(self.applynumber)

    def ui_filename(self):
        return "ExpertScreen.ui"

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())

    def applynumber(self):
        number = float(self.value.text())
        number = int(number)
        print(number)

        if len(str(number)) == 0:
            self.errortext.setText("No number")
        else:
            self.value.setText(str(number))
            self.errortext.setText("")
    



    
#main
app = QApplication(sys.argv)
injection = Injection_diagram()
widget = QtWidgets.QStackedWidget()
widget.addWidget(injection)
widget.setFixedHeight(486)
widget.setFixedWidth(1214)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("exiting")
