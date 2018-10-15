rosbuild_add_library(libhokuyo hokuyo.cpp)
find_library(LOG4CXX_LIBRARY log4cxx)
target_link_libraries(libhokuyo ${LOG4CXX_LIBRARY})
