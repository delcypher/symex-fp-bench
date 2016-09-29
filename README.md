# Floating Point correctness benchmark repository.

Build Status: [![Build Status](https://travis-ci.org/delcypher/fp-bench.svg?branch=master)](https://travis-ci.org/delcypher/fp-bench)

This repository contains a system for organising and building
various benchmarks.

In this system each benchmark is placed in its own folder containings

* Source files
* A benchmark specification file (``spec.yml``)

This system of organisation is fork of https://github.com/delcypher/svcomp-build-mockup

## Benchmark specification file

This [YAML](http://www.yaml.org/) file contains the relevant information for
verifiying and compiling the benchmark.

The schema for these benchmark specification files is written using
[json-schema](http://json-schema.org/) and be found at
[svcb/svcb/schema.yml](svcb/svcb/schema.yml).

Please note that the schema currently isn't finalised.

Having such a format is useful because

* It is clear how benchmarks should be compiled.
* It is clear what properties should be verified/checked for.
* It is easy to gather statistics on the benchmarks.

A key concept to understand with this format is that a `spec.yml` can declare
multiple benchmarks by declaring multiple variants. If no variants are specified
or if there is only one variant the `spec.yml` file only declares a single benchmark.

Having variants is useful for having benchmarks where small changes guarded by macro
definitions create different versions of a benchmark from the same source files.

## Requirements

Before building the benchmarks you will need the following installed:

* A working C and C++ compiler
* [CMake](https://cmake.org/) >= 2.8.12
* [Python](https://www.python.org/) >= 2.7
* [jsonschema](https://pypi.python.org/pypi/jsonschema) and [pyyaml](https://pypi.python.org/pypi/PyYAML) Python modules

Note we provide a `requirements.txt` file for the Python dependencies so you can install these via `pip`.

```
pip install -r requirements.txt
```

If you don't want to install these dependencies globally create a Python virtual environment
by using [virtualenv](https://virtualenv.pypa.io/en/stable/).

## Building benchmarks as native binaries

Here are the basic steps for building the benchmarks.

```
$ mkdir build
$ cd build
$ KLEE_NATIVE_RUNTIME_LIB_DIR=<KLEE_RUNTIME_LIB_DIR> KLEE_NATIVE_RUNTIME_INCLUDE_DIR=<KLEE_RUNTIME_INCLUDE_DIR>  cmake ../
$ make
```

where `<KLEE_RUNTIME_LIB_DIR>` is the directory containing `libkleeRuntest.so` and `<KLEE_RUNTIME_INCLUDE_DIR>` is the
directory containing `klee/klee.h`. You can get and build KLEE from [GitHub](https://github.com/klee/klee).

Note by default it is enforced that the KLEE runtime be available because the majority of the benchmarks will require it.
However you can change this by passing `-DKLEE_NATIVE_RUNTIME_REQUIRED=FALSE` when invoking CMake. Doing this will cause
only the benchmarks that don't need the KLEE runtime.


## Building benchmarks as LLVM bitcode

KLEE can't run native binaries. Instead it runs LLVM bitcode. To build the benchmarks as LLVM bitcode you should follow
the steps above but use [Whole Program LLVM](https://github.com/travitch/whole-program-llvm) as the compiler rather
than your normal host compiler.

The invocation to CMake will probably look something like this:

```
$ export WLLVM_COMPILER=clang
$ mkdir build_llvm
$ cd build_llvm
$ CC=wllvm CXX=wllvm++ KLEE_NATIVE_RUNTIME_LIB_DIR=<KLEE_RUNTIME_LIB_DIR> KLEE_NATIVE_RUNTIME_INCLUDE_DIR=<KLEE_RUNTIME_INCLUDE_DIR>  cmake ../
$ make
```

If the `WLLVM_RUN_EXTRACT_BC` CMake option is set to `TRUE` and CMake detects that wllvm is being used as the compiler then
it will automatically run the `extract-bc` tool on each binary and will output the LLVM bitcode in the same directory as the binary
with a `.bc` suffix. Note `extract-bc` must be in your `PATH`.

If the `WLLVM_RUN_EXTRACT_BC` CMake option is set to `FALSE` you will need to run the `extract-bc` tool manually.

## Running schema tests

```
make check-svcb
```

## Displaying the number of benchmarks by category

```
make show-categories
```

## Displaying the number of verification tasks

```
make show-tasks
```

## Displaying a summary of benchmark correctness

```
make show-correctness-summary
```

## Generate list of augmented spec files

```
make create-augmented-spec-file-list
```

## Benchmark tools

You can find various tools in `svcb/tools/`.

## `category-count.py`

This tool will recursively traverse a specified directory parsing all found `spec.yml` files and reporting the found categories and how
many benchmarks are in each category.

## `correctness-count.py`

This tool will recursively traverse a specified directory parsing all found `spec.yml` files and reporting all the found verification tasks.

## `filter-augmented-spec-list.py`

Filter a list of augented spec files by some criteria.

## `svcb-emit-cmake-decls.py`

A tool for internal use that when given a `spec.yml` file will declare all the targets (i.e. the benchmarks) to be built for the CMake build system.

## `svcb-show-targets.py`

This tool when given a `spec.yml` file will parse it and display all the benchmarks declared by the file. Note there will only be multiple
benchmarks in a `spec.yml` file is multiple variants are declared in it.

## `svcb-emit-klee-runner-invocation-info.py`

This tool when given a file containing of a list of augmented spec files will
generate an invocation info file suitable for use by the [klee-runner](svcb-emit-klee-runner-invocation-info.py)
framework.

## Exporting an invocation info file for the klee-runner framework

The [klee-runner framework](https://github.com/delcypher/klee-runner) consumes
an invocation info file to know how KLEE should run a benchmark. The following
steps can be performed to generate this file after successfully building the
benchmarks.

```
# Create `augmented_spec_files.txt`
make create-augmented-spec-file-list

# Filter the list using `filter-augmented-spec-list.py` (optional)
/path/to/fp-bench/svcb/tools/filter-augmented-spec-list.py --categories examples -- augmented_spec_files.txt > examples.txt

# Generate invocation info file
/path/to/fp-bench/svcb/tools/svcb-emit-klee-runner-invocation-info.py examples.txt > examples_invocation_info.yml
```
