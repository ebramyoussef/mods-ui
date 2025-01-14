from os import path
import pydm
from PyQt5.QtWidgets import QApplication
from ophyd import EpicsSignal, EpicsSignalRO, EpicsSignalWithRBV
import sys
from PyQt5 import QtWidgets
from image_settings_2_ui import Ui_imageSettingsForm
import pyqtgraph as pg
import numpy as np


class CamIOC:
    def __init__(
        self,
        base_pv,
        classification,
        protocol="ca://",
        image_pv_suffix="IMAGE1:ArrayData",
        width_pv_suffix="IMAGE1:ArraySize0_RBV",
        bits_pv_suffix="BitsPerPixel_RBV",
        centroidx_pv_suffix="Stats2:CentroidX_RBV",
        centroidy_pv_suffix="Stats2:CentroidY_RBV",
    ):
        self.base_pv = base_pv
        self.classification = classification
        self.protocal = protocol
        self.image_pv = self.base_pv + image_pv_suffix
        self.width_pv = self.base_pv + width_pv_suffix
        self.bits_pv = self.base_pv + bits_pv_suffix
        self.image_ca = self.protocal + self.image_pv
        self.width_ca = self.protocal + self.width_pv
        self.centroidx_pv = self.base_pv + centroidx_pv_suffix
        self.centroidy_pv = self.base_pv + centroidy_pv_suffix
        self.centroidx_ca = self.protocal + self.centroidx_pv
        self.centroidy_ca = self.protocal + self.centroidy_pv
        self.bits = EpicsSignalRO(read_pv=self.bits_pv)
        self.maxcolor = (1 << self.bits.get()) - 1

    def set_image_object(self, image_object):
        self.image_object = image_object


class testScreen(pydm.Display):
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
        self.qss_file = "styles.qss"
        with open(self.qss_file, "r") as fh:
            self.setStyleSheet(fh.read())
        self.resize(1200, 900)
        self.ui.NFImageView.imageChannel = self.NF_cam.image_ca
        self.ui.FFImageView.imageChannel = self.FF_cam.image_ca
        self.ui.NFImageView.widthChannel = self.NF_cam.width_ca
        self.ui.FFImageView.widthChannel = self.FF_cam.width_ca
        self.ui.NFCXLabel.channel = self.NF_cam.centroidx_ca
        self.ui.NFCYLabel.channel = self.NF_cam.centroidy_ca
        self.ui.FFCXLabel.channel = self.FF_cam.centroidx_ca
        self.ui.FFCYLabel.channel = self.FF_cam.centroidy_ca
        self.ui.NFImageView.view.invertX(False)
        self.ui.NFImageView.view.invertY(False)
        self.ui.NFImageView.readingOrder = 1
        self.ui.FFImageView.view.invertX(False)
        self.ui.FFImageView.view.invertY(False)
        self.ui.NFImageView.readingOrder = 1
        self.nf_orientation_idx = 0
        self.ff_orientation_idx = 0
        self.NF_cam.set_image_object(self.ui.NFImageView)
        self.FF_cam.set_image_object(self.ui.FFImageView)
        self.ui.NFImageSettingsPushButton.clicked.connect(
            lambda: self.load_image_settings(self.NF_cam)
        )
        self.ui.FFImageSettingsPushButton.clicked.connect(
            lambda: self.load_image_settings(self.FF_cam)
        )
        self.ui.NFSavePushButton.clicked.connect(
            lambda: self.save_image(self.NF_cam.image_object)
        )
        self.ui.FFSavePushButton.clicked.connect(
            lambda: self.save_image(self.FF_cam.image_object)
        )
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

    def load_image_settings(self, cam_object):
        screen = imageSettingsScreen(cam_object)
        screen.ui.minLineEdit.setText(str(cam_object.image_object.colorMapMin))
        screen.ui.maxLineEdit.setText(str(cam_object.image_object.colorMapMax))
        screen.ui.XLineEdit.setText(str(cam_object.image_object.roi.pos().x()))
        screen.ui.YLineEdit.setText(str(cam_object.image_object.roi.pos().y()))
        screen.ui.WLineEdit.setText(
            str(cam_object.image_object.roi.size().x())
        )
        screen.ui.HLineEdit.setText(
            str(cam_object.image_object.roi.size().y())
        )
        screen.ui.normalizeCheckBox.setChecked(
            cam_object.image_object.normalizeData
        )
        if cam_object.classification == "NF":
            screen.ui.orientationComboBox.setCurrentIndex(
                self.nf_orientation_idx
            )
        elif cam_object.classification == "FF":
            screen.ui.orientationComboBox.setCurrentIndex(
                self.ff_orientation_idx
            )
        screen.ui.minSlider.setMaximum(cam_object.maxcolor)
        screen.ui.minSlider.setValue(int(cam_object.image_object.colorMapMin))
        screen.ui.minSlider.setTickInterval(
            int((1 << cam_object.bits.get()) / 4)
        )
        screen.ui.maxSlider.setMaximum(cam_object.maxcolor)
        screen.ui.maxSlider.setTickInterval(
            int((1 << cam_object.bits.get()) / 4)
        )
        screen.ui.maxSlider.setValue(int(cam_object.image_object.colorMapMax))
        screen.show()
        screen.ui.buttonBox.accepted.connect(
            lambda: self.apply_image_settings(screen, cam_object)
        )
        screen.ui.buttonBox.rejected.connect(screen.close)

    def apply_image_settings(self, screen, cam_object):
        try:
            self.color_map_min_val = float(screen.ui.minLineEdit.text())
            self.color_map_max_val = float(screen.ui.maxLineEdit.text())
            self.normalize_val = screen.ui.normalizeCheckBox.isChecked()
            self.autoset_val = screen.ui.autosetCheckBox.isChecked()
            self.ROI_position_x_val = float(screen.ui.XLineEdit.text())
            self.ROI_range_x_val = float(screen.ui.WLineEdit.text())
            self.ROI_position_y_val = float(screen.ui.YLineEdit.text())
            self.ROI_range_y_val = float(screen.ui.HLineEdit.text())
            orientation_idx = screen.ui.orientationComboBox.currentIndex()
            if cam_object.classification == "NF":
                self.nf_orientation_idx = orientation_idx
            elif cam_object.classification == "FF":
                self.ff_orientation_idx = orientation_idx
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
                self.autoset_colormap(cam_object.image_object)
            else:
                cam_object.image_object.colorMapMin = self.color_map_min_val
                cam_object.image_object.colorMapMax = self.color_map_max_val
            cam_object.image_object.normalizeData = self.normalize_val
            roi_pos = pg.Point(
                self.ROI_position_x_val, self.ROI_position_y_val
            )
            roi_size = pg.Point(self.ROI_range_x_val, self.ROI_range_y_val)
            cam_object.image_object.roi = pg.ROI(pos=roi_pos, size=roi_size)
            self.apply_orientation(cam_object, orientation_idx)
            screen.close()

    def apply_orientation(self, cam_object, orientation_idx):
        if orientation_idx == 0:
            cam_object.image_object.readingOrder = 1
            cam_object.image_object.view.invertX(False)
            cam_object.image_object.view.invertY(False)
        elif orientation_idx == 1:
            cam_object.image_object.readingOrder = 0
            cam_object.image_object.view.invertX(False)
            cam_object.image_object.view.invertY(True)
        elif orientation_idx == 2:
            cam_object.image_object.readingOrder = 1
            cam_object.image_object.view.invertX(True)
            cam_object.image_object.view.invertY(True)
        elif orientation_idx == 3:
            cam_object.image_object.readingOrder = 0
            cam_object.image_object.view.invertX(False)
            cam_object.image_object.view.invertY(False)
        elif orientation_idx == 4:
            cam_object.image_object.readingOrder = 1
            cam_object.image_object.view.invertX(True)
            cam_object.image_object.view.invertY(False)
        elif orientation_idx == 5:
            cam_object.image_object.readingOrder = 1
            cam_object.image_object.view.invertX(False)
            cam_object.image_object.view.invertY(True)


class imageSettingsScreen(QtWidgets.QWidget):
    def __init__(self, cam_object):
        super(imageSettingsScreen, self).__init__()
        self.ui = Ui_imageSettingsForm()
        self.ui.setupUi(self)
        self.no_errors = True
        self.ui.minSlider.valueChanged.connect(self.onMinSliderChanged)
        self.ui.maxSlider.valueChanged.connect(self.onMaxSliderChanged)
        self.ui.minLineEdit.returnPressed.connect(self.onMinLineEditReturned)
        self.ui.maxLineEdit.returnPressed.connect(self.onMaxLineEditReturned)
        self.cam_object = cam_object

    def onMinSliderChanged(self, value):
        self.ui.minLineEdit.setText(str(value))
        if value > self.ui.maxSlider.value():
            self.ui.maxSlider.setValue(value)

    def onMaxSliderChanged(self, value):
        self.ui.maxLineEdit.setText(str(value))
        if value < self.ui.minSlider.value():
            self.ui.minSlider.setValue(value)

    def onMinLineEditReturned(self):
        try:
            value = int(self.ui.minLineEdit.text())
        except Exception:
            value = 0
        if value < 0:
            value = 0
        if value > self.cam_object.maxcolor:
            value = self.cam_object.maxcolor
        self.ui.minSlider.setValue(value)

    def onMaxLineEditReturned(self):
        try:
            value = int(self.ui.maxLineEdit.text())
        except Exception:
            value = 0
        if value < 0:
            value = 0
        if value > self.cam_object.maxcolor:
            value = self.cam_object.maxcolor
        self.ui.maxSlider.setValue(value)


if __name__ == "__main__":
    qapp = QApplication.instance()
    if not qapp:
        qapp = QApplication(sys.argv)
    screen = testScreen()
    qapp.exec_()
