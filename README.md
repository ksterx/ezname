# ezname

A simple tool for generating random, memorable names - better than UUIDs

## Overview

`ezname` is a Python tool that generates random, human-readable names that are much more memorable than UUIDs or timestamps. Use them for experiments, temporary resources, projects, or anywhere you need a distinctive identifier.

## Installation

```bash
pip install ezname
```

## Usage

- Python

```python
import ezname

ezname.generate()
# happy-friday

ezname.generate(prefix="run", suffix="v1.0", delimiter="_")
# run_sleepy_penguin_v1.0

ezname.generate(as_tuple=True)
# ("bad", "cop")

ezname.generate_batch(3)
# ['desirable-none', 'old-code', 'troublesome-rod']
```

- Terminal

```bash
$ ezname
>> witty-calculator
```

## Features

- Generates names that are easy to pronounce and understand
- Provides customizable naming options with prefixes, suffixes, and delimiters
- Supports tuple output format for structured naming

## License

MIT License
