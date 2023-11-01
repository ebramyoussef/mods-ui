from os import path
from pydm import Display
from PyQt5.QtWidgets import QApplication
import sys
from PyQt5 import QtWidgets
from image_settings import Ui_imageSettingsForm
import pyqtgraph as pg


class testScreen(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(testScreen, self).__init__(
            parent=parent, args=args, macros=macros
        )
        self.ui.NFImageSettingsPushButton.clicked.connect(
            lambda: self.load_image_settings(self.ui.NFImageView)
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
        screen.show()
        screen.ui.buttonBox.accepted.connect(
            lambda: self.apply_image_settings(screen, image_object)
        )
        screen.ui.buttonBox.rejected.connect(screen.close)

    def apply_image_settings(self, screen, image_object):
        try:
            self.color_map_min_val = float(
                screen.ui.colorMapMinLineEdit.text()
            )
            self.color_map_max_val = float(
                screen.ui.colorMapMaxLineEdit.text()
            )
            self.normalize_val = screen.ui.normalizeCheckBox.isChecked()
            self.ROI_center_x_val = float(screen.ui.ROICenterXLineEdit.text())
            self.ROI_range_x_val = float(screen.ui.ROIRangeXLineEdit.text())
            self.ROI_center_y_val = float(screen.ui.ROICenterYLineEdit.text())
            self.ROI_range_y_val = float(screen.ui.ROIRangeYLineEdit.text())
            self.orientation_idx = int(
                screen.ui.orientationComboBox.currentIndex()
            )
            self.redraw_rate_val = float(screen.ui.redrawRateLineEdit.text())
        except ValueError:
            self.no_errors = False
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("ValueError: Invalid input values.")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.buttonClicked.connect(self.show)
            msg.exec_()
        if screen.no_errors is True:
            image_object.colorMapMin = self.color_map_min_val
            image_object.colorMapMax = self.color_map_max_val
            image_object.normalizeData = self.normalize_val
            screen.close()


class imageSettingsScreen(QtWidgets.QWidget):
    def __init__(self, image_object):
        super(imageSettingsScreen, self).__init__()
        self.ui = Ui_imageSettingsForm()
        self.ui.setupUi(self)

        self.ui.colorMapMinLineEdit.setText(image_object.colorMapMin)
        self.ui.colorMapMaxLineEdit.setText(image_object.colorMapMax)
        self.no_errors = True

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
