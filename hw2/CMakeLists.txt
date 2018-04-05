cmake_minimum_required(VERSION 3.9)
project(hw2)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS -fno-exceptions)


add_executable(good_example_1 good_example_1.cpp myexceptions.h)
add_executable(good_example_2 good_example_2.cpp myexceptions.h)

add_executable(bad_example_1 bad_example_1.cpp myexceptions.h)
add_executable(bad_example_2 bad_example_2.cpp myexceptions.h)