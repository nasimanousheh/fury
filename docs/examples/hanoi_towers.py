import numpy as np
import sys
from fury import actor, window, utils
from fury.window import vtk
from fury.utils import set_polydata_vertices, set_polydata_colors, set_polydata_normals, set_polydata_triangles
from fury.utils import numpy_to_vtk_points, numpy_to_vtk_colors, numpy_support

first_place = "A"
with_place = "B"
last_place= "C" 

towers_bases = {'A': np.array([0, 0, 0]), 'B': np.array([3, 0, 0]), 'C': np.array([6, 0, 0])}
towers_total_heights = {'A': 6, 'B': 0, 'C': 0}
individual_heights = {1: 3, 2: 3, 3: 3}
towers_elements = {'A': [1, 2, 3], 'B': [], 'C': []}


interactive = False

if interactive :
    h = input("How many disks are available? ")
    disk_number = float(h)
else:
    disk_number = 3

count = 0

class Counter(object):
    count = 0
    path = []

counter = Counter()

def move_disk(disk_number, first_place, last_place, with_place):

    if disk_number >= 1:
        move_disk(disk_number-1, first_place, with_place, last_place)
        counter.count += 1
        counter.path.append((first_place, last_place))
        print("moving disk from", first_place, "to", last_place, counter.count)
        move_disk(disk_number-1, with_place, last_place, first_place)


if disk_number < 3:
    print ("First rule in hanoitowe: number of disks should be more than 3!\n")
    sys.exit()
else:
    move_disk(disk_number, first_place, last_place, with_place)

    print ("minimum number of movements for ", disk_number, " disks is: " , counter.count)


scene = window.Scene()
scene.projection('perspective')
centers = np.array([[0, 0, 0.],
                    [0, 0 + 3, 0.],
                    [0, 3 + 3, 0.]]) 

directions = np.array([[0, 1, 0],
                       [0, 1, 0],
                       [0, 1, 0]]) 

# directions = np.random.ra
# nd(3, 3)
heights = np.array([3, 3, 3])
colors = np.array([[1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1.]])

cone_actor = actor.cube(centers, directions, colors, heights)
scene.add(cone_actor)
scene.add(actor.axes())
scene.set_camera(position=(5, 5, 30), focal_point=(0, 0, 0))
scene.background((1, 1, 1))

showm = window.ShowManager(scene,
                           size=(1900, 1080), reset_camera=False,
                           order_transparent=True)

showm.initialize()

# use itertools to avoid global variables
# import itertools
# counter_object = itertools.count()
cnt = 0

nb_pts = cone_actor.GetMapper().GetInput().GetReferenceCount()

pts = utils.numpy_support.vtk_to_numpy(
        cone_actor.GetMapper().GetInput().GetPoints().GetData())

def timer_callback(obj, event):
    global cnt, pts, nb_pts
    print('cnt', cnt)
    
    if cnt >= len(counter.path):
        return

    movement = counter.path[cnt]
    print(movement)
    
    before = movement[0]
    after = movement[1]
    print('before', before)
    print('after', after)
    print('tower_el_before', towers_elements)
    el = towers_elements[before].pop() 
    print('popped el', el)
    print('tower_el_before', towers_elements) 
    towers_elements[after].append(el)
    print(after)
    print('tower_el_after', towers_elements)
    
    # print(individual_heights[el])
    # he = individual_heights[el]
    
    base = towers_bases[after]
    print('base', base)
    centers_update = np.zeros((3, 3))
    centers_update[el - 1] -= centers[el - 1]
    new_height = 3 * (len(towers_elements[after]) - 1)
    print('new height', new_height) 
    centers_update[el - 1] +=  np.array([0, new_height, 0]) + base
    
    print('centers_update', centers_update) 
    centers[el - 1] += centers_update[el - 1]
    print('centers', centers[el - 1])
    centers_update = np.repeat(centers_update, pts.shape[0] / nb_pts, axis=0)
    pts += centers_update
    cone_actor.GetMapper().GetInput().SetPoints(numpy_to_vtk_points(pts))
    cone_actor.GetMapper().GetInput().ComputeBounds()

    #scene.camera_info()

    showm.render()
    
    cnt += 1


# Run every 1000 milliseconds
showm.add_timer_callback(True, 1000, timer_callback)

showm.render()
showm.start()
