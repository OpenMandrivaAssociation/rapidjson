# There are no files that we can get debug info from
%global debug_package %{nil}

%bcond_without	doc

Name:		rapidjson
Version:	1.2.0~20250417
Release:	1
Summary:	A fast JSON parser/generator for C++
Group:		Development/C++
License:	BSD
URL:		https://rapidjson.org/
#Source0:	https://github.com/Tencent/rapidjson/archive/v%{version}/%{name}-%{version}.tar.gz
Source0:	https://github.com/Tencent/rapidjson/archive/refs/heads/master.tar.gz
#Patch0:	remove-Werror-cmakelist.patch
# Remove a method from rapidjson/document.h that can't possibly work
# (writes to a const member), and that breaks builds if the file is
# merely included
#Patch0:		rapidjson-remove-broken-method.patch

%if %{with doc}
BuildRequires:	doxygen
%endif
BuildRequires:	gtest-source

BuildSystem:	cmake
BuildOption:	-Wno-dev
BuildOption:	-DRAPIDJSON_BUILD_DOC:BOOL=%{?with_doc:ON}%{?!with_doc:OFF}
BuildOption:	-DRAPIDJSON_BUILD_EXAMPLES:BOOL=ON
BuildOption:	-DRAPIDJSON_BUILD_TESTS:BOOL=ON
BuildOption:	-DRAPIDJSON_BUILD_THIRDPARTY_GTEST:BOOL=OFF
BuildOption:	-DRAPIDJSON_BUILD_CXX11:BOOL=OFF
BuildOption:	-DRAPIDJSON_BUILD_CXX17:BOOL=ON
BuildOption:	-DRAPIDJSON_BUILD_ASAN:BOOL=OFF
BuildOption:	-DRAPIDJSON_BUILD_UBSAN:BOOL=OFF
BuildOption:	-DRAPIDJSON_HAS_STDSTRING:BOOL=OFF
BuildOption:	-DINSTALL_GTEST:BOOL=OFF
BuildOption:	-DLIB_INSTALL_DIR=%{_libdir}
BuildOption:	-DGTEST_SOURCE_DIR=%{_prefix}/src/googletest

%description
RapidJSON is a JSON parser and generator for C++. It was inspired by RapidXml.

- RapidJSON is small but complete. It supports both SAX and DOM style API.
  The SAX parser is only a half thousand lines of code.
- RapidJSON is fast. Its performance can be comparable to strlen(). It also
  optionally supports SSE2/SSE4.2 for acceleration.
- RapidJSON is self-contained and header-only. It does not depend on external
  libraries such as BOOST. It even does not depend on STL.
- RapidJSON is memory-friendly. Each JSON value occupies exactly 16 bytes for
  most 32/64-bit machines (excluding text string). By default it uses a fast
  memory allocator, and the parser allocates memory compactly during parsing.
- RapidJSON is Unicode-friendly. It supports UTF-8, UTF-16, UTF-32 (LE & BE),
  and their detection, validation and transcoding internally. For example, you
  can read a UTF-8 file and let RapidJSON transcode the JSON strings into
  UTF-16 in the DOM. It also supports surrogates and "\u0000" (null character)

%files
%{_includedir}/%{name}/
%{_libdir}/cmake/RapidJSON
%{_libdir}/pkgconfig/RapidJSON.pc
%{_datadir}/doc/RapidJSON/

#---------------------------------------------------------------------------

%prep -a
# Remove -march=native and -Werror from compile commands
find . -type f -name CMakeLists.txt -print0 | \
  xargs -0r sed -i -e "s/-march=native/ /g" -e "s/-Werror//g"
