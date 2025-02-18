# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

#[=======================================================================[.rst:
FindLibLZMA
-----------

Find LibLZMA

Find LibLZMA headers and library


IMPORTED Targets
^^^^^^^^^^^^^^^^

This module defines :prop_tgt:`IMPORTED` target ``LibLZMA::LibLZMA``, if
LibLZMA has been found.

Result variables
^^^^^^^^^^^^^^^^

This module will set the following variables in your project:

::

  LIBLZMA_FOUND             - True if liblzma is found.
  LIBLZMA_INCLUDE_DIRS      - Directory where liblzma headers are located.
  LIBLZMA_LIBRARIES         - Lzma libraries to link against.
  #LIBLZMA_HAS_AUTO_DECODER  - True if lzma_auto_decoder() is found (required).
  #LIBLZMA_HAS_EASY_ENCODER  - True if lzma_easy_encoder() is found (required).
  #LIBLZMA_HAS_LZMA_PRESET   - True if lzma_lzma_preset() is found (required).
  LIBLZMA_VERSION_MAJOR     - The major version of lzma
  LIBLZMA_VERSION_MINOR     - The minor version of lzma
  LIBLZMA_VERSION_PATCH     - The patch version of lzma
  LIBLZMA_VERSION_STRING    - version number as a string (ex: "5.0.3")
#]=======================================================================]

find_path(LIBLZMA_INCLUDE_DIR lzma.h )
find_library(LIBLZMA_LIBRARY NAMES lzma liblzma)

if(LIBLZMA_INCLUDE_DIR AND EXISTS "${LIBLZMA_INCLUDE_DIR}/lzma/version.h")
    file(STRINGS "${LIBLZMA_INCLUDE_DIR}/lzma/version.h" LIBLZMA_HEADER_CONTENTS REGEX "#define LZMA_VERSION_[A-Z]+ [0-9]+")

    string(REGEX REPLACE ".*#define LZMA_VERSION_MAJOR ([0-9]+).*" "\\1" LIBLZMA_VERSION_MAJOR "${LIBLZMA_HEADER_CONTENTS}")
    string(REGEX REPLACE ".*#define LZMA_VERSION_MINOR ([0-9]+).*" "\\1" LIBLZMA_VERSION_MINOR "${LIBLZMA_HEADER_CONTENTS}")
    string(REGEX REPLACE ".*#define LZMA_VERSION_PATCH ([0-9]+).*" "\\1" LIBLZMA_VERSION_PATCH "${LIBLZMA_HEADER_CONTENTS}")

    set(LIBLZMA_VERSION_STRING "${LIBLZMA_VERSION_MAJOR}.${LIBLZMA_VERSION_MINOR}.${LIBLZMA_VERSION_PATCH}")
    unset(LIBLZMA_HEADER_CONTENTS)
endif()

# We're using new code known now as XZ, even library still been called LZMA
# it can be found in http://tukaani.org/xz/
# Avoid using old codebase
if (LIBLZMA_LIBRARY)
   include(CheckLibraryExists)
   set(CMAKE_REQUIRED_QUIET_SAVE ${CMAKE_REQUIRED_QUIET})
   set(CMAKE_REQUIRED_QUIET ${LibLZMA_FIND_QUIETLY})
   #CHECK_LIBRARY_EXISTS(${LIBLZMA_LIBRARY} lzma_auto_decoder "" LIBLZMA_HAS_AUTO_DECODER)
   #CHECK_LIBRARY_EXISTS(${LIBLZMA_LIBRARY} lzma_easy_encoder "" LIBLZMA_HAS_EASY_ENCODER)
   #CHECK_LIBRARY_EXISTS(${LIBLZMA_LIBRARY} lzma_lzma_preset "" LIBLZMA_HAS_LZMA_PRESET)
   set(CMAKE_REQUIRED_QUIET ${CMAKE_REQUIRED_QUIET_SAVE})
endif ()

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(LibLZMA  REQUIRED_VARS  LIBLZMA_LIBRARY
                                                          LIBLZMA_INCLUDE_DIR
                                                          #LIBLZMA_HAS_AUTO_DECODER
                                                          #LIBLZMA_HAS_EASY_ENCODER
                                                          #LIBLZMA_HAS_LZMA_PRESET
                                           VERSION_VAR    LIBLZMA_VERSION_STRING
                                 )
mark_as_advanced( LIBLZMA_INCLUDE_DIR LIBLZMA_LIBRARY )

if (LIBLZMA_FOUND)
    set(LIBLZMA_LIBRARIES ${LIBLZMA_LIBRARY})
    set(LIBLZMA_INCLUDE_DIRS ${LIBLZMA_INCLUDE_DIR})
    if(NOT TARGET LibLZMA::LibLZMA)
        add_library(LibLZMA::LibLZMA UNKNOWN IMPORTED)
        set_target_properties(LibLZMA::LibLZMA PROPERTIES
                              INTERFACE_INCLUDE_DIRECTORIES ${LIBLZMA_INCLUDE_DIR}
                              IMPORTED_LINK_INTERFACE_LANGUAGES C
                              IMPORTED_LOCATION ${LIBLZMA_LIBRARY})
    endif()
endif ()
