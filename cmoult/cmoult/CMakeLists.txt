cmake_minimum_required(VERSION 3.4)

project(CmoultLib)

#Add all source files (remove extern_manager from it)
file(GLOB_RECURSE source_files src/* include/*)
list(REMOVE_ITEM source_files ${CMAKE_CURRENT_SOURCE_DIR}/src/highlevel/managers/extern_manager.c)

#Add includes
include_directories(include)

#Add headers and libs path to libuminati 
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../libuminati/include)
link_directories(${CMAKE_CURRENT_SOURCE_DIR}/../libuminati/lib)

#Output for binaries and libraries
set(EXECUTABLE_OUTPUT_PATH bin/)
set(LIBRARY_OUTPUT_PATH lib/)


#Build libcmoult.so
add_library(cmoult SHARED ${source_files})
#Cmoult requires libuminati
target_link_libraries(cmoult uminati config dl pthread)

#Build external manager
add_executable(
    cmoult_manager
    src/highlevel/managers/extern_manager.c
    src/highlevel/managers/common.c
    src/highlevel/listeners/common.c
    src/highlevel/listeners/socket_listener.c
    src/common.c
    src/highlevel/updates/update.c
)

target_link_libraries(cmoult_manager pthread uminati config dl)
