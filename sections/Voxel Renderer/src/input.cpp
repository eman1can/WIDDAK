//
// Created by Zoe on 11/11/2022.
//

#include "renderer.h"

void Renderer::onResize(GLFWwindow* window, int width, int height) {
    setSize(width, height);
}

void Renderer::onMouseButton(GLFWwindow* window, int button, int action, int mods) {
    printf("%d, %d, %d\n", button, action, mods);
    if (button == 0) {
        if (!_locked) {
            _locked = true;
            glfwSetInputMode(_window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
        }
        if (action == 1)
            camera_speed *= 5;
        else
            camera_speed /= 5;
    }
}

void Renderer::onMouse(GLFWwindow*, float x, float y) {
    float x_off = x - _last_x;
    float y_off = y - _last_y;
    _last_x = x;
    _last_y = y;

    if (first_mouse) {
        first_mouse = false;
        return;
    }

    if (!_locked)
        return;

    x_off *= camera_sensitivity;
    y_off *= camera_sensitivity;

    yaw += x_off;
    pitch -= y_off;

    if (pitch > 89.0f)
        pitch = 89.0f;
    if (pitch < -89.0f)
        pitch = -89.0f;

    glm::vec3 direction;
    direction.x = cos(glm::radians(yaw)) * cos(glm::radians(pitch));
    direction.y = sin(glm::radians(pitch));
    direction.z = sin(glm::radians(yaw)) * cos(glm::radians(pitch));
    camera_front = glm::normalize(direction);
}

void Renderer::onKeyboard(GLFWwindow* window, int keycode, int scancode, int action, int mods) {
    if (action == 1 || action == 2) {
        switch (keycode) {
            case 87: // W
                key_translate.z = 1;
                break;
            case 83: // S
                key_translate.z = -1;
                break;
            case 68: // D
                key_translate.x = 1;
                break;
            case 65: // A
                key_translate.x = -1;
                break;
            case 32: // Space
                key_translate.y = 1;
                break;
            case 340: // Shift
                key_translate.y = -1;
                break;
            case 256: // Escape
                glfwSetInputMode(_window, GLFW_CURSOR, GLFW_CURSOR_NORMAL);
                _locked = false;
                break;
            default:
                printf("Unhandled Keycode: %d, %d, %d, %d\n", keycode, scancode, action, mods);
                break;
        }
    } else {
        switch (keycode) {
            case 87: // W
                if (key_translate.z == 1)
                    key_translate.z = 0;
                break;
            case 83: // S
                if (key_translate.z == -1)
                    key_translate.z = 0;
                break;
            case 68: // D
                if (key_translate.x == 1)
                    key_translate.x = 0;
                break;
            case 65: // A
                if (key_translate.x == -1)
                    key_translate.x = 0;
                break;
            case 32: // Space
                if (key_translate.y == 1)
                    key_translate.y = 0;
                break;
            case 340: // Shift
                if (key_translate.y == -1)
                    key_translate.y = 0;
                break;
            default:
                break;
        }
    }
}