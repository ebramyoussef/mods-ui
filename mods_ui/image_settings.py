# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'image_settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_imageSettingsForm(object):
    def setupUi(self, imageSettingsForm):
        imageSettingsForm.setObjectName("imageSettingsForm")
        imageSettingsForm.resize(332, 268)
        self.verticalLayout = QtWidgets.QVBoxLayout(imageSettingsForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.colorMapMinLabel = QtWidgets.QLabel(imageSettingsForm)
        self.colorMapMinLabel.setObjectName("colorMapMinLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.colorMapMinLabel)
        self.colorMapMinLineEdit = QtWidgets.QLineEdit(imageSettingsForm)
        self.colorMapMinLineEdit.setObjectName("colorMapMinLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.colorMapMinLineEdit)
        self.colorMapMaxLabel = QtWidgets.QLabel(imageSettingsForm)
        self.colorMapMaxLabel.setObjectName("colorMapMaxLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.colorMapMaxLabel)
        self.colorMapMaxLineEdit = QtWidgets.QLineEdit(imageSettingsForm)
        self.colorMapMaxLineEdit.setObjectName("colorMapMaxLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.colorMapMaxLineEdit)
        self.normalizeLabel = QtWidgets.QLabel(imageSettingsForm)
        self.normalizeLabel.setObjectName("normalizeLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.normalizeLabel)
        self.normalizeCheckBox = QtWidgets.QCheckBox(imageSettingsForm)
        self.normalizeCheckBox.setObjectName("normalizeCheckBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.normalizeCheckBox)
        self.ROICenterXLabel = QtWidgets.QLabel(imageSettingsForm)
        self.ROICenterXLabel.setObjectName("ROICenterXLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.ROICenterXLabel)
        self.ROICenterXLineEdit = QtWidgets.QLineEdit(imageSettingsForm)
        self.ROICenterXLineEdit.setObjectName("ROICenterXLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.ROICenterXLineEdit)
        self.ROIRangeXLabel = QtWidgets.QLabel(imageSettingsForm)
        self.ROIRangeXLabel.setObjectName("ROIRangeXLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.ROIRangeXLabel)
        self.ROIRangeXLineEdit = QtWidgets.QLineEdit(imageSettingsForm)
        self.ROIRangeXLineEdit.setObjectName("ROIRangeXLineEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.ROIRangeXLineEdit)
        self.ROICenterYLabel = QtWidgets.QLabel(imageSettingsForm)
        self.ROICenterYLabel.setObjectName("ROICenterYLabel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.ROICenterYLabel)
        self.ROICenterYLineEdit = QtWidgets.QLineEdit(imageSettingsForm)
        self.ROICenterYLineEdit.setObjectName("ROICenterYLineEdit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.ROICenterYLineEdit)
        self.ROIRangeYLabel = QtWidgets.QLabel(imageSettingsForm)
        self.ROIRangeYLabel.setObjectName("ROIRangeYLabel")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.ROIRangeYLabel)
        self.ROIRangeYLineEdit = QtWidgets.QLineEdit(imageSettingsForm)
        self.ROIRangeYLineEdit.setObjectName("ROIRangeYLineEdit")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.ROIRangeYLineEdit)
        self.orientationLabel = QtWidgets.QLabel(imageSettingsForm)
        self.orientationLabel.setObjectName("orientationLabel")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.orientationLabel)
        self.orientationComboBox = QtWidgets.QComboBox(imageSettingsForm)
        self.orientationComboBox.setObjectName("orientationComboBox")
        self.orientationComboBox.addItem("")
        self.orientationComboBox.addItem("")
        self.orientationComboBox.addItem("")
        self.orientationComboBox.addItem("")
        self.orientationComboBox.addItem("")
        self.orientationComboBox.addItem("")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.orientationComboBox)
        self.redrawRateLabel = QtWidgets.QLabel(imageSettingsForm)
        self.redrawRateLabel.setObjectName("redrawRateLabel")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.redrawRateLabel)
        self.redrawRateLineEdit = QtWidgets.QLineEdit(imageSettingsForm)
        self.redrawRateLineEdit.setObjectName("redrawRateLineEdit")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.redrawRateLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(imageSettingsForm)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(imageSettingsForm)
        QtCore.QMetaObject.connectSlotsByName(imageSettingsForm)

    def retranslateUi(self, imageSettingsForm):
        _translate = QtCore.QCoreApplication.translate
        imageSettingsForm.setWindowTitle(_translate("imageSettingsForm", "Image settings"))
        self.colorMapMinLabel.setText(_translate("imageSettingsForm", "Color map min"))
        self.colorMapMaxLabel.setText(_translate("imageSettingsForm", "Color map max"))
        self.normalizeLabel.setText(_translate("imageSettingsForm", "Normalize"))
        self.ROICenterXLabel.setText(_translate("imageSettingsForm", "ROI center x"))
        self.ROIRangeXLabel.setText(_translate("imageSettingsForm", "ROI range x"))
        self.ROICenterYLabel.setText(_translate("imageSettingsForm", "ROI center y"))
        self.ROIRangeYLabel.setText(_translate("imageSettingsForm", "ROI range y"))
        self.orientationLabel.setText(_translate("imageSettingsForm", "Orientation"))
        self.orientationComboBox.setItemText(0, _translate("imageSettingsForm", "Unchanged"))
        self.orientationComboBox.setItemText(1, _translate("imageSettingsForm", "Rotate 90"))
        self.orientationComboBox.setItemText(2, _translate("imageSettingsForm", "Rotate 180"))
        self.orientationComboBox.setItemText(3, _translate("imageSettingsForm", "Rotate 270"))
        self.orientationComboBox.setItemText(4, _translate("imageSettingsForm", "Flip H"))
        self.orientationComboBox.setItemText(5, _translate("imageSettingsForm", "Flip V"))
        self.redrawRateLabel.setText(_translate("imageSettingsForm", "Redraw rate"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    imageSettingsForm = QtWidgets.QWidget()
    ui = Ui_imageSettingsForm()
    ui.setupUi(imageSettingsForm)
    imageSettingsForm.show()
    sys.exit(app.exec_())