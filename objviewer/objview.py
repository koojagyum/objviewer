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

from pyglfw.camera import set_camera_params
from pyglfw.instance import ModelInstance
from pyglfw.instance import MonoInstanceRenderer
from pyglfw.model import ColorModel
from pyglfw.mousecamera import MouseCamera
from pyqt5glfw.qquickglitem import QQuickGLItem

from .loader import load_model


default_camera_params = {
    'yaw': math.radians(270.0),
    'pitch': math.radians(0.0),
    'position': np.array([0.0, 1.5, 9.0], dtype=np.float32),
    'SPEED': 0.3
}


class ObjView(QQuickGLItem):

    objModelUpdated = pyqtSignal(ColorModel)

    def __init__(
            self,
            parent=None,
            camera=None):
        super(ObjView, self).__init__(parent=parent)

        if camera is None:
            camera = MouseCamera(projection_type='perspective')

        self._camera = camera
        self.resetCamera()

        renderer = MonoInstanceRenderer(camera=camera, use_material=False)

        self._objpath = None
        self._camera = camera
        self.keyPressed.connect(self._camera.key_pressed)
        self.mouseEvent.connect(self._camera.mouse_event)

        self.renderer = renderer

    def _load_model(self):
        model = load_model(self.objSource)
        instance = ModelInstance(model=model)

        # make empty
        self.renderer.clear_instances()
        self.renderer.add_instance(instance)

        self.objModelUpdated.emit(model)

    @pyqtProperty(str)
    def objSource(self):
        return self._objpath

    @objSource.setter
    def objSource(self, value):
        print('objSource set:', value)
        if value[:7] == 'file://':
            value = value[7:]

        if value == self.objSource:
            return

        self._objpath = value
        self._load_model()

        self.update()

    @pyqtSlot()
    def resetCamera(self):
        set_camera_params(self._camera, default_camera_params)
        self.update()


def register_qml():
    qmlRegisterType(ObjView, 'ObjViewer', 1, 0, 'ObjView')


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

    run_qml('qml/objviewer_simple.qml')


if __name__ == '__main__':
    main()
