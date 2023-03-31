# There are no files that we can get debug info from
%global debug_package %{nil}

%bcond_without	doc

Name:		rapidjson
Version:	1.1.0
Release:	6
Summary:	A fast JSON parser/generator for C++
Group:		Development/C++
License:	BSD
URL:		https://rapidjson.org/
Source0:	https://github.com/Tencent/rapidjson/archive/v%{version}/%{name}-%{version}.tar.gz
#Patch0:	remove-Werror-cmakelist.patch

BuildRequires:	cmake
BuildRequires:	ninja
%if %{with doc}
BuildRequires:	doxygen
%endif

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
%{_libdir}/cmake/RapidJSON/RapidJSONConfig.cmake
%{_libdir}/cmake/RapidJSON/RapidJSONConfigVersion.cmake
%{_libdir}/pkgconfig/RapidJSON.pc
%{_datadir}/doc/RapidJSON/

#---------------------------------------------------------------------------

%prep
%autosetup -p1

# Remove -march=native and -Werror from compile commands
find . -type f -name CMakeLists.txt -print0 | \
  xargs -0r sed -i -e "s/-march=native/ /g" -e "s/-Werror//g"

%build
%cmake \
	-Wno-dev \
	-DRAPIDJSON_BUILD_DOC:BOOL=%{?with_doc:ON}%{?!with_doc:OFF} \
	-DRAPIDJSON_BUILD_EXAMPLES:BOOL=ON \
	-DRAPIDJSON_BUILD_TESTS:BOOL=ON \
	-DRAPIDJSON_BUILD_THIRDPARTY_GTEST:BOOL=OFF \
	-DRAPIDJSON_BUILD_CXX11:BOOL=ON \
	-DRAPIDJSON_BUILD_ASAN:BOOL=OFF \
	-DRAPIDJSON_BUILD_UBSAN:BOOL=OFF \
	-DRAPIDJSON_HAS_STDSTRING:BOOL=OFF \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

