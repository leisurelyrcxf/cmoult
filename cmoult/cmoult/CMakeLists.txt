cmake_minimum_required(VERSION 3.4)

project(CmoultLib)

#Add all source files
file(GLOB_RECURSE source_files highlevel/* lowlevel/*)

#Add includes
include_directories(include)

#Add headers and libs path to libuminati 
include_directories()
link_directories()

#Output for binaries and libraries
set(EXECUTABLE_OUTPUT_PATH bin/)
set(LIBRARY_OUTPUT_PATH lib/)


#Build libcmoult.so
add_library(cmoult SHARED ${source_files})
#Cmoult requires libuminati
target_link_libraries(cmoult uminati)

#Build external manager
