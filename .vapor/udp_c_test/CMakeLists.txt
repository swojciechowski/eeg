cmake_minimum_required(VERSION 3.0.0)
project(udp-test VERSION 0.1.0 LANGUAGES C CXX)

include(CTest)
enable_testing()

add_executable(udp-server server.cpp)
target_link_libraries(udp-server wsock32 ws2_32)

add_executable(udp-client client.cpp)
target_link_libraries(udp-client wsock32 ws2_32)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
