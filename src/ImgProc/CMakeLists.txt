#configure_file(${CMAKE_CURRENT_SOURCE_DIR}/config.h.cmake ${CMAKE_CURRENT_BINARY_DIR}/config.h)
cmake_minimum_required(VERSION 3.5)

project(ImgProc VERSION 0.1 LANGUAGES CXX)

add_subdirectory(GameRecognize)
add_subdirectory(UI)


########### install files ###############




#original Makefile.am contents follow:

#SUBDIRS=GameRecognize UI
