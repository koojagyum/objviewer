import numpy as np
import pywavefront

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def read_objfile(filepath):
    scene = pywavefront.Wavefront(filepath, collect_faces=True)
    v = np.array(scene.vertices, dtype=np.float32)
    e = []
    for name, mesh in scene.meshes.items():
        e += mesh.faces

    return v, e


def plot_3d(v, color='blue'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(
        v[:,0],
        v[:,1],
        v[:,2],
        color=color,
        marker='.',
        linestyle='None'
    )

    # ax.set_xlim(-1.0, 1.0)
    # ax.set_ylim(-1.0, 1.0)
    # ax.set_zlim(-1.0, 1.0)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


def plot_3ds(verts):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i, v in enumerate(verts):
        color_spec = 'C{}'.format(i)
        ax.scatter(
            v[:,0],
            v[:,1],
            v[:,2],
            color=color_spec,
            marker='.',
            linestyle='None',
            label='v{}'.format(i)
        )

    ax.legend()
    
    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-1.0, 1.0)
    ax.set_zlim(-1.0, 1.0)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


def plot_2ds(verts):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for i, v in enumerate(verts):
        color_spec = 'C{}'.format(i)
        ax.scatter(
            v[:,0],
            v[:,1],
            color=color_spec,
            marker='.',
            linestyle='None',
            label='v{}'.format(i)
        )

    ax.legend()
    
    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-1.0, 1.0)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    plt.show()


INFILE = 'objviewer/teapod.obj'

v, e = read_objfile(INFILE)

plot_3d(v)
