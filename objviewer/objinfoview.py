import argparse
import math
import numpy as np
import os
import sys

from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtQuick import QQuickView

from . objview import ObjView


def _cameraParamDesc(camera):
    with np.printoptions(precision=2, suppress=True, floatmode='fixed'):
        text = 'Yaw: {:.2f}\nPitch: {:.2f}\nPosition: {}'.format(
            math.degrees(camera.yaw),
            math.degrees(camera.pitch),
            camera.position
        )
    return text


class ObjInfoView(ObjView):

    cameraParamDescUpdated = pyqtSignal(str)

    def __init__(
            self,
            parent=None):
        super(ObjInfoView, self).__init__(parent=parent)
        self._cameraParamDesc = '-'
        self._updateCameraParamDesc()

        self.keyPressed.connect(self.onCameraUpdate)
        self.mouseEvent.connect(self.onCameraUpdate)


    @pyqtProperty(str, notify=cameraParamDescUpdated)
    def cameraParamDesc(self):
        return self._cameraParamDesc

    @pyqtSlot()
    def resetCamera(self):
        super(ObjInfoView, self).resetCamera()
        self.onCameraUpdate()

    def onCameraUpdate(self):
        self._updateCameraParamDesc()
        self.cameraParamDescUpdated.emit(self._cameraParamDesc)

    def _updateCameraParamDesc(self):
        self._cameraParamDesc = _cameraParamDesc(self._camera)


def register_qml():
    qmlRegisterType(ObjInfoView, 'ObjViewer', 1, 0, 'ObjInfoView')


def run_qml(qmlpath):
    app = QGuiApplication(sys.argv)
    register_qml()

    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.setSource(QUrl(qmlpath))
    view.show()

    sys.exit(app.exec_())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        default=False,
        help='Print debug strings'
    )
    args = parser.parse_args()
    verbose = args.verbose

    run_qml('qml/objviewer.qml')


if __name__ == '__main__':
    main()
