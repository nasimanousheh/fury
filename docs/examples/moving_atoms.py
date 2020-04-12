import numpy as np
from fury import window, actor, ui
from vtk.util import numpy_support
import itertools
from pdb import set_trace


lammps_file = open('C:\\Users\\nasim\\Documents\\Python Scripts\\Practice\\propagation.lammpstrj', 'r')

lines = lammps_file.readlines()

no_atoms = int(lines[3])
print(no_atoms)
header = 9
step = 0

no_frames = 0

# all_nframes = np.empty((0, 6), dtype=np.float)
all_nframes = []

while True:
    frame = lines[header + step: header + step + no_atoms]

    numerical_frame = np.zeros((len(frame), 6))
    for i in range(len(frame)):
        numerical_frame[i] = list(map(float, frame[i].split('\n')[0].split('\t')))
    # np.append(all_nframes, numerical_frame, axis=0)
    all_nframes.append(numerical_frame)
    step += header + no_atoms
    no_frames += 1
    if step >= len(lines):
        break

xyz = all_nframes[0][:, 2:5]

colors = np.random.rand(no_atoms, 3)
radii = 0.1 * np.ones(no_atoms)

scene = window.Scene()

sphere_actor = actor.sphere(centers=xyz,
                            colors=colors,
                            radii=radii)

scene.add(sphere_actor)

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

    print(pos)

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

