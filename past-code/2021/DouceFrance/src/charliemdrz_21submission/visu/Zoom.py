"""
Class used to zoom in the visualization

"""

from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import Scatter
from kivy.properties import ObjectProperty


class Zoom(ScatterLayout):
    move_lock = False
    scale_lock_left = False
    scale_lock_right = False
    scale_lock_top = False
    scale_lock_bottom = False
    auto_bring_to_front = False

    initial_pos = None

    obj = ObjectProperty(None)


    def focus(self):
        self.scale = 1
        self.pos = self.initial_pos


    def on_touch_move(self, touch):
        if touch.button != 'right':
            super(Zoom, self).on_touch_move(touch)


    def on_touch_up(self, touch):
        self.move_lock = False
        self.scale_lock_left = False
        self.scale_lock_right = False
        self.scale_lock_top = False
        self.scale_lock_bottom = False
        if touch.grab_current is self:
            touch.ungrab(self)
            x = self.pos[0] / 10
            x = round(x, 0)
            x = x * 10
            y = self.pos[1] / 10
            y = round(y, 0)
            y = y * 10
            self.pos = x, y

            return super(Zoom, self).on_touch_up(touch)

    def transform_to_local(self, point):
        return super(Zoom, self).to_local(point[0], point[1])

    def transform_to_parent(self, point):
        return super(Zoom, self).to_parent(point[0], point[1])


    def on_touch_down(self, touch):



        x, y = touch.x, touch.y
        self.prev_x = touch.x
        self.prev_y = touch.y

        if touch.is_mouse_scrolling:

            (x_before, y_before) = self.transform_to_local(touch.pos) # Take the position under the pointer

            if touch.button == 'scrolldown':
                if self.scale < 30:
                    self.scale = self.scale * 1.1

            elif touch.button == 'scrollup':
                if self.scale > 0.8:
                    self.scale = self.scale * 0.9

            (x_before, y_before) = self.transform_to_parent((x_before, y_before))
            (x_after, y_after) = touch.pos
            dx, dy = x_after-x_before, y_after-y_before
            self.center = (self.center[0]+dx, self.center[1]+dy)


        if not self.do_collide_after_children:
            if not self.collide_point(x, y):
                return False

        if touch.button != 'left':
            touch.push()
            touch.apply_transform_2d(self.to_local)
            if super(Scatter, self).on_touch_down(touch):
                if 'multitouch_sim' in touch.profile:
                    touch.multitouch_sim = True
                touch.pop()
                self._bring_to_front(touch)
                return True
            touch.pop()

            if not self.do_translation_x and \
                    not self.do_translation_y and \
                    not self.do_rotation and \
                    not self.do_scale:
                return False

        if self.do_collide_after_children:
            if not self.collide_point(x, y):
                return False

        if 'multitouch_sim' in touch.profile:
            touch.multitouch_sim = True
        self._bring_to_front(touch)
        touch.grab(self)
        self._touches.append(touch)
        self._last_touch_pos[touch] = touch.pos

        return True
