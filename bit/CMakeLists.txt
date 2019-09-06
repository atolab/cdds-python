cmake_minimum_required(VERSION 3.7)

find_package(CycloneDDS)

idlc_generate(ddsbit bit.idl)
add_library(ddstubs SHARED dds_stubs.c)
target_link_libraries(ddstubs ddsbit CycloneDDS::ddsc)
