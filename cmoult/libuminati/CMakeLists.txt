cmake_minimum_required(VERSION 3.4)

project(Libuminati)

#Add all source files
file(GLOB_RECURSE source_files src/* include/*)


#Add includes
include_directories(include)

#We cannot use pkg-config for finding these paths, so we have to guess
#TODO, find a way to automate this
include_directories(SYSTEM /usr/include/elfutils)


#Output binaries into bin
set(EXECUTABLE_OUTPUT_PATH bin/)
#Output libs into lib
set(LIBRARY_OUTPUT_PATH lib/)


#This CMake file provides libuminati
add_library(uminati SHARED ${source_files})

#Libuminati requires libdw
target_link_libraries(uminati dw)


