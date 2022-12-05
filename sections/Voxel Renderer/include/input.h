//
// Created by Zoe on 11/11/2022.
//

#ifndef LIBVOXEL_INPUT_H
#define LIBVOXEL_INPUT_H

#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include "renderer.h"

class Input {
public:
    static Input& getInstance(void* renderer) {
        static Input instance; // lazy singleton, instantiated on first use
        if (renderer != nullptr)
            instance.renderer = renderer;
        return instance;
    }

    static void onResize(GLFWwindow* win, int w, int h) { getInstance(nullptr).onResizeImpl(win, w, h); }
    void onResizeImpl(GLFWwindow* win, int w, int h) { ((Renderer*) renderer)->onResize(win, w, h); }

    static void onMouseButton(GLFWwindow* win, int b, int a, int m) { getInstance(nullptr).onMouseButtonImpl(win, b, a, m); }
    void onMouseButtonImpl(GLFWwindow* win, int b, int a, int m) { ((Renderer*) renderer)->onMouseButton(win, b, a, m); }

    static void onMouse(GLFWwindow* win, double x, double y) { getInstance(nullptr).onMouseImpl(win, x, y); }
    void onMouseImpl(GLFWwindow* win, double x, double y) { ((Renderer*) renderer)->onMouse(win, (float) x, (float) y); }

    static void onKeyboard(GLFWwindow* win, int k, int s, int a, int m) { getInstance(nullptr).onKeyboardImpl(win, k, s, a, m); }
    void onKeyboardImpl(GLFWwindow* win, int k, int s, int a, int m) { ((Renderer*) renderer)->onKeyboard(win, k, s, a, m); }

    Input(Input const&) = delete;
    void operator=(Input const&) = delete;
private:
    Input() = default;
    void* renderer;
};


#endif //LIBVOXEL_INPUT_H
