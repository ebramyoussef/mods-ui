from os import path
from pydm import Display
from PyQt5.QtWidgets import QApplication
import sys


class testScreen(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(testScreen, self).__init__(
            parent=parent, args=args, macros=macros
        )
        self.ui.NFImageView.normalizeData = True
        # self.ui.NFImageView.autoRange()
        self.ui.NFImageView.normalizeData = True
        # self.ui.FFImageView.autoRange()
        # self.ui.FFImageView.redrawImage()
        # self.ui.NFImageView.redrawImage()
        self.show()

    def ui_filename(self):
        return "untitled.ui"

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
