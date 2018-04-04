cmake_minimum_required(VERSION 3.9)
project(hw2)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS -fno-exceptions)


add_executable(hw2 main.cpp myexceptions.h)