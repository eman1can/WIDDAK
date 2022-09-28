# -*- coding: utf-8 -*-
"""
The main app

"""

import sys
from os.path import join, isdir
from os import listdir
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.stencilview import StencilView

Window.maximize()  # Fullscreen


class BoxStencil(BoxLayout, StencilView):
    """
    A box that avoid its child go out its borders.
    """

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(BoxStencil, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(BoxStencil, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(BoxStencil, self).on_touch_up(touch)


class Interface(BoxLayout):
    """
    Main interface

    """

    buttons_coordinates = {}
    nb_disabled = 0
    my_zoom = ObjectProperty(None)
    button_box = ObjectProperty(None)
    current_filepath = StringProperty("choose_a_map.png")
    stock_name = StringProperty("No stock")

    def __init__(self, stock_name, **kwargs):
        super(Interface, self).__init__(**kwargs)
        self.stock_name = stock_name

        stock_dir = join("stock", self.stock_name)
        maps = listdir(stock_dir)

        for map_name in maps:
            self.button_box.add_widget(Button(text=map_name[:-4], on_release=self.display_map))

    def display_map(self, button):
        self.current_filepath = join("stock", self.stock_name, button.text + ".png")


class GuiApp(App):
    """
    The app
    """

    def __init__(self, stock_name, **kwargs):
        super(GuiApp, self).__init__(**kwargs)
        self.stock_name = stock_name

    def build(self):
        root = Interface(self.stock_name)
        return root


if __name__ == '__main__':

    try:
        assert (len(sys.argv) == 2)
    except AssertionError:
        print("ERROR \nUsage: python .\\map_visu.py <stock_name>")
        sys.exit(1)

    stock_name = sys.argv[1]

    stock_dir = join("stock", stock_name)

    try:
        assert (isdir(stock_dir))
    except AssertionError:
        print("ERROR \nThe stock you specified does not exist.")
        sys.exit(1)

    GuiApp(stock_name).run()
