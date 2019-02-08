import argparse
import numpy as np
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QTimer

from facelm.detector import FaceDetector
from util import geo
from pyglfw.model import ColorModel
from pyqt5glfw.qquickglitem import QQuickGLItem

from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import qmlRegisterType

from .flip import FlipRenderer

from pyglfw.instance import ModelInstance
from pyglfw.instance import MonoInstanceRenderer
from pyglfw.renderer import RendererGroup
from pyglfw.video import Webcam
from pyglfw.video import VideoRenderer


class FaceView(QQuickGLItem):

    requestUpdate = pyqtSignal()
    setFloatParam = pyqtSignal(str, float)

    def __init__(self, parent=None):
        super(FaceView, self).__init__(parent=parent)

        self._params = {}
        self._size = QSize()
        self.detector = FaceDetector()

        lip_faces = np.array(
            [
                [54, 55, 64],
                [55, 65, 64],
                [55, 56, 65],
                [56, 66, 65],
                [56, 57, 66],
                [57, 67, 66],
                [57, 58, 67],
                [58, 59, 67],
                [59, 60, 67],
                [59, 48, 60],
            ],
            dtype=np.uint8
        )

        lm_model = ColorModel(
            name='facelm_model',
            color=np.array([1.0, 0.3, 0.3], dtype=np.float32),
            faces = lip_faces,
            draw_point=False
        )
        self.lm_model = lm_model

        self.requestUpdate.connect(self._requestUpdate)
        self.setFloatParam.connect(self._setFloatParam)

        # Fixme: workaround...
        QTimer.singleShot(500, lambda: self.update())

    def geometryChanged(self, newGeometry, oldGeometry):
        if not newGeometry.isEmpty():
            if newGeometry.width() != self._size.width() or \
               newGeometry.height() != self._size.height():
                self._update_size(newGeometry.width(), newGeometry.height())
                self.update()

    def _update_size(self, w=0, h=0):
        if self.provider is None:
            return

        if w <= 0 or h <= 0:
            w, h = self.width(), self.height()

        w, h = geo.scale(1.0, self.provider.aspect_ratio, w, h, True)

        self._size.setWidth(w)
        self._size.setHeight(h)
        self.setWidth(w)
        self.setHeight(h)

    def _update_frame(self, image):
        if image is None:
            return None

        _, shapes = self.detector.detect(image)
        if shapes.shape[0] > 0:
            v_ndc = geo.to_ndc(
                shapes[0].astype(np.float32),
                (image.shape[1], image.shape[0])
            )
            self.lm_model.vertices = v_ndc

        return image

    def _requestUpdate(self):
        self.update()

    def _setFloatParam(self, key, value):
        self._params[key] = value
        self.update()


class LiveFaceView(FaceView):

    def __init__(self, parent=None, play=False):
        super(LiveFaceView, self).__init__(parent=parent)

        self._play = False

        lm_instance = ModelInstance(
            name='facelm_instance',
            model=self.lm_model,
            # Points in framebuffer are not rendered
            # so we need to flip their coordinates
            scale=[-1.0, 1.0, 1.0]
        )

        provider = Webcam()
        vrend = VideoRenderer(
            video_source=provider,
            frame_block=self._update_frame
        )
        irend = MonoInstanceRenderer()
        irend.instances.append(lm_instance)

        flip = FlipRenderer(
            width=720,
            height=405,
            inner_renderer=vrend
        )

        group = RendererGroup()
        group.renderers.append(irend)
        group.renderers.append(flip)

        self.renderer = group
        self.provider = provider
        self.play = play

    def __del__(self):
        self.play = False

    def _update_frame(self, image):
        ret = super(LiveFaceView, self)._update_frame(image)
        if ret is not None:
            self.requestUpdate.emit()

        return ret

    @pyqtProperty(bool)
    def play(self):
        return self._play

    @play.setter
    def play(self, value):
        if self._play != value:
            self._play = value
            if value:
                self.provider.start()
            else:
                self.provider.stop()

    # TODO: Add about resume
    def _onInvalidateUnderlay(self):
        super(LiveFaceView, self)._onInvalidateUnderlay()
        self.play = False


def run_qml(qmlpath):
    app = QGuiApplication(sys.argv)

    qmlRegisterType(LiveFaceView, 'FaceWarp', 1, 0, 'LiveFaceView')

    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.setSource(QUrl(qmlpath))
    view.show()

    sys.exit(app.exec_())


def main():
    global verbose

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        default=False,
        help='Print debug string'
    )

    args = parser.parse_args()
    verbose = args.verbose

    run_qml('qml/lip_test.qml')


if __name__ == '__main__':
    main()
