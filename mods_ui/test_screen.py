from os import path
from pydm import Display
from PyQt5.QtWidgets import QApplication
import sys
from PyQt5 import QtWidgets
from .image_settings import Ui_imageSettingsForm
import pyqtgraph as pg


class testScreen(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(testScreen, self).__init__(
            parent=parent, args=args, macros=macros
        )
        self.ui.NFImageSettingsPushButton.clicked.connect(
            lambda: self.load_image_settings()
        )
        self.show()

    def ui_filename(self):
        return "untitled.ui"

    def ui_filepath(self):
        return path.join(
            path.dirname(path.realpath(__file__)), self.ui_filename()
        )

    def load_image_settings(self, image_object):
        screen = imageSettingsScreen(image_object)
        if screen.no_errors is True:
            image_object.colorMapMin = screen.color_map_min_val
            image_object.colorMapMax = screen.color_map_max_val
            image_object.normalizeData = screen.normalize_val


class imageSettingsScreen(QtWidgets.QWidget):
    def __init__(self, image_object):
        super(imageSettingsScreen, self).__init__()
        self.ui = Ui_imageSettingsForm()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.close)
        self.no_errors = True
        self.show()

    def ok(self):
        try:
            self.color_map_min_val = float(self.ui.colorMapMinLineEdit.text())
            self.color_map_max_val = float(self.ui.colorMapMaxLineEdit.text())
            self.normalize_val = self.ui.normalizeCheckBox.isChecked()
            self.ROI_center_x_val = float(self.ui.ROICenterXLineEdit.text())
            self.ROI_range_x_val = float(self.ui.ROIRangeXLineEdit.text())
            self.ROI_center_y_val = float(self.ui.ROICenterYLineEdit.text())
            self.ROI_range_y_val = float(self.ui.ROIRangeYLineEdit.text())
            self.orientation_idx = int(
                self.ui.orientationComboBox.currentIndex()
            )
            self.redraw_rate_val = float(self.ui.redrawRateLineEdit.text())
        except ValueError:
            self.no_errors = False
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("ValueError: Invalid input values.")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.buttonClicked.connect(self.show)
            msg.exec_()

        self.close()

    def cancel(self):
        self.no_errors = False
        self.close()

    def ui_filename(self):
        return "image_settings.ui"

    def ui_filepath(self):
        return path.join(
            path.dirname(path.realpath(__file__)), self.ui_filename()
        )


if __name__ == "__main__":
    qapp = QApplication.instance()
    if not qapp:
        qapp = QApplication(sys.argv)
    screen = testScreen()
    qapp.exec_()
