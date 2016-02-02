# SV-COMP benchmark build mock up

This repository contains a draft design for organising and building
SV-COMP's C benchmarks.

In this system each benchmark is placed in its own folder containings

* Source files
* A benchmark specification file (``spec.yml``)

## Benchmark specification file

This [YAML](http://www.yaml.org/) file contains the relevant information for
verifiying and compiling the benchmark.

The schema for these benchmark specification files is written using
[json-schema](http://json-schema.org/) and be found at
[svcb/schema.yml](svcb/schema.yml).

Please note that the schema currently isn't finalised

# Running schema tests

```
make check-svcb
```

# Buidling benchmarks

TODO
