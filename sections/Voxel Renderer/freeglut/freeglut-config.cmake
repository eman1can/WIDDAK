set(GLUT_INCLUDE_DIRS "${CMAKE_CURRENT_LIST_DIR}/include")

# Support both 32 and 64 bit builds
if (CMAKE_SIZEOF_VOID_P EQUAL 8)
  set(GLUT_LIBRARIES "${CMAKE_CURRENT_LIST_DIR}/lib/x64/freeglut.lib")
  set(GLUT_BINARIES "${CMAKE_CURRENT_LIST_DIR}/bin/x64/freeglut.dll")
else ()
  set(GLUT_LIBRARIES "${CMAKE_CURRENT_LIST_DIR}/lib/freeglut.lib")
  set(GLUT_BINARIES "${CMAKE_CURRENT_LIST_DIR}/bin/freeglut.dll")
endif ()

string(STRIP "${SDL2_LIBRARIES}" SDL2_LIBRARIES)