from os import path
from pydm import Display
from PyQt5.QtWidgets import QApplication
from ophyd import EpicsSignal, EpicsSignalRO, EpicsSignalWithRBV
import sys
from PyQt5 import QtWidgets
from image_settings_2 import Ui_imageSettingsForm
import pyqtgraph as pg
import numpy as np
from dataclasses import dataclass


@dataclass
class CamIOC:
    base_pv: str = "LM1K4:COM_DP1_TF1_NF1:"
    classification: str = "NF"
    protocal: str = "ca://"
    image_pv: str = "IMAGE1:ArrayData"
    width_pv: str = "IMAGE1:ArraySize0_RBV"
    bits_pv: str = "BIT_DEPTH"
    image_ca: str = protocal + base_pv + image_pv
    width_ca: str = protocal + base_pv + width_pv


class testScreen(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(testScreen, self).__init__(
            parent=parent, args=args, macros=macros
        )
        self.NF_cam = CamIOC(
            base_pv="LM1K4:COM_DP1_TF1_NF1:", classification="NF"
        )
        self.FF_cam = CamIOC(
            base_pv="LM1K4:COM_DP1_TF1_FF1:", classification="FF"
        )
        self.ui.NFImageView.imageChannel = self.NF_cam.image_ca
        self.ui.NFImageView.widthChannel = self.NF_cam.width_ca
        self.ui.FFImageView.imageChannel = self.FF_cam.image_ca
        self.ui.FFImageView.widthChannel = self.FF_cam.width_ca
        self.ui.NFImageSettingsPushButton.clicked.connect(
            lambda: self.load_image_settings(self.ui.NFImageView)
        )
        self.ui.FFImageSettingsPushButton.clicked.connect(
            lambda: self.load_image_settings(self.ui.FFImageView)
        )
        self.ui.NFSavePushButton.clicked.connect(
            lambda: self.save_image(self.ui.NFImageView)
        )
        self.ui.FFSavePushButton.clicked.connect(
            lambda: self.save_image(self.ui.FFImageView)
        )
        self.nf_bits = EpicsSignalRO("LM1K4:COM_DP1_TF1_NF1:BIT_DEPTH")
        self.nf_maxcolor = (1 << self.nf_bits.get()) - 1
        self.show()

    def ui_filename(self):
        return "untitled.ui"

    def ui_filepath(self):
        return path.join(
            path.dirname(path.realpath(__file__)), self.ui_filename()
        )

    def autoset_colormap(self, image_object):
        min_max = image_object.quickMinMax(image_object.getImageItem().image)
        image_object.colorMapMin = min_max[0][0]
        image_object.colorMapMax = min_max[0][1]

    def save_image(self, image_object):
        image_data = image_object.getImageItem().image
        np.save("saved_image.npy", image_data)

    def load_image_settings(self, image_object):
        screen = imageSettingsScreen()
        screen.ui.minLineEdit.setText(str(image_object.colorMapMin))
        screen.ui.maxLineEdit.setText(str(image_object.colorMapMax))
        screen.ui.XLineEdit.setText(str(image_object.roi.pos().x()))
        screen.ui.YLineEdit.setText(str(image_object.roi.pos().y()))
        screen.ui.WLineEdit.setText(str(image_object.roi.size().x()))
        screen.ui.HLineEdit.setText(str(image_object.roi.size().y()))
        screen.ui.normalizeCheckBox.setChecked(image_object.normalizeData)
        screen.ui.minSlider.setMaximum()
        screen.show()
        screen.ui.buttonBox.accepted.connect(
            lambda: self.apply_image_settings(screen, image_object)
        )
        screen.ui.buttonBox.rejected.connect(screen.close)

    def apply_image_settings(self, screen, image_object):
        try:
            self.color_map_min_val = float(screen.ui.minLineEdit.text())
            self.color_map_max_val = float(screen.ui.maxLineEdit.text())
            self.normalize_val = screen.ui.normalizeCheckBox.isChecked()
            self.autoset_val = screen.ui.autosetCheckBox.isChecked()
            self.ROI_position_x_val = float(screen.ui.XLineEdit.text())
            self.ROI_range_x_val = float(screen.ui.WLineEdit.text())
            self.ROI_position_y_val = float(screen.ui.YLineEdit.text())
            self.ROI_range_y_val = float(screen.ui.HLineEdit.text())
            # self.orientation_idx = int(
            #     screen.ui.orientationComboBox.currentIndex()
            # )
        except ValueError:
            screen.no_errors = False
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("ValueError: Invalid input values.")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.buttonClicked.connect(self.show)
            msg.exec_()
        if screen.no_errors is True:
            if self.autoset_val:
                self.autoset_colormap(image_object)
            else:
                image_object.colorMapMin = self.color_map_min_val
                image_object.colorMapMax = self.color_map_max_val
            image_object.normalizeData = self.normalize_val
            roi_pos = pg.Point(
                self.ROI_position_x_val, self.ROI_position_y_val
            )
            roi_size = pg.Point(self.ROI_range_x_val, self.ROI_range_y_val)
            image_object.roi = pg.ROI(pos=roi_pos, size=roi_size)
            screen.close()


class imageSettingsScreen(QtWidgets.QWidget):
    def __init__(self):
        super(imageSettingsScreen, self).__init__()
        self.ui = Ui_imageSettingsForm()
        self.ui.setupUi(self)
        self.no_errors = True


if __name__ == "__main__":
    qapp = QApplication.instance()
    if not qapp:
        qapp = QApplication(sys.argv)
    screen = testScreen()
    qapp.exec_()
