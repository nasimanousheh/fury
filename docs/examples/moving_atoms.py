import numpy as np
from fury import window, actor, ui
from vtk.util import numpy_support
import itertools
from pdb import set_trace


lammps_file = open('C:\\Users\\nasim\\Documents\\Python Scripts\\Practice\\propagation.lammpstrj', 'r')

lines = lammps_file.readlines()

no_atoms = int(lines[3])
line_lx = list(map(float, lines[5].split('\n')[0].split('\t')))
line_ly = list(map(float, lines[6].split('\n')[0].split('\t')))
line_lz = list(map(float, lines[7].split('\n')[0].split('\t')))

box_lx = (np.abs(line_lx[0])+np.abs(line_lx[1]))
box_ly = (np.abs(line_ly[0])+np.abs(line_ly[1]))
box_lz = (np.abs(line_lz[0])+np.abs(line_lz[1]))
header = 9
step = 0
no_frames = 0

# all_nframes = np.empty((0, 6), dtype=np.float)
all_nframes = []

while True:
    frame = lines[header + step: header + step + no_atoms]

    numerical_frame = np.zeros((len(frame), 5))
    for i in range(len(frame)):
        numerical_frame[i] = list(map(float, frame[i].split('\n')[0].split('\t')))
    all_nframes.append(numerical_frame)
    step += header + no_atoms
    no_frames += 1

    if step >= len(lines):
        break
xyz = all_nframes[0][:, 2:5]

scene = window.Scene()
box_centers = np.array([[0, 0, 0.]])
box_directions = np.array([[0, 1, 0]])
box_colors = np.array([[1, 0, 0, 0.2]])
box_actor = actor.box(box_centers, box_directions, box_colors,
                      size=(box_lx, box_ly, box_lz),
                      heights=2, vertices=None, faces=None)
box_actor.GetProperty().SetRepresentationToWireframe()
box_actor.GetProperty().SetLineWidth(10)
atom_types = all_nframes[0][:, 1]


print(atom_types)
colors = np.ones((no_atoms, 3))
colors[atom_types == 1] = np.array([1., 0, 0])
colors[atom_types == -1] = np.array([0, 0, 1.])

radii = 0.1 * np.ones(no_atoms)

scene = window.Scene()

sphere_actor = actor.sphere(centers=xyz,
                            colors=colors,
                            radii=radii, theta=6, phi=6)

scene.add(sphere_actor)
scene.add(box_actor)

showm = window.ShowManager(scene,
                           size=(900, 768), reset_camera=False,
                           order_transparent=True)

showm.initialize()

tb = ui.TextBlock2D(bold=True)

# use itertools to avoid global variables
counter = itertools.count()


def get_vertices(act):

    all_vertices = np.array(numpy_support.vtk_to_numpy(
        act.GetMapper().GetInput().GetPoints().GetData()))
    return all_vertices


def set_vertices(act, num_arr):

    vtk_num_array = numpy_support.numpy_to_vtk(num_arr)
    act.GetMapper().GetInput().GetPoints().SetData(vtk_num_array)

def modified(act):
    act.GetMapper().GetInput().GetPoints().GetData().Modified()
    act.GetMapper().GetInput().ComputeBounds()


global all_vertices
all_vertices = get_vertices(sphere_actor)
initial_vertices = all_vertices.copy()
no_vertices_per_sphere = len(all_vertices) / no_atoms

# set_trace()
pos = all_nframes[0][:, 2:5]


def timer_callback(_obj, _event):
    cnt = next(counter)

    tb.message = "Let's count up to 100 and exit :" + str(cnt)

    pos = all_nframes[cnt][:, 2:5]# .copy()

    #print(pos)

    # all_vertices = np.array(numpy_support.vtk_to_numpy(
    #    sphere_actor.GetMapper().GetInput().GetPoints().GetData()))

    # all_vertices = get_vertices(sphere_actor)
    all_vertices[:] = initial_vertices + \
        np.repeat(pos, no_vertices_per_sphere, axis=0)

    # all_vertices[:] += np.random.rand(*all_vertices.shape)

    set_vertices(sphere_actor, all_vertices)
    modified(sphere_actor)

    showm.render()
    if cnt == no_frames - 1:
        showm.exit()


scene.add(tb)

# Run every 200 milliseconds
showm.add_timer_callback(True, 500, timer_callback)

showm.start()

