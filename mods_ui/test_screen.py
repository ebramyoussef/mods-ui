from os import path
import pydm
from PyQt5.QtWidgets import QApplication
from ophyd import EpicsSignal, EpicsSignalRO, EpicsSignalWithRBV
import sys
from PyQt5 import QtWidgets, QtGui
from image_settings_2_ui import Ui_imageSettingsForm
from ref_settings import Ui_refSettingsForm
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
        sigmax_pv_suffix="Stats2:SigmaX_RBV",
        sigmay_pv_suffix="Stats2:SigmaY_RBV",
        ellipse_overlay_pv_suffix="Over1:1:",
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
        self.sigmax_pv = self.base_pv + sigmax_pv_suffix
        self.sigmay_pv = self.base_pv + sigmay_pv_suffix
        self.sigmax_ca = self.protocal + self.sigmax_pv
        self.sigmay_ca = self.protocal + self.sigmay_pv
        self.bits = EpicsSignalRO(read_pv=self.bits_pv)
        self.maxcolor = (1 << self.bits.get()) - 1
        self.ellipse_overlay_pv_suffix = ellipse_overlay_pv_suffix

    def wPV(self, pv_suffix, yourVal):
        temppv = EpicsSignal(self.base_pv + pv_suffix)
        temppv.put(yourVal)

    def set_image_object(self, image_object):
        self.image_object = image_object


class MirrorIOC:
    def __init__(
        self,
        base_pv,
        protocol="ca://",
        stepsize_pv_suffix="STEP_COUNT",
        steptotal_pv_suffix="TOTAL_STEP_COUNT",
        stepreverse_pv_suffix="STEP_REVERSE",
        stepforward_pv_suffix="STEP_FORWARD",
        indicator_pv_suffix=":PROC",
    ):
        self.base_pv = base_pv
        self.protocol = protocol
        self.stepsize_pv = self.base_pv + stepsize_pv_suffix
        self.steptotal_pv = self.base_pv + steptotal_pv_suffix
        self.stepreverse_pv = self.base_pv + stepreverse_pv_suffix
        self.stepforward_pv = self.base_pv + stepforward_pv_suffix
        self.stepreverse_indicator_pv = (
            self.stepreverse_pv + indicator_pv_suffix
        )
        self.stepforward_indicator_pv = (
            self.stepforward_pv + indicator_pv_suffix
        )
        self.stepsize_ca = self.protocol + self.stepsize_pv
        self.steptotal_ca = self.protocol + self.steptotal_pv
        self.stepreverse_ca = self.protocol + self.stepreverse_pv
        self.stepforward_ca = self.protocol + self.stepforward_pv
        self.stepreverse_indicator_ca = (
            self.protocol + self.stepreverse_indicator_pv
        )
        self.stepforward_indicator_ca = (
            self.protocol + self.stepforward_indicator_pv
        )


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
        self.M1_tip = MirrorIOC(base_pv="LM1K4:COM_MP1_MR1_TIP1:")
        self.M1_tilt = MirrorIOC(base_pv="LM1K4:COM_MP1_MR1_TILT1:")
        self.M2_tip = MirrorIOC(base_pv="LM1K4:COM_MP1_MR4_TIP1:")
        self.M2_tilt = MirrorIOC(base_pv="LM1K4:COM_MP1_MR4_TILT1:")
        self.qss_file = "styles.qss"
        with open(self.qss_file, "r") as fh:
            self.setStyleSheet(fh.read())
        self.resize(600, 600)
        self.ui.NFRefGroupBox.setVisible(False)
        self.ui.FFRefGroupBox.setVisible(False)
        self.ui.NFShowRefPushButton.clicked.connect(
            lambda: self.ui.NFRefGroupBox.setVisible(
                not self.ui.NFRefGroupBox.isVisible()
            )
        )
        self.ui.FFShowRefPushButton.clicked.connect(
            lambda: self.ui.FFRefGroupBox.setVisible(
                not self.ui.FFRefGroupBox.isVisible()
            )
        )
        self.ui.NFImageView.imageChannel = self.NF_cam.image_ca
        self.ui.FFImageView.imageChannel = self.FF_cam.image_ca
        self.ui.NFImageView.widthChannel = self.NF_cam.width_ca
        self.ui.FFImageView.widthChannel = self.FF_cam.width_ca
        self.ui.NFCXLabel.channel = self.NF_cam.centroidx_ca
        self.ui.NFCYLabel.channel = self.NF_cam.centroidy_ca
        self.ui.FFCXLabel.channel = self.FF_cam.centroidx_ca
        self.ui.FFCYLabel.channel = self.FF_cam.centroidy_ca
        self.ui.NFSXLabel.channel = self.NF_cam.sigmax_ca
        self.ui.NFSYLabel.channel = self.NF_cam.sigmay_ca
        self.ui.FFSXLabel.channel = self.FF_cam.sigmax_ca
        self.ui.FFSYLabel.channel = self.FF_cam.sigmay_ca
        self.ui.M1VStepLineEdit.channel = self.M1_tip.stepsize_ca
        self.ui.M1VStepLabel.channel = self.M1_tip.stepsize_ca
        self.ui.M1VRevPushButton.channel = self.M1_tip.stepreverse_ca
        self.ui.M1VRevIndicator.channel = self.M1_tip.stepreverse_indicator_ca
        self.ui.M1VFwdPushButton.channel = self.M1_tip.stepforward_ca
        self.ui.M1VFwdIndicator.channel = self.M1_tip.stepforward_indicator_ca
        self.ui.M1VTotalLabel.channel = self.M1_tip.steptotal_ca
        self.ui.M1HStepLineEdit.channel = self.M1_tilt.stepsize_ca
        self.ui.M1HStepLabel.channel = self.M1_tilt.stepsize_ca
        self.ui.M1HRevPushButton.channel = self.M1_tilt.stepreverse_ca
        self.ui.M1HRevIndicator.channel = self.M1_tilt.stepreverse_indicator_ca
        self.ui.M1HFwdPushButton.channel = self.M1_tilt.stepforward_ca
        self.ui.M1HFwdIndicator.channel = self.M1_tilt.stepforward_indicator_ca
        self.ui.M1HTotalLabel.channel = self.M1_tilt.steptotal_ca
        self.ui.M2VStepLineEdit.channel = self.M2_tip.stepsize_ca
        self.ui.M2VStepLabel.channel = self.M2_tip.stepsize_ca
        self.ui.M2VRevPushButton.channel = self.M2_tip.stepreverse_ca
        self.ui.M2VRevIndicator.channel = self.M2_tip.stepreverse_indicator_ca
        self.ui.M2VFwdPushButton.channel = self.M2_tip.stepforward_ca
        self.ui.M2VFwdIndicator.channel = self.M2_tip.stepforward_indicator_ca
        self.ui.M2VTotalLabel.channel = self.M2_tip.steptotal_ca
        self.ui.M2HStepLineEdit.channel = self.M2_tilt.stepsize_ca
        self.ui.M2HStepLabel.channel = self.M2_tilt.stepsize_ca
        self.ui.M2HRevPushButton.channel = self.M2_tilt.stepreverse_ca
        self.ui.M2HRevIndicator.channel = self.M2_tilt.stepreverse_indicator_ca
        self.ui.M2HFwdPushButton.channel = self.M2_tilt.stepforward_ca
        self.ui.M2HFwdIndicator.channel = self.M2_tilt.stepforward_indicator_ca
        self.ui.M2HTotalLabel.channel = self.M2_tilt.steptotal_ca
        self.ui.NFImageView.view.invertX(False)
        self.ui.NFImageView.view.invertY(False)
        self.ui.NFImageView.readingOrder = 1
        self.ui.FFImageView.view.invertX(False)
        self.ui.FFImageView.view.invertY(False)
        self.ui.FFImageView.readingOrder = 1
        self.ui.NFRefView.view.invertX(False)
        self.ui.NFRefView.view.invertY(False)
        self.ui.NFRefView.readingOrder = 1
        self.ui.FFRefView.view.invertX(False)
        self.ui.FFRefView.view.invertY(False)
        self.ui.FFRefView.readingOrder = 1
        self.nf_orientation_idx = 0
        self.ff_orientation_idx = 0
        self.nfref_orientation_idx = 0
        self.ffref_orientation_idx = 0
        self.nfref_data = None
        self.ffref_data = None
        self.NF_cam.set_image_object(self.ui.NFImageView)
        self.FF_cam.set_image_object(self.ui.FFImageView)
        self.ui.NFUploadRefPushButton.clicked.connect(
            lambda: self.upload_reference(
                self.ui.NFRefView, classification="NF"
            )
        )
        self.ui.FFUploadRefPushButton.clicked.connect(
            lambda: self.upload_reference(
                self.ui.FFRefView, classification="FF"
            )
        )
        self.ui.NFImageSettingsPushButton.clicked.connect(
            lambda: self.load_image_settings(self.NF_cam)
        )
        self.ui.FFImageSettingsPushButton.clicked.connect(
            lambda: self.load_image_settings(self.FF_cam)
        )
        self.ui.NFRefSettingsPushButton.clicked.connect(
            lambda: self.load_ref_settings(self.ui.NFRefView, "NF")
        )
        self.ui.FFRefSettingsPushButton.clicked.connect(
            lambda: self.load_ref_settings(self.ui.FFRefView, "FF")
        )
        self.ui.NFSavePushButton.clicked.connect(
            lambda: self.save_image(self.NF_cam.image_object)
        )
        self.ui.FFSavePushButton.clicked.connect(
            lambda: self.save_image(self.FF_cam.image_object)
        )
        self.ui.NFEllipsePushButton.clicked.connect(
            lambda: self.draw_ellipse(self.NF_cam)
        )
        self.show()

    def ui_filename(self):
        return "untitled.ui"

    def ui_filepath(self):
        return path.join(
            path.dirname(path.realpath(__file__)), self.ui_filename()
        )

    def draw_ellipse(self, cam_object: CamIOC):
        cam_object.wPV(cam_object.ellipse_overlay_pv_suffix + "Use", 1)
        cam_object.wPV(cam_object.ellipse_overlay_pv_suffix + "Shape", 2)
        cam_object.wPV(cam_object.ellipse_overlay_pv_suffix + "DrawMode", 1)
        cam_object.wPV(cam_object.ellipse_overlay_pv_suffix + "WidthX", 3)
        cam_object.wPV(cam_object.ellipse_overlay_pv_suffix + "WidthY", 3)
        cam_object.wPV(
            cam_object.ellipse_overlay_pv_suffix + "SizeXLink.DOL",
            cam_object.sigmax_pv + " CP",
        )
        cam_object.wPV(
            cam_object.ellipse_overlay_pv_suffix + "SizeYLink.DOL",
            cam_object.sigmay_pv + " CP",
        )
        cam_object.wPV(
            cam_object.ellipse_overlay_pv_suffix + "CenterXLink.DOL",
            cam_object.centroidx_pv + " CP",
        )
        cam_object.wPV(
            cam_object.ellipse_overlay_pv_suffix + "CenterYLink.DOL",
            cam_object.centroidy_pv + " CP",
        )

    def upload_reference(self, image_object, classification):
        try:
            fileName = QtWidgets.QFileDialog.getOpenFileName(
                parent=self,
                caption="Load Reference...",
                filter="Numpy Arrays (*.npy)",
            )[0]
            if fileName == "":
                raise Exception("No File Specified")
            if fileName.lower().endswith(".npy"):
                reference_data = np.load(fileName)
            else:
                raise Exception("Unsupported file format")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "File Save Failed", str(e))
        image_object.setImage(reference_data)
        if classification == "NF":
            self.nfref_data = reference_data
        elif classification == "FF":
            self.ffref_data = reference_data

    def autoset_colormap(self, image_object, type):
        min_max = image_object.quickMinMax(image_object.getImageItem().image)
        if type == "ref":
            image_object.setLevels(min=min_max[0][0], max=min_max[0][1])
        elif type == "img":
            image_object.colorMapMin = min_max[0][0]
            image_object.colorMapMax = min_max[0][1]

    def save_image(self, image_object):
        image_data = image_object.getImageItem().image
        try:
            fileName = QtWidgets.QFileDialog.getSaveFileName(
                parent=self,
                caption="Save Image...",
                filter="Numpy Arrays (*.npy)",
            )[0]
            if fileName == "":
                raise Exception("No File Name Specified")
            if fileName.lower().endswith(".npy"):
                np.save(fileName, image_data)
                QtWidgets.QMessageBox.information(
                    self,
                    "File Save Succeeded",
                    "Image has been saved as a numpy file: %s" % (fileName),
                )
            else:
                raise Exception("Unsupported file format")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "File Save Failed", str(e))

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
                self.autoset_colormap(cam_object.image_object, type="img")
            else:
                cam_object.image_object.colorMapMin = self.color_map_min_val
                cam_object.image_object.colorMapMax = self.color_map_max_val
            cam_object.image_object.normalizeData = self.normalize_val
            roi_pos = pg.Point(
                self.ROI_position_x_val, self.ROI_position_y_val
            )
            roi_size = pg.Point(self.ROI_range_x_val, self.ROI_range_y_val)
            cam_object.image_object.roi = pg.ROI(pos=roi_pos, size=roi_size)
            self.apply_orientation(
                cam_object.image_object,
                orientation_idx,
                type="img",
                classification=cam_object.classification,
            )
            screen.close()

    def load_ref_settings(self, image_object, classification):
        screen = refSettingsScreen()
        screen.ui.minLineEdit.setText(
            str(image_object.imageItem.getLevels()[0])
        )
        screen.ui.maxLineEdit.setText(
            str(image_object.imageItem.getLevels()[1])
        )
        if classification == "NF":
            screen.ui.orientationComboBox.setCurrentIndex(
                self.nfref_orientation_idx
            )
        elif classification == "FF":
            screen.ui.orientationComboBox.setCurrentIndex(
                self.ffref_orientation_idx
            )
        screen.show()
        screen.ui.buttonBox.accepted.connect(
            lambda: self.apply_ref_settings(
                screen, image_object, classification
            )
        )
        screen.ui.buttonBox.rejected.connect(screen.close)

    def apply_ref_settings(self, screen, image_object, classification):
        try:
            self.color_map_min_val = float(screen.ui.minLineEdit.text())
            self.color_map_max_val = float(screen.ui.maxLineEdit.text())
            self.normalize_val = screen.ui.normalizeCheckBox.isChecked()
            self.autoset_val = screen.ui.autosetCheckBox.isChecked()
            orientation_idx = screen.ui.orientationComboBox.currentIndex()
            if classification == "NF":
                self.nfref_orientation_idx = orientation_idx
            elif classification == "FF":
                self.ffref_orientation_idx = orientation_idx
        except ValueError:
            screen.no_errors = False
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("ValueError: Invalid input values.")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.buttonClicked.connect(self.show)
            msg.exec_()
        if screen.no_errors is True:
            self.apply_orientation(
                image_object,
                orientation_idx,
                type="ref",
                classification=classification,
            )
            if self.autoset_val:
                self.autoset_colormap(image_object, type="ref")
            else:
                image_object.setLevels(
                    min=self.color_map_min_val, max=self.color_map_max_val
                )
            if self.normalize_val is True:
                norm_img = image_object.normalize(
                    image_object.getImageItem().image
                )
                image_object.setImage(norm_img)
            image_object.redrawImage()
            screen.close()

    def apply_orientation(
        self, image_object, orientation_idx, type, classification
    ):
        if type == "img":
            if orientation_idx == 0:
                image_object.readingOrder = 1
                image_object.view.invertX(False)
                image_object.view.invertY(False)
            elif orientation_idx == 1:
                image_object.readingOrder = 0
                image_object.view.invertX(False)
                image_object.view.invertY(True)
            elif orientation_idx == 2:
                image_object.readingOrder = 1
                image_object.view.invertX(True)
                image_object.view.invertY(True)
            elif orientation_idx == 3:
                image_object.readingOrder = 0
                image_object.view.invertX(True)
                image_object.view.invertY(False)
            elif orientation_idx == 4:
                image_object.readingOrder = 1
                image_object.view.invertX(True)
                image_object.view.invertY(False)
            elif orientation_idx == 5:
                image_object.readingOrder = 1
                image_object.view.invertX(False)
                image_object.view.invertY(True)
        elif type == "ref":
            if classification == "NF":
                original_image = self.nfref_data
            elif classification == "FF":
                original_image = self.ffref_data
            if orientation_idx == 0:
                image_object.setImage(original_image)
                image_object.view.invertX(False)
                image_object.view.invertY(False)
            elif orientation_idx == 1:
                tr = QtGui.QTransform()
                tr.rotate(270)
                image_object.setImage(original_image, transform=tr)
                image_object.view.invertX(False)
                image_object.view.invertY(False)
            elif orientation_idx == 2:
                tr = QtGui.QTransform()
                tr.rotate(180)
                image_object.setImage(original_image, transform=tr)
                image_object.view.invertX(False)
                image_object.view.invertY(False)
            elif orientation_idx == 3:
                tr = QtGui.QTransform()
                tr.rotate(90)
                image_object.setImage(original_image, transform=tr)
                image_object.view.invertX(False)
                image_object.view.invertY(False)
            elif orientation_idx == 4:
                image_object.setImage(original_image)
                image_object.view.invertX(True)
                image_object.view.invertY(False)
            elif orientation_idx == 5:
                image_object.setImage(original_image)
                image_object.view.invertX(False)
                image_object.view.invertY(True)


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


class refSettingsScreen(QtWidgets.QWidget):
    def __init__(self):
        super(refSettingsScreen, self).__init__()
        self.ui = Ui_refSettingsForm()
        self.ui.setupUi(self)
        self.no_errors = True


if __name__ == "__main__":
    qapp = QApplication.instance()
    if not qapp:
        qapp = QApplication(sys.argv)
    screen = testScreen()
    qapp.exec_()
