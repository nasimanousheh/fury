import numpy as np
from dipy.viz import actor, window, widget
from dipy.data import fetch_viz_icons, read_viz_icons
import numpy.testing as npt


@npt.dec.skipif(not actor.have_vtk)
@npt.dec.skipif(not actor.have_vtk_colors)
def test_slider_widget():

    renderer = window.Renderer()

    # Create 2 lines with 2 different colors
    lines = [np.random.rand(10, 3), np.random.rand(20, 3)]
    colors = np.array([[1., 0., 0.], [0.8, 0., 0.]])
    c = actor.line(lines, colors, linewidth=3)

    renderer.add(c)

    show_manager = window.ShowManager(renderer)
    show_manager.initialize()

    def slider_callback(obj, event):
        print(obj)
        print(event)
        renderer.SetBackground(np.random.rand(3))

    slider = widget.slider(iren=show_manager.iren,
                           callback=slider_callback)
    # text = widget.text(slider.iren, None)

    show_manager.render()
    show_manager.start()

    arr = window.snapshot(renderer, size=(600, 600))
    report = window.analyze_snapshot(arr)


@npt.dec.skipif(not actor.have_vtk)
@npt.dec.skipif(not actor.have_vtk_colors)
def test_button_widget():

    from dipy.viz.window import vtk

    renderer = window.Renderer()

    lines = [np.random.rand(10, 3), np.random.rand(20, 3)]
    colors = np.array([[1., 0., 0.], [0.3, 0.7, 0.]])
    stream_actor = actor.streamtube(lines, colors)

    renderer.add(stream_actor)

    show_manager= window.ShowManager(renderer, size=(600, 600))

    def callback(obj, event):
        print(obj)
        print('Pressed')

    fetch_viz_icons()
    button_png = read_viz_icons(fname='home3.png')

    button = widget.button(show_manager.iren, callback,
                           button_png, (1., 1.), (80, 50))

    button_png_plus = read_viz_icons(fname='plus.png')
    button_plus = widget.button(show_manager.iren, callback,
                                button_png_plus, (1., .8), (120, 50))

    button_png_minus = read_viz_icons(fname='minus.png')
    button_minus = widget.button(show_manager.iren, callback,
                                 button_png_minus, (1., .8), (50, 50))

    def print_status(obj, event):
        print(obj)
        print(event)
        renderer.SetBackground(np.random.rand(3))

    slider = widget.slider(iren=show_manager.iren, callback=print_status,
                           coord1=(0.9, 0.5), coord2=(1., 0.5))

    show_manager.initialize()
    show_manager.render()

    button_norm_coords = (.9, 1.2)
    button_size = (50, 50)

    button.place(renderer)
    button_plus.place(renderer)
    button_minus.place(renderer)

    def win_callback(obj, event):
        # print(obj)
        print(event)
        print(obj.GetSize())

        button.place(renderer)
        button_plus.place(renderer)
        button_minus.place(renderer)
        # TODO
        # GET SLIDER REPRESENTATION HERE AND SET THE COORDINATES TO ALIGN
        # WITH BUTTONS
        slider.place
    # ren_win.AddObserver(vtk.vtkCommand.ModifiedEvent, win_callback)
    show_manager.add_window_callback(win_callback)

    show_manager.render()
    show_manager.start()

    arr = window.snapshot(renderer, size=(600, 600))


@npt.dec.skipif(not actor.have_vtk)
@npt.dec.skipif(not actor.have_vtk_colors)
def test_button_widget_show():

    renderer = window.renderer()

    lines = [np.random.rand(10, 3), np.random.rand(20, 3)]
    colors = np.array([[1., 0., 0.], [0.8, 0., 0.]])
    stream_actor = actor.line(lines, colors)

    window.add(renderer, stream_actor)

    # renderer.ResetCamera()

    from dipy.viz.window import ShowManager

    show_manager = ShowManager(renderer)

    def button_callback(obj, event):
        print('Button Pressed')

    show_manager.initialize()

    fetch_viz_icons()
    button_png = read_viz_icons(fname='home3.png')

    button = widget.button(show_manager.iren, button_callback,
                           button_png, (.8, 1.2), (40, 40))

    button.place(renderer)

    def win_callback(obj, event):
        print('Window modified')
        button.place(renderer)

    show_manager.add_window_callback(win_callback)

    show_manager.render()

    def text_callback(obj, event):
        print(event)
        print('Text moved')
        print(obj)
        print('Rep')
        print(obj.GetRepresentation())

    text = widget.text(show_manager.iren, text_callback, opacity=1., selectable=False, border=True)

    show_manager.render()
    show_manager.start()

    # show(renderer)

    arr = window.snapshot(renderer, size=(600, 600))

    report = window.analyze_snapshot(arr)

    print(report.objects)


if __name__ == '__main__':

    # test_slider_widget()
    test_button_widget()
    # npt.run_module_suite()
    # test_button_widget_show()