import argparse
import math
import numpy as np
import os
import pywavefront
import sys

from app.flip import FlipRenderer
from PyQt5.QtWidgets import QApplication
from pyqt5glfw.glwidget import GLWidget
from pyglfw.instance import ModelInstance
from pyglfw.instance import MonoInstanceRenderer
from pyglfw.mousecamera import MouseCamera
from pyglfw.renderer import RendererGroup
from pyglfw.scene import Scene
from pyglfw.model import ColorModel
from pyglfw.video import FrameProvider


def read_objfile(objfile):
    scene = pywavefront.Wavefront(
        objfile,
        collect_faces=True
    )
    v = np.array(scene.vertices, dtype=np.float32)
    e = []
    for name, mesh in scene.meshes.items():
        e += mesh.faces

    return v, np.array(e, dtype=np.uint16)


def load_model(objfile=None, color=(0.0, 1.0, 0.0)):
    if objfile is None:
        return None

    name = os.path.splitext(os.path.basename(objfile))[0]
    v, e = read_objfile(objfile)

    return ColorModel(
        name=name,
        vertices=v,
        edges=None,
        faces=e,
        color=color,
        attributes=None,
        wireframe=True,
        # draw_point=True
        draw_point=False
    )


def test_objview(filepath):
    app = QApplication(sys.argv)

    renderer = MonoInstanceRenderer(
        camera=MouseCamera(projection_type='perspective'),
        # camera=MouseCamera(projection_type='orthographic'),
        use_material=False
    )

    model1 = load_model(filepath)
    instance1 = ModelInstance(model=model1)

    renderer.instances.append(instance1)

    renderer.camera.yaw = math.radians(273.0)
    renderer.camera.pitch = math.radians(-15.0)
    renderer.camera.position = np.array([-0.21, 0.63, 3.13], dtype=np.float32)
    # renderer.camera.set_projection(aspect_ratio=900.0/1600.0)

    w = GLWidget()
    w.renderer = renderer
    w.keyPressed.connect(renderer.camera.key_pressed)
    w.mouseEvent.connect(renderer.camera.mouse_event)
    # w.setMouseTracking(False)
    w.show()

    sys.exit(app.exec_())


def main():
    global verbose

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        default=True,
        help='Print debug string'
    )
    parser.add_argument(
        '--filepath', '-f',
        required=True,
        help='Filepath for obj file'
    )

    args = parser.parse_args()

    verbose = args.verbose
    filepath = args.filepath

    test_objview(filepath)


if __name__ == '__main__':
    main()
