cmake_minimum_required(VERSION 3.5.0)
project(emotiv-server VERSION 0.1.0 LANGUAGES C CXX)

include(CTest)
enable_testing()

add_executable(emotiv-server emotiv_server.cpp edk_helpers.cpp udp.cpp)

target_include_directories(emotiv-server PRIVATE "./edk/headers")
target_link_libraries(emotiv-server "./edk/lib/edk.lib")
target_link_libraries(emotiv-server wsock32 ws2_32)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
