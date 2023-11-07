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
from pydm.widgets import PyDMEmbeddedDisplay
from pydm.utilities import connection
from ophyd import EpicsSignal, EpicsSignalRO

# test


class Harmonic_diagram(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(Harmonic_diagram, self).__init__(
            parent=parent, args=args, macros=macros
        )
        #########START the MAIN Screen Buttons#############
        self.ui.HRM_MP1_MR1_expert.clicked.connect(self.gotocontrol)
        self.ui.HRM_MP3_MR1_expert.clicked.connect(self.gotocontrol)
        self.ui.HRM_MP1_MR4_expert.clicked.connect(self.gotocontrol)
        self.ui.HRM_MP1_MR7_expert.clicked.connect(self.gotocontrol)
        self.ui.HRM_MP1_MR8_expert.clicked.connect(self.gotocontrol)
        self.ui.HRM_MP3_MR2_expert.clicked.connect(self.gotocontrol)

        self.ui.MP1_MR1_SHG_THG.clicked.connect(self.gotoMP1_MR1_SHG_THG)
        self.ui.MP1_MR1_Bypass_800.clicked.connect(self.gotoMP1_MR1_Bypass_800)
        # self.ui.MP1_MR1_expert.clicked.connect(self.gotoexpert)#may delete later

        # self.ui.MP3_MR1_expert.clicked.connect(self.gotoexpert)#may delete later
        self.ui.MP1_SPO1_SHG.clicked.connect(self.gotoMP1_SPO1_SHG)
        self.ui.MP1_SPO1_THG.clicked.connect(self.gotoMP1_SPO1_THG)
        # self.ui.MP1_SPO1_expert.clicked.connect(self.gotoexpert)
        # self.ui.MP1_PC1_SHG.clicked.connect(self.gotoMP1_PC1_SHG)
        # self.ui.MP1_PC1_THG.clicked.connect(self.gotoMP1_PC1_THG)
        self.ui.MP1_MR8_SHG_THG.clicked.connect(self.gotoMP1_MR8_SHG_THG)
        self.ui.MP1_MR8_Bypass.clicked.connect(self.gotoMP1_MR8_Bypass)
        # self.ui.MP1_MR8_expert.clicked.connect(self.gotoexpert)#may delete later
        self.ui.MP3_MR2_Output.clicked.connect(self.gotoMP3_MR2_Output)
        self.ui.MP3_MR2_Diag.clicked.connect(self.gotoMP3_MR2_Diag)
        self.ui.MP3_MR2_800.clicked.connect(self.gotoMP3_MR2_800)
        # self.ui.MP3_MR2_expert.clicked.connect(self.gotoexpert)#may delete later
        #########START the Embedded Buttons#############

        self.ui.embeddedControl_MP1_MR1.embedded_widget.tip_mm.clicked.connect(
            self.tip11mm
        )
        self.ui.embeddedControl_MP3_MR1.embedded_widget.tip_mm.clicked.connect(
            self.tip31mm
        )
        self.ui.embeddedControl_MP1_MR4.embedded_widget.tip_mm.clicked.connect(
            self.tip14mm
        )
        self.ui.embeddedControl_MP1_MR7.embedded_widget.tip_mm.clicked.connect(
            self.tip17mm
        )
        self.ui.embeddedControl_MP1_MR8.embedded_widget.tip_mm.clicked.connect(
            self.tip18mm
        )
        self.ui.embeddedControl_MP3_MR2.embedded_widget.tip_mm.clicked.connect(
            self.tip32mm
        )
        self.ui.embeddedControl_MP1_MR1.embedded_widget.tip_m.clicked.connect(
            self.tip11m
        )
        self.ui.embeddedControl_MP3_MR1.embedded_widget.tip_m.clicked.connect(
            self.tip31m
        )
        self.ui.embeddedControl_MP1_MR4.embedded_widget.tip_m.clicked.connect(
            self.tip14m
        )
        self.ui.embeddedControl_MP1_MR7.embedded_widget.tip_m.clicked.connect(
            self.tip17m
        )
        self.ui.embeddedControl_MP1_MR8.embedded_widget.tip_m.clicked.connect(
            self.tip18m
        )
        self.ui.embeddedControl_MP3_MR2.embedded_widget.tip_m.clicked.connect(
            self.tip32m
        )
        self.ui.embeddedControl_MP1_MR1.embedded_widget.tip_p.clicked.connect(
            self.tip11p
        )
        self.ui.embeddedControl_MP3_MR1.embedded_widget.tip_p.clicked.connect(
            self.tip31p
        )
        self.ui.embeddedControl_MP1_MR4.embedded_widget.tip_p.clicked.connect(
            self.tip14p
        )
        self.ui.embeddedControl_MP1_MR7.embedded_widget.tip_p.clicked.connect(
            self.tip17p
        )
        self.ui.embeddedControl_MP1_MR8.embedded_widget.tip_p.clicked.connect(
            self.tip18p
        )
        self.ui.embeddedControl_MP3_MR2.embedded_widget.tip_p.clicked.connect(
            self.tip32p
        )
        self.ui.embeddedControl_MP1_MR1.embedded_widget.tip_pp.clicked.connect(
            self.tip11pp
        )
        self.ui.embeddedControl_MP3_MR1.embedded_widget.tip_pp.clicked.connect(
            self.tip31pp
        )
        self.ui.embeddedControl_MP1_MR4.embedded_widget.tip_pp.clicked.connect(
            self.tip14pp
        )
        self.ui.embeddedControl_MP1_MR7.embedded_widget.tip_pp.clicked.connect(
            self.tip17pp
        )
        self.ui.embeddedControl_MP1_MR8.embedded_widget.tip_pp.clicked.connect(
            self.tip18pp
        )
        self.ui.embeddedControl_MP3_MR2.embedded_widget.tip_pp.clicked.connect(
            self.tip32pp
        )

        self.ui.embeddedControl_MP1_MR1.embedded_widget.tilt_mm.clicked.connect(
            self.tilt11mm
        )
        self.ui.embeddedControl_MP3_MR1.embedded_widget.tilt_mm.clicked.connect(
            self.tilt31mm
        )
        self.ui.embeddedControl_MP1_MR4.embedded_widget.tilt_mm.clicked.connect(
            self.tilt14mm
        )
        self.ui.embeddedControl_MP1_MR7.embedded_widget.tilt_mm.clicked.connect(
            self.tilt17mm
        )
        self.ui.embeddedControl_MP1_MR8.embedded_widget.tilt_mm.clicked.connect(
            self.tilt18mm
        )
        self.ui.embeddedControl_MP3_MR2.embedded_widget.tilt_mm.clicked.connect(
            self.tilt32mm
        )
        self.ui.embeddedControl_MP1_MR1.embedded_widget.tilt_m.clicked.connect(
            self.tilt11m
        )
        self.ui.embeddedControl_MP3_MR1.embedded_widget.tilt_m.clicked.connect(
            self.tilt31m
        )
        self.ui.embeddedControl_MP1_MR4.embedded_widget.tilt_m.clicked.connect(
            self.tilt14m
        )
        self.ui.embeddedControl_MP1_MR7.embedded_widget.tilt_m.clicked.connect(
            self.tilt17m
        )
        self.ui.embeddedControl_MP1_MR8.embedded_widget.tilt_m.clicked.connect(
            self.tilt18m
        )
        self.ui.embeddedControl_MP3_MR2.embedded_widget.tilt_m.clicked.connect(
            self.tilt32m
        )
        self.ui.embeddedControl_MP1_MR1.embedded_widget.tilt_p.clicked.connect(
            self.tilt11p
        )
        self.ui.embeddedControl_MP3_MR1.embedded_widget.tilt_p.clicked.connect(
            self.tilt31p
        )
        self.ui.embeddedControl_MP1_MR4.embedded_widget.tilt_p.clicked.connect(
            self.tilt14p
        )
        self.ui.embeddedControl_MP1_MR7.embedded_widget.tilt_p.clicked.connect(
            self.tilt17p
        )
        self.ui.embeddedControl_MP1_MR8.embedded_widget.tilt_p.clicked.connect(
            self.tilt18p
        )
        self.ui.embeddedControl_MP3_MR2.embedded_widget.tilt_p.clicked.connect(
            self.tilt32p
        )
        self.ui.embeddedControl_MP1_MR1.embedded_widget.tilt_pp.clicked.connect(
            self.tilt11pp
        )
        self.ui.embeddedControl_MP3_MR1.embedded_widget.tilt_pp.clicked.connect(
            self.tilt31pp
        )
        self.ui.embeddedControl_MP1_MR4.embedded_widget.tilt_pp.clicked.connect(
            self.tilt14pp
        )
        self.ui.embeddedControl_MP1_MR7.embedded_widget.tilt_pp.clicked.connect(
            self.tilt17pp
        )
        self.ui.embeddedControl_MP1_MR8.embedded_widget.tilt_pp.clicked.connect(
            self.tilt18pp
        )
        self.ui.embeddedControl_MP3_MR2.embedded_widget.tilt_pp.clicked.connect(
            self.tilt32pp
        )

        self.MP1_SPO1_pos = EpicsSignal(
            "LM1K4:HRM_MP1_SPO1.DRBV",
            write_pv="LM1K4:HRM_MP1_SPO1.VAL",
            name="MP1_SPO1_pos",
        )
        self.MP1_PC1_pos = EpicsSignal(
            "LM1K4:HRM_MP1_PC1.DRBV",
            write_pv="LM1K4:HRM_MP1_PC1.VAL",
            name="MP1_PC1_pos",
        )
        self.MP1_PC11_PZM2_pos = EpicsSignal(
            "LM1K4:HRM_MP1_PC1_PZM2.DRBV",
            write_pv="LM1K4:HRM_MP1_PC1_PZM2.VAL",
            name="MP1_PC1_PZM2_pos",
        )

        self.ui.MP1_MR1_tip_step_size = EpicsSignalRO(
            "LM1K4:HRM_MP1_MR1_TIP1:STEP_COUNT", name="MP1_MR1_tip_step_size"
        )
        self.ui.MP1_MR1_tilt_step_size = EpicsSignalRO(
            "LM1K4:HRM_MP1_MR1_TILT1:STEP_COUNT", name="MP1_MR1_tilt_step_size"
        )
        self.ui.MP1_MR1_tip_total_step = EpicsSignal(
            "LM1K4:HRM_MP1_MR1_TIP1:TOTAL_STEP_COUNT",
            write_pv="LM1K4:HRM_MP1_MR1_TIP1:SET_TOTAL_STEP_COUNT",
            name="MP1_MR1_tip_steps",
        )
        self.ui.MP1_MR1_tilt_total_step = EpicsSignal(
            "LM1K4:HRM_MP1_MR1_TILT1:TOTAL_STEP_COUNT",
            write_pv="LM1K4:HRM_MP1_MR1_TILT1:SET_TOTAL_STEP_COUNT",
            name="MP1_MR1_tilt_steps",
        )
        # self.MP1_MR1_max_step_tip = 1000
        # self.MP1_MR1_max_step_tilt = 1000
        self.MP1_MR1_pos = EpicsSignal(
            "LM1K4:HRM_MP1_MR1_LM1.DRBV",
            write_pv="LM1K4:HRM_MP1_MR1_LM1.VAL",
            name="MP1_MR1_pos",
        )

        self.ui.MP3_MR1_tip_step_size = EpicsSignalRO(
            "LM1K4:HRM_MP3_MR1_TIP1:STEP_COUNT", name="MP3_MR1_tip_step_size"
        )
        self.ui.MP3_MR1_tilt_step_size = EpicsSignalRO(
            "LM1K4:HRM_MP3_MR1_TILT1:STEP_COUNT", name="MP3_MR1_tilt_step_size"
        )
        self.ui.MP3_MR1_tip_total_step = EpicsSignal(
            "LM1K4:HRM_MP3_MR1_TIP1:TOTAL_STEP_COUNT",
            write_pv="LM1K4:HRM_MP3_MR1_TIP1:SET_TOTAL_STEP_COUNT",
            name="MP3_MR1_tip_steps",
        )
        self.ui.MP3_MR1_tilt_total_step = EpicsSignal(
            "LM1K4:HRM_MP3_MR1_TILT1:TOTAL_STEP_COUNT",
            write_pv="LM1K4:HRM_MP3_MR1_TILT1:SET_TOTAL_STEP_COUNT",
            name="MP3_MR1_tilt_steps",
        )

        self.ui.MP1_MR4_tip_step_size = EpicsSignalRO(
            "LM1K4:HRM_MP1_MR4_TIP1:STEP_COUNT", name="MP1_MR4_tip_step_size"
        )
        self.ui.MP1_MR4_tilt_step_size = EpicsSignalRO(
            "LM1K4:HRM_MP1_MR4_TILT1:STEP_COUNT", name="MP1_MR4_tilt_step_size"
        )
        self.ui.MP1_MR4_tip_total_step = EpicsSignal(
            "LM1K4:HRM_MP1_MR4_TIP1:TOTAL_STEP_COUNT",
            write_pv="LM1K4:HRM_MP1_MR4_TIP1:SET_TOTAL_STEP_COUNT",
            name="MP1_MR4_tip_steps",
        )
        self.ui.MP1_MR4_tilt_total_step = EpicsSignal(
            "LM1K4:HRM_MP1_MR4_TILT1:TOTAL_STEP_COUNT",
            write_pv="LM1K4:HRM_MP1_MR4_TILT1:SET_TOTAL_STEP_COUNT",
            name="MP1_MR4_tilt_steps",
        )

        self.ui.MP1_MR7_tip_step_size = EpicsSignalRO(
            "LM1K4:HRM_MP1_MR7_TIP1:STEP_COUNT", name="MP1_MR7_tip_step_size"
        )
        self.ui.MP1_MR7_tilt_step_size = EpicsSignalRO(
            "LM1K4:HRM_MP1_MR7_TILT1:STEP_COUNT", name="MP1_MR7_tilt_step_size"
        )
        self.ui.MP1_MR7_tip_total_step = EpicsSignal(
            "LM1K4:HRM_MP1_MR7_TIP1:TOTAL_STEP_COUNT",
            write_pv="LM1K4:HRM_MP1_MR7_TIP1:SET_TOTAL_STEP_COUNT",
            name="MP1_MR7_tip_steps",
        )
        self.ui.MP1_MR7_tilt_total_step = EpicsSignal(
            "LM1K4:HRM_MP1_MR7_TILT1:TOTAL_STEP_COUNT",
            write_pv="LM1K4:HRM_MP1_MR7_TILT1:SET_TOTAL_STEP_COUNT",
            name="MP1_MR7_tilt_steps",
        )

        self.ui.MP1_MR8_tip_step_size = EpicsSignalRO(
            "LM1K4:HRM_MP1_MR8_TIP1:STEP_COUNT", name="MP1_MR8_tip_step_size"
        )
        self.ui.MP1_MR8_tilt_step_size = EpicsSignalRO(
            "LM1K4:HRM_MP1_MR8_TILT1:STEP_COUNT", name="MP1_MR8_tilt_step_size"
        )
        self.ui.MP1_MR8_tip_total_step = EpicsSignal(
            "LM1K4:HRM_MP1_MR8_TIP1:TOTAL_STEP_COUNT",
            write_pv="LM1K4:HRM_MP1_MR8_TIP1:SET_TOTAL_STEP_COUNT",
            name="MP1_MR8_tip_steps",
        )
        self.ui.MP1_MR8_tilt_total_step = EpicsSignal(
            "LM1K4:HRM_MP1_MR8_TILT1:TOTAL_STEP_COUNT",
            write_pv="LM1K4:HRM_MP1_MR8_TILT1:SET_TOTAL_STEP_COUNT",
            name="MP1_MR8_tilt_steps",
        )
        self.MP1_MR8_pos = EpicsSignal(
            "LM1K4:HRM_MP1_MR8_LM1.DRBV",
            write_pv="LM1K4:HRM_MP1_MR8_LM1.VAL",
            name="MP1_MR8_pos",
        )

        self.ui.MP3_MR2_tip_step_size = EpicsSignalRO(
            "LM1K4:HRM_MP3_MR2_TIP1:STEP_COUNT", name="MP3_MR2_tip_step_size"
        )
        self.ui.MP3_MR2_tilt_step_size = EpicsSignalRO(
            "LM1K4:HRM_MP3_MR2_TILT1:STEP_COUNT", name="MP3_MR2_tilt_step_size"
        )
        self.ui.MP3_MR2_tip_total_step = EpicsSignal(
            "LM1K4:HRM_MP3_MR2_TIP1:TOTAL_STEP_COUNT",
            write_pv="LM1K4:HRM_MP3_MR2_TIP1:SET_TOTAL_STEP_COUNT",
            name="MP3_MR2_tip_steps",
        )
        self.ui.MP3_MR2_tilt_total_step = EpicsSignal(
            "LM1K4:HRM_MP3_MR2_TILT1:TOTAL_STEP_COUNT",
            write_pv="LM1K4:HRM_MP3_MR2_TILT1:SET_TOTAL_STEP_COUNT",
            name="MP3_MR2_tilt_steps",
        )
        self.MP3_MR2_pos = EpicsSignal(
            "LM1K4:HRM_MP3_MR2_LM1.DRBV",
            write_pv="LM1K4:HRM_MP3_MR2_LM1.VAL",
            name="MP3_MR2_pos",
        )

    def tip11mm(self):
        newnumber = (
            self.ui.MP1_MR1_tip_total_step.get()
            - self.ui.MP1_MR1_tip_step_size.get()
        )
        # if newnumber <= 0:
        #    self.ui.MP1_MR1_tip_total_step.put(0)
        # else:
        self.ui.MP1_MR1_tip_total_step.put(newnumber)

    def tip31mm(self):
        newnumber = (
            self.ui.MP3_MR1_tip_total_step.get()
            - self.ui.MP3_MR1_tip_step_size.get()
        )
        self.ui.MP3_MR1_tip_total_step.put(newnumber)

    def tip14mm(self):
        newnumber = (
            self.ui.MP1_MR4_tip_total_step.get()
            - self.ui.MP1_MR4_tip_step_size.get()
        )
        self.ui.MP1_MR4_tip_total_step.put(newnumber)

    def tip17mm(self):
        newnumber = (
            self.ui.MP1_MR7_tip_total_step.get()
            - self.ui.MP1_MR7_tip_step_size.get()
        )
        self.ui.MP1_MR7_tip_total_step.put(newnumber)

    def tip18mm(self):
        newnumber = (
            self.ui.MP1_MR8_tip_total_step.get()
            - self.ui.MP1_MR8_tip_step_size.get()
        )
        self.ui.MP1_MR8_tip_total_step.put(newnumber)

    def tip32mm(self):
        newnumber = (
            self.ui.MP3_MR2_tip_total_step.get()
            - self.ui.MP3_MR2_tip_step_size.get()
        )
        self.ui.MP3_MR2_tip_total_step.put(newnumber)

    def tip11m(self):
        newnumber = self.ui.MP1_MR1_tip_total_step.get() - 1
        self.ui.MP1_MR1_tip_total_step.put(newnumber)

    def tip31m(self):
        newnumber = self.ui.MP3_MR1_tip_total_step.get() - 1
        self.ui.MP3_MR1_tip_total_step.put(newnumber)

    def tip14m(self):
        newnumber = self.ui.MP1_MR4_tip_total_step.get() - 1
        self.ui.MP1_MR4_tip_total_step.put(newnumber)

    def tip17m(self):
        newnumber = self.ui.MP1_MR7_tip_total_step.get() - 1
        self.ui.MP1_MR7_tip_total_step.put(newnumber)

    def tip18m(self):
        newnumber = self.ui.MP1_MR8_tip_total_step.get() - 1
        self.ui.MP1_MR8_tip_total_step.put(newnumber)

    def tip32m(self):
        newnumber = self.ui.MP3_MR2_tip_total_step.get() - 1
        self.ui.MP3_MR2_tip_total_step.put(newnumber)

    def tip11p(self):
        newnumber = self.ui.MP1_MR1_tip_total_step.get() + 1
        self.ui.MP1_MR1_tip_total_step.put(newnumber)

    def tip31p(self):
        newnumber = self.ui.MP3_MR1_tip_total_step.get() + 1
        # if newnumber >= self.MP3_MR1_max_step_tip:
        #    self.ui.MP3_MR1_tip_total_step.put(self.MP3_MR1_max_step_tip)
        # else:
        self.ui.MP3_MR1_tip_total_step.put(newnumber)

    def tip14p(self):
        newnumber = self.ui.MP1_MR4_tip_total_step.get() + 1
        elf.ui.MP1_MR4_tip_total_step.put(newnumber)

    def tip17p(self):
        newnumber = self.ui.MP1_MR7_tip_total_step.get() + 1
        self.ui.MP1_MR7_tip_total_step.put(newnumber)

    def tip18p(self):
        newnumber = self.ui.MP1_MR8_tip_total_step.get() + 1
        self.ui.MP1_MR8_tip_total_step.put(newnumber)

    def tip32p(self):
        newnumber = self.ui.MP3_MR2_tip_total_step.get() + 1
        self.ui.MP3_MR2_tip_total_step.put(newnumber)

    def tip11pp(self):
        newnumber = (
            self.ui.MP1_MR1_tip_total_step.get()
            + self.ui.MP1_MR1_tip_step_size.get()
        )
        self.ui.MP1_MR1_tip_total_step.put(newnumber)

    def tip31pp(self):
        newnumber = (
            self.ui.MP3_MR1_tip_total_step.get()
            + self.ui.MP3_MR1_tip_step_size.get()
        )
        self.ui.MP3_MR1_tip_total_step.put(newnumber)

    def tip14pp(self):
        newnumber = (
            self.ui.MP1_MR4_tip_total_step.get()
            + self.ui.MP1_MR4_tip_step_size.get()
        )
        self.ui.MP1_MR4_tip_total_step.put(newnumber)

    def tip17pp(self):
        newnumber = (
            self.ui.MP1_MR7_tip_total_step.get()
            + self.ui.MP1_MR7_tip_step_size.get()
        )
        self.ui.MP1_MR7_tip_total_step.put(newnumber)

    def tip18pp(self):
        newnumber = (
            self.ui.MP1_MR8_tip_total_step.get()
            + self.ui.MP1_MR8_tip_step_size.get()
        )
        self.ui.MP1_MR8_tip_total_step.put(newnumber)

    def tip32pp(self):
        newnumber = (
            self.ui.MP3_MR2_tip_total_step.get()
            + self.ui.MP3_MR2_tip_step_size.get()
        )
        self.ui.MP3_MR2_tip_total_step.put(newnumber)

    def tilt11mm(self):
        newnumber = (
            self.ui.MP1_MR1_tilt_total_step.get()
            - self.ui.MP1_MR1_tilt_step_size.get()
        )
        self.ui.MP1_MR1_tilt_total_step.put(newnumber)

    def tilt31mm(self):
        newnumber = (
            self.ui.MP3_MR1_tilt_total_step.get()
            - self.ui.MP3_MR1_tilt_step_size.get()
        )
        self.ui.MP3_MR1_tilt_total_step.put(newnumber)

    def tilt14mm(self):
        newnumber = (
            self.ui.MP1_MR4_tilt_total_step.get()
            - self.ui.MP1_MR4_tilt_step_size.get()
        )
        self.ui.MP1_MR4_tilt_total_step.put(newnumber)

    def tilt17mm(self):
        newnumber = (
            self.ui.MP1_MR7_tilt_total_step.get()
            - self.ui.MP1_MR7_tilt_step_size.get()
        )
        self.ui.MP1_MR7_tilt_total_step.put(newnumber)

    def tilt18mm(self):
        newnumber = (
            self.ui.MP1_MR8_tilt_total_step.get()
            - self.ui.MP1_MR8_tilt_step_size.get()
        )
        self.ui.MP1_MR8_tilt_total_step.put(newnumber)

    def tilt32mm(self):
        newnumber = (
            self.ui.MP3_MR2_tilt_total_step.get()
            - self.ui.MP3_MR2_tilt_step_size.get()
        )
        self.ui.MP3_MR2_tilt_total_step.put(newnumber)

    def tilt11m(self):
        newnumber = self.ui.MP1_MR1_tilt_total_step.get() - 1
        self.ui.MP1_MR1_tilt_total_step.put(newnumber)

    def tilt31m(self):
        newnumber = self.ui.MP3_MR1_tilt_total_step.get() - 1
        self.ui.MP3_MR1_tilt_total_step.put(newnumber)

    def tilt14m(self):
        newnumber = self.ui.MP1_MR4_tilt_total_step.get() - 1
        self.ui.MP1_MR4_tilt_total_step.put(newnumber)

    def tilt17m(self):
        newnumber = self.ui.MP1_MR7_tilt_total_step.get() - 1
        self.ui.MP1_MR7_tilt_total_step.put(newnumber)

    def tilt18m(self):
        newnumber = self.ui.MP1_MR8_tilt_total_step.get() - 1
        self.ui.MP1_MR8_tilt_total_step.put(newnumber)

    def tilt32m(self):
        newnumber = self.ui.MP3_MR2_tilt_total_step.get() - 1
        self.ui.MP3_MR2_tilt_total_step.put(newnumber)

    def tilt11p(self):
        newnumber = self.ui.MP1_MR1_tilt_total_step.get() + 1
        self.ui.MP1_MR1_tilt_total_step.put(newnumber)

    def tilt31p(self):
        newnumber = self.ui.MP3_MR1_tilt_total_step.get() + 1
        self.ui.MP3_MR1_tilt_total_step.put(newnumber)

    def tilt14p(self):
        newnumber = self.ui.MP1_MR4_tilt_total_step.get() + 1
        self.ui.MP1_MR4_tilt_total_step.put(newnumber)

    def tilt17p(self):
        newnumber = self.ui.MP1_MR7_tilt_total_step.get() + 1
        self.ui.MP1_MR7_tilt_total_step.put(newnumber)

    def tilt18p(self):
        newnumber = self.ui.MP1_MR8_tilt_total_step.get() + 1
        self.ui.MP1_MR8_tilt_total_step.put(newnumber)

    def tilt32p(self):
        newnumber = self.ui.MP3_MR2_tilt_total_step.get() + 1
        # if newnumber >= self.MP3_MR2_max_step_tilt:
        #    self.ui.MP3_MR2_tilt_total_step.put(self.MP3_MR2_max_step_tilt)
        # else:
        self.ui.MP3_MR2_tilt_total_step.put(newnumber)

    def tilt11pp(self):
        newnumber = (
            self.ui.MP1_MR1_tilt_total_step.get()
            + self.ui.MP1_MR1_tilt_step_size.get()
        )
        self.ui.MP1_MR1_tilt_total_step.put(newnumber)

    def tilt31pp(self):
        newnumber = (
            self.ui.MP3_MR1_tilt_total_step.get()
            + self.ui.MP3_MR1_tilt_step_size.get()
        )
        self.ui.MP3_MR1_tilt_total_step.put(newnumber)

    def tilt14pp(self):
        newnumber = (
            self.ui.MP1_MR4_tilt_total_step.get()
            + self.ui.MP1_MR4_tilt_step_size.get()
        )
        self.ui.MP1_MR4_tilt_total_step.put(newnumber)

    def tilt17pp(self):
        newnumber = (
            self.ui.MP1_MR7_tilt_total_step.get()
            + self.ui.MP1_MR7_tilt_step_size.get()
        )
        self.ui.MP1_MR7_tilt_total_step.put(newnumber)

    def tilt18pp(self):
        newnumber = (
            self.ui.MP1_MR8_tilt_total_step.get()
            + self.ui.MP1_MR8_tilt_step_size.get()
        )
        self.ui.MP1_MR8_tilt_total_step.put(newnumber)

    def tilt32pp(self):
        newnumber = (
            self.ui.MP3_MR2_tilt_total_step.get()
            + self.ui.MP3_MR2_tilt_step_size.get()
        )
        self.ui.MP3_MR2_tilt_total_step.put(newnumber)

    #########END the Embedded Buttons#############

    def gotoMP1_MR1_SHG_THG(self):
        self.MP1_MR1_pos.put(10)
        self.HRM_MP1_MR1.setGeometry(60, 160, 211, 41)
        self.PyDMDrawingLine.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_2.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
        self.PyDMDrawingLine_3.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
        self.PyDMDrawingLine_4.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_5.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
        self.PyDMDrawingLine_6.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_7.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        if self.HRM_MP1_SPO1_up.y() == 230:
            self.HAR_MP1_PC1.setGeometry(280, 380, 41, 41)
            self.HAR_MP1_PC1_2.setGeometry(240, 410, 31, 31)
            self.PyDMDrawingLine_8.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_8.setGeometry(40, 220, 471, 41)
            self.PyDMDrawingLine_8.penColor = PyQt5.QtGui.QColor(0, 0, 255)
            self.PyDMDrawingLine_9.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_9.setGeometry(430, 240, 81, 41)
            self.PyDMDrawingLine_9.penColor = PyQt5.QtGui.QColor(0, 0, 255)
            self.PyDMDrawingLine_16.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_16.setGeometry(290, 350, 671, 81)
            self.PyDMDrawingLine_16.penColor = PyQt5.QtGui.QColor(0, 0, 255)
            self.PyDMDrawingLine_17.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_17.setGeometry(240, 390, 71, 41)
            self.PyDMDrawingLine_17.penColor = PyQt5.QtGui.QColor(0, 0, 255)
            # self.PyDMDrawingLine_18.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_18.penColor = PyQt5.QtGui.QColor(0, 0, 255)
            self.PyDMDrawingLine_19.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_19.setGeometry(470, 240, 671, 81)
            self.PyDMDrawingLine_19.penColor = PyQt5.QtGui.QColor(0, 0, 255)
            self.PyDMDrawingLine_27.penColor = PyQt5.QtGui.QColor(0, 0, 255)
            # self.PyDMDrawingLine_27.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            # blue

            ###need change
            self.PyDMDrawingLine_11.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_11.penColor = PyQt5.QtGui.QColor(0, 0, 255)
            ###
            self.PyDMDrawingLine_12.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_12.penColor = PyQt5.QtGui.QColor(0, 0, 255)
            self.PyDMDrawingLine_13.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_13.penColor = PyQt5.QtGui.QColor(0, 0, 255)
            self.PyDMDrawingLine_14.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_14.penColor = PyQt5.QtGui.QColor(0, 0, 255)
            self.PyDMDrawingLine_21.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_21.setGeometry(470, 220, 41, 41)
            if self.HRM_DP2_MR1.x() == 990:
                self.PyDMDrawingLine_11.setGeometry(920, 310, 251, 91)
                self.PyDMDrawingLine_18.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.SolidLine
                )
                self.PyDMDrawingLine_27.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.SolidLine
                )
            elif self.HRM_DP2_MR1.x() > 990:
                self.PyDMDrawingLine_11.setGeometry(920, 330, 251, 261)
                self.PyDMDrawingLine_18.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.DashLine
                )
                self.PyDMDrawingLine_27.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.DashLine
                )
            if self.HRM_MP1_MR8.x() == 990:
                self.PyDMDrawingLine_14.setGeometry(890, 240, 301, 151)
            elif self.HRM_MP1_MR8.x() > 990:
                self.PyDMDrawingLine_14.setGeometry(900, 150, 381, 241)

        if self.HRM_MP1_SPO1_up.y() > 230:
            # pink
            self.HAR_MP1_PC1.setGeometry(570, 340, 41, 41)
            self.HAR_MP1_PC1_2.setGeometry(530, 370, 31, 31)
            self.PyDMDrawingLine_8.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_8.setGeometry(220, 200, 181, 81)
            self.PyDMDrawingLine_8.penColor = PyQt5.QtGui.QColor(254, 133, 232)
            self.PyDMDrawingLine_9.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_9.setGeometry(180, 240, 81, 41)
            self.PyDMDrawingLine_9.penColor = PyQt5.QtGui.QColor(254, 133, 232)
            self.PyDMDrawingLine_11.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_11.penColor = PyQt5.QtGui.QColor(
                254, 133, 232
            )
            self.PyDMDrawingLine_12.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_12.penColor = PyQt5.QtGui.QColor(
                254, 133, 232
            )
            self.PyDMDrawingLine_13.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_13.penColor = PyQt5.QtGui.QColor(
                254, 133, 232
            )
            self.PyDMDrawingLine_14.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_14.penColor = PyQt5.QtGui.QColor(
                254, 133, 232
            )
            self.PyDMDrawingLine_16.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_17.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_18.penColor = PyQt5.QtGui.QColor(
                254, 133, 232
            )
            self.PyDMDrawingLine_19.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_19.setGeometry(220, 240, 921, 81)
            self.PyDMDrawingLine_19.penColor = PyQt5.QtGui.QColor(
                254, 133, 232
            )
            self.PyDMDrawingLine_21.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_21.setGeometry(40, 220, 471, 41)
            self.PyDMDrawingLine_27.penColor = PyQt5.QtGui.QColor(
                254, 133, 232
            )
            if self.HRM_DP2_MR1.x() == 990:
                self.PyDMDrawingLine_11.setGeometry(920, 310, 251, 91)
                self.PyDMDrawingLine_18.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.SolidLine
                )
                self.PyDMDrawingLine_27.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.SolidLine
                )
            elif self.HRM_DP2_MR1.x() > 990:
                self.PyDMDrawingLine_11.setGeometry(920, 310, 251, 241)
                self.PyDMDrawingLine_18.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.DashLine
                )
                self.PyDMDrawingLine_27.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.DashLine
                )

    def gotoMP1_MR1_Bypass_800(self):
        self.MP1_MR1_pos.put(0)
        self.HRM_MP1_MR1.setGeometry(20, 160, 211, 41)
        self.PyDMDrawingLine_11.setGeometry(1000, 440, 91, 101)
        self.PyDMDrawingLine_11.penColor = PyQt5.QtGui.QColor(254, 0, 0)
        if self.HRM_MP3_MR1.x() == 60:
            self.PyDMDrawingLine.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
            self.PyDMDrawingLine_11.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
        else:
            self.PyDMDrawingLine.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_11.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
        self.PyDMDrawingLine_2.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_3.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_4.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
        self.PyDMDrawingLine_5.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_6.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_7.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_8.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_9.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        # self.PyDMDrawingLine_10.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_12.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_13.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_14.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_16.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_17.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_18.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_19.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_21.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_27.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine

    def gotoMP3_MR1_Bypass(self):
        # self.MP3_MR1_pos.put(0)
        self.HRM_MP3_MR1.setGeometry(20, 430, 211, 41)
        if self.HRM_MP1_MR1.x() < 60:
            self.PyDMDrawingLine.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_2.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_3.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_4.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_4.setGeometry(-70, 180, 471, 351)
            self.PyDMDrawingLine_5.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_6.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_7.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_8.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_9.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_11.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_12.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_13.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_14.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_16.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_17.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_18.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_19.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_21.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_27.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )

    def gotoMP3_MR1_800(self):
        # self.MP3_MR1_pos.put(10)
        self.HRM_MP3_MR1.setGeometry(60, 430, 211, 41)
        if self.HRM_MP1_MR1.x() < 60:
            self.PyDMDrawingLine.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
            self.PyDMDrawingLine_2.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_3.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_4.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_4.setGeometry(-10, 180, 351, 271)
            self.PyDMDrawingLine_5.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_6.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_7.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_8.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            self.PyDMDrawingLine_9.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
            if self.PyDMDrawingLine_11.y() > 310:
                self.PyDMDrawingLine_11.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.SolidLine
                )
            self.PyDMDrawingLine_12.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_13.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_14.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_16.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_17.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_18.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_19.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_21.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_27.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )

    def gotoMP1_SPO1_SHG(self):  # S is blue
        self.MP1_SPO1_pos.put(0)
        self.MP1_PC1_pos.put(0)
        self.MP1_PC11_PZM2_pos.put(0)
        self.HRM_MP1_SPO1_up.setGeometry(440, 230, 61, 20)
        self.HRM_MP1_SPO1_bot.setGeometry(440, 270, 61, 20)
        self.HAR_MP1_PC1.setGeometry(280, 380, 41, 41)
        self.HAR_MP1_PC1_2.setGeometry(240, 410, 31, 31)
        self.PyDMDrawingLine_8.penStyle = PyQt5.QtCore.Qt.PenStyle.DashLine
        self.PyDMDrawingLine_8.setGeometry(40, 220, 471, 41)
        self.PyDMDrawingLine_8.penColor = PyQt5.QtGui.QColor(0, 0, 255)
        self.PyDMDrawingLine_9.setGeometry(430, 240, 81, 41)
        self.PyDMDrawingLine_9.penColor = PyQt5.QtGui.QColor(0, 0, 255)
        self.PyDMDrawingLine_16.setGeometry(290, 350, 671, 81)
        self.PyDMDrawingLine_16.rotation = 0
        self.PyDMDrawingLine_16.penColor = PyQt5.QtGui.QColor(0, 0, 255)
        self.PyDMDrawingLine_17.setGeometry(240, 390, 71, 41)
        self.PyDMDrawingLine_17.penColor = PyQt5.QtGui.QColor(0, 0, 255)
        self.PyDMDrawingLine_18.penColor = PyQt5.QtGui.QColor(0, 0, 255)
        self.PyDMDrawingLine_19.setGeometry(470, 240, 671, 81)
        self.PyDMDrawingLine_19.penColor = PyQt5.QtGui.QColor(0, 0, 255)
        self.PyDMDrawingLine_12.penColor = PyQt5.QtGui.QColor(0, 0, 255)
        self.PyDMDrawingLine_13.penColor = PyQt5.QtGui.QColor(0, 0, 255)
        self.PyDMDrawingLine_14.penColor = PyQt5.QtGui.QColor(0, 0, 255)
        self.PyDMDrawingLine_27.penColor = PyQt5.QtGui.QColor(0, 0, 255)
        self.PyDMDrawingLine_21.setGeometry(470, 220, 41, 41)
        if self.HRM_MP1_MR1.x() == 60:
            self.PyDMDrawingLine_11.penColor = PyQt5.QtGui.QColor(0, 0, 255)
            # self.PyDMDrawingLine_9.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
            # self.PyDMDrawingLine_11.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
            # self.PyDMDrawingLine_12.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
            # self.PyDMDrawingLine_13.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
            # self.PyDMDrawingLine_14.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
            # self.PyDMDrawingLine_16.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
            # self.PyDMDrawingLine_17.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
            # self.PyDMDrawingLine_19.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
            # self.PyDMDrawingLine_21.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
            if self.HRM_DP2_MR1.x() == 990:
                self.PyDMDrawingLine_11.setGeometry(920, 310, 251, 91)
                self.PyDMDrawingLine_18.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.SolidLine
                )
                self.PyDMDrawingLine_27.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.SolidLine
                )
            elif self.HRM_DP2_MR1.x() > 990:
                self.PyDMDrawingLine_11.setGeometry(920, 330, 251, 261)
                self.PyDMDrawingLine_18.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.DashLine
                )
                self.PyDMDrawingLine_27.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.DashLine
                )

    def gotoMP1_SPO1_THG(self):  # pink
        self.MP1_SPO1_pos.put(10)
        self.MP1_PC1_pos.put(10)
        self.MP1_PC11_PZM2_pos.put(-10)
        self.HRM_MP1_SPO1_up.setGeometry(440, 260, 61, 20)
        self.HRM_MP1_SPO1_bot.setGeometry(440, 300, 61, 20)
        self.HAR_MP1_PC1.setGeometry(570, 340, 41, 41)
        self.HAR_MP1_PC1_2.setGeometry(530, 370, 31, 31)
        self.PyDMDrawingLine_8.setGeometry(220, 200, 181, 81)
        self.PyDMDrawingLine_8.penColor = PyQt5.QtGui.QColor(254, 133, 232)
        self.PyDMDrawingLine_9.setGeometry(180, 240, 81, 41)
        self.PyDMDrawingLine_9.penColor = PyQt5.QtGui.QColor(254, 133, 232)
        self.PyDMDrawingLine_16.setGeometry(580, 330, 381, 81)
        self.PyDMDrawingLine_16.rotation = -5.0
        self.PyDMDrawingLine_16.penColor = PyQt5.QtGui.QColor(254, 133, 232)
        self.PyDMDrawingLine_17.setGeometry(530, 350, 71, 41)
        self.PyDMDrawingLine_17.penColor = PyQt5.QtGui.QColor(254, 133, 232)
        self.PyDMDrawingLine_18.penColor = PyQt5.QtGui.QColor(254, 133, 232)
        self.PyDMDrawingLine_19.setGeometry(220, 240, 921, 81)
        self.PyDMDrawingLine_19.penColor = PyQt5.QtGui.QColor(254, 133, 232)
        self.PyDMDrawingLine_12.penColor = PyQt5.QtGui.QColor(254, 133, 232)
        self.PyDMDrawingLine_13.penColor = PyQt5.QtGui.QColor(254, 133, 232)
        self.PyDMDrawingLine_14.penColor = PyQt5.QtGui.QColor(254, 133, 232)
        self.PyDMDrawingLine_21.setGeometry(40, 220, 471, 41)
        self.PyDMDrawingLine_27.penColor = PyQt5.QtGui.QColor(254, 133, 232)
        if self.HRM_MP1_MR1.x() == 60:
            self.PyDMDrawingLine_11.penColor = PyQt5.QtGui.QColor(
                254, 133, 232
            )
            if self.HRM_DP2_MR1.x() == 990:
                self.PyDMDrawingLine_11.setGeometry(920, 310, 251, 91)
                self.PyDMDrawingLine_18.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.SolidLine
                )
                self.PyDMDrawingLine_27.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.SolidLine
                )
            elif self.HRM_DP2_MR1.x() > 990:
                self.PyDMDrawingLine_11.setGeometry(920, 330, 251, 261)
                self.PyDMDrawingLine_18.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.DashLine
                )
                self.PyDMDrawingLine_27.penStyle = (
                    PyQt5.QtCore.Qt.PenStyle.DashLine
                )

    def gotoMP1_PC1_SHG(self):
        return print(1)

    def gotoMP1_PC1_THG(self):
        return print(1)

    def gotoMP3_MR2_Diag(self):
        self.MP3_MR2_pos.put(0)
        self.HRM_DP2_MR1.setGeometry(990, 390, 111, 21)
        self.HRM_MP3_MR2.setGeometry(940, 430, 211, 41)
        self.PyDMDrawingLine.setGeometry(160, 400, 891, 101)
        if self.HRM_MP1_MR1.x() == 60:
            self.PyDMDrawingLine_18.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_27.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_11.setGeometry(920, 310, 251, 91)
        elif self.HRM_MP1_MR1.x() < 60:
            self.PyDMDrawingLine_11.setGeometry(1000, 440, 91, 101)

    def gotoMP3_MR2_Output(self):
        self.MP3_MR2_pos.put(10)
        self.HRM_DP2_MR1.setGeometry(1030, 390, 111, 21)
        self.HRM_MP3_MR2.setGeometry(980, 430, 211, 41)
        self.PyDMDrawingLine.setGeometry(160, 400, 931, 101)
        if self.HRM_MP1_MR1.x() == 60:
            self.PyDMDrawingLine_18.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_27.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_11.setGeometry(920, 310, 251, 241)
        elif self.HRM_MP1_MR1.x() < 60:
            self.PyDMDrawingLine_11.setGeometry(960, 450, 251, 101)

    def gotoMP1_MR8_Bypass(self):
        self.MP1_MR8_pos.put(10)
        self.HRM_MP1_MR8.setGeometry(1030, 300, 111, 21)
        self.PyDMDrawingLine_14.setGeometry(900, 150, 381, 241)
        if self.HRM_MP1_MR1.x() == 60:
            self.PyDMDrawingLine_11.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_18.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )
            self.PyDMDrawingLine_27.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.DashLine
            )

    def gotoMP1_MR8_SHG_THG(self):
        self.MP1_MR8_pos.put(0)
        self.HRM_MP1_MR8.setGeometry(990, 300, 111, 21)
        self.PyDMDrawingLine_14.setGeometry(890, 240, 301, 151)
        self.PyDMDrawingLine_11.penStyle = PyQt5.QtCore.Qt.PenStyle.SolidLine
        if self.HRM_MP1_MR1.x() == 60:
            self.PyDMDrawingLine_18.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )
            self.PyDMDrawingLine_27.penStyle = (
                PyQt5.QtCore.Qt.PenStyle.SolidLine
            )

    def gotoMP3_MR2_800(self):
        print(1)

    def gotocontrol(self):
        controlfile = mirrorscreen()
        controlfile.setModal(True)
        controlfile.exec()

    def gotoexpert(self):  # (self, other)
        expertscreen = Expert()
        expertscreen.show()

    def ui_filename(self):
        return "harmonics.ui"

    def ui_filepath(self):
        return path.join(
            path.dirname(path.realpath(__file__)), self.ui_filename()
        )


class mirrorscreen(QDialog):
    def __init__(self):  # , parent=None, args=None, macros=None):
        super(
            mirrorscreen, self
        ).__init__()  # parent=parent, args=args, macros=macros)
        loadUi("littlecontrol.ui", self)
        self.tip_step = int(self.initialtip.text())
        self.tilt_step = int(self.initialtilt.text())
        self.tip_large_step = int(self.TipLargeStep.text())
        self.tilt_large_step = int(self.TiltLargeStep.text())
        self.ChangeStep.clicked.connect(self.changeCurrentSetup)
        ## four lineEdit
        ##do not have to write enterpressed to fire (dont know the connect work, maybe comments aboved solved it)

        self.small_step = 1
        # just for ramdon try, will be connected to the channel
        self.max_step_tip = int(self.TipRange.text())  # 12030
        self.max_step_tilt = int(self.TiltRange.text())  # 2550
        # large step will now be pulg in by hand

        self.tip_mm.clicked.connect(self.mm_tip)
        self.tip_m.clicked.connect(self.m_tip)
        self.tip_p.clicked.connect(self.p_tip)
        self.tip_pp.clicked.connect(self.pp_tip)
        self.tilt_mm.clicked.connect(self.mm_tilt)
        self.tilt_m.clicked.connect(self.m_tilt)
        self.tilt_p.clicked.connect(self.p_tilt)
        self.tilt_pp.clicked.connect(self.pp_tilt)

    # def ui_filename(self):
    #    return "littlecontrol.ui"

    # def ui_filepath(self):
    #    return path.join(path.dirname(path.realpath(__file__)), self.ui_filename)

    def changeCurrentSetup(self):
        # max step will remove later
        # self.max_step_tip = int(self.TipRange.text())
        # self.max_step_tilt = int(self.TiltRange.text())
        self.tip_step = int(float(self.initialtip.text()))
        self.initialtip.setText(str(self.tip_step))
        self.tilt_step = int(float(self.initialtilt.text()))
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
        return path.join(
            path.dirname(path.realpath(__file__)), self.ui_filename()
        )

    def applynumber(self):
        number = float(self.value.text())
        number = int(number)
        print(number)

        if len(str(number)) == 0:
            self.errortext.setText("No number")
        else:
            self.value.setText(str(number))
            self.errortext.setText("")


# main
app = QApplication(sys.argv)
Harmonics = Harmonic_diagram()
widget = QtWidgets.QStackedWidget()
widget.addWidget(Harmonics)
widget.setFixedHeight(600)
widget.setFixedWidth(1260)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("exiting")
