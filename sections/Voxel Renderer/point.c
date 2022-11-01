//
// Created by Zoe on 10/31/2022.
//

#include <stdint.h>
#include <stdio.h>

void hello_world();

typedef struct {
    int32_t x;
    int32_t y;
} Point;

void show_point(Point p) {
    printf("Point in C is (%d, %d)\n", p.x, p.y);
}

int32_t add_point(Point p) {

}