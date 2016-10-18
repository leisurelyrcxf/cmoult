cmake_minimum_required(VERSION 3.4)

project(libama)

#Add all source files
file(GLOB_RECURSE source_files src/* include/*)
list(REMOVE_ITEM source_files ${CMAKE_CURRENT_SOURCE_DIR}/src/main.c ${CMAKE_CURRENT_SOURCE_DIR}/test/*)

#Add includes
include_directories(include include/luminati)


#We cannot use pkg-config for finding these paths, so we have to guess
EXEC_PROGRAM(${CMAKE_CURRENT_SOURCE_DIR}/finddw ARGS "h" OUTPUT_VARIABLE dwh_path)
EXEC_PROGRAM(${CMAKE_CURRENT_SOURCE_DIR}/finddw ARGS "l" OUTPUT_VARIABLE dwl_path)

include_directories(SYSTEM ${dwh_path})
link_directories(${dwl_path})


#Output binaries into bin
set(EXECUTABLE_OUTPUT_PATH bin/)
#Output libs into lib
set(LIBRARY_OUTPUT_PATH lib/)





add_executable(testama ${source_files} ${CMAKE_CURRENT_SOURCE_DIR}/src/main.c)

#libama requires libdw
target_link_libraries(testama dw bfd elf iberty)




