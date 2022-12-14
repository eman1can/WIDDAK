cmake_minimum_required(VERSION 3.21)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_C_STANDARD 17)

project(GLFWTest)
project(VoxelRenderer)

include(TargetArch.cmake)

if (${CMAKE_HOST_WIN32})
    if ("${CMAKE_HOST_SYSTEM_PROCESSOR}" STREQUAL "AMD64")
        message("Windows 64-bit")
        set(GLFW_LIB "${CMAKE_SOURCE_DIR}/GLFW/win64/glfw3.lib")
        set(GLFW_BIN "${CMAKE_SOURCE_DIR}/GLFW/win64/glfw3.dll")
        set(GLEW_LIB "${CMAKE_SOURCE_DIR}/GLEW/win64/glew32.lib")
        set(GLEW_BIN "${CMAKE_SOURCE_DIR}/GLEW/win64/glew32.dll")
        set(SDL2_LIB "${CMAKE_SOURCE_DIR}/SDL2/win64/sdl2.lib")
        set(SDL2_BIN "${CMAKE_SOURCE_DIR}/SDL2/win64/sdl2.dll")
        set(SDL2_IMAGE_LIB "${CMAKE_SOURCE_DIR}/SDL2_IMAGE/win64/SDL2_image.lib")
        set(SDL2_IMAGE_BIN "${CMAKE_SOURCE_DIR}/SDL2_IMAGE/win64/SDL2_image.dll")
    else()
        message("Winows 32-bit")
        set(GLFW_LIB "${CMAKE_SOURCE_DIR}/GLFW/win32/glfw3.lib")
        set(GLFW_BIN "${CMAKE_SOURCE_DIR}/GLFW/win32/glfw3.dll")
        set(GLEW_LIB "${CMAKE_SOURCE_DIR}/GLEW/win32/glew32.lib")
        set(GLEW_BIN "${CMAKE_SOURCE_DIR}/GLEW/win32/glew32.dll")
        set(SDL2_LIB "${CMAKE_SOURCE_DIR}/SDL2/win32/sdl2.lib")
        set(SDL2_BIN "${CMAKE_SOURCE_DIR}/SDL2/win32/sdl2.dll")
        set(SDL2_IMAGE_LIB "${CMAKE_SOURCE_DIR}/SDL2_IMAGE/win32/SDL2_image.lib")
        set(SDL2_IMAGE_BIN "${CMAKE_SOURCE_DIR}/SDL2_IMAGE/win32/SDL2_image.dll")
    endif()
else()
    message("On a Mac")
endif()

message("${GLFW_LIB}")
message("${GLEW_LIB}")
message("${SDL2_LIB}")
message("${SDL2_IMAGE_LIB}")

add_executable(VoxelRenderer
        src/renderer.cpp
        src/input.cpp
        src/core.cpp
        src/shader_utils.cpp
        src/shape.cpp
        src/main.cpp)
target_link_libraries(VoxelRenderer ${GLEW_LIB} ${GLFW_LIB} ${SDL2_IMAGE_LIB} ${SDL2_LIB} opengl32.lib)
target_include_directories(VoxelRenderer PRIVATE include)
target_include_directories(VoxelRenderer PRIVATE GLFW/include)
target_include_directories(VoxelRenderer PRIVATE GLEW/include)
target_include_directories(VoxelRenderer PRIVATE SDL2/include)
target_include_directories(VoxelRenderer PRIVATE SDL2_IMAGE/include)
target_include_directories(VoxelRenderer PRIVATE GLM)

project(LibVoxel C)
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
add_library(LibVoxel SHARED
        src/renderer.cpp
        src/input.cpp
        src/core.cpp
        src/shader_utils.cpp
        src/shape.cpp
        src/main.cpp)
target_link_libraries(LibVoxel ${GLEW_LIB} ${GLFW_LIB} ${SDL2_IMAGE_LIB} ${SDL2_LIB} opengl32.lib)
target_include_directories(LibVoxel PRIVATE include)
target_include_directories(LibVoxel PRIVATE GLFW/include)
target_include_directories(LibVoxel PRIVATE GLEW/include)
target_include_directories(LibVoxel PRIVATE SDL2/include)
target_include_directories(LibVoxel PRIVATE SDL2_IMAGE/include)
target_include_directories(LibVoxel PRIVATE GLM)

file(COPY ${GLFW_BIN} DESTINATION ${CMAKE_BINARY_DIR})
file(COPY ${GLEW_BIN} DESTINATION ${CMAKE_BINARY_DIR})
file(COPY ${SDL2_BIN} DESTINATION ${CMAKE_BINARY_DIR})
file(COPY ${SDL2_IMAGE_BIN} DESTINATION ${CMAKE_BINARY_DIR})