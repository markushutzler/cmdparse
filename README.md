cmdparse - Argparse with Command Support
========================================

comparse is a simple subclass of Python's argparse module to allow 'git style'
commands to be passed to Python applications.



## Code Example

See [example.py](./example.py)

---

`python example.py -h`:

```
usage: example.py [-h]

Test application

optional arguments:
  -h, --help  show this help message and exit

commands:
  test  A test command
  new   A new test command
```
---

`python example.py test -h`:
```
usage: example.py test [-h] [-x]

Test application

A test command

A detailed description of test command displayed if -h is set.

optional arguments:
  -h, --help  show this help message and exit
  -x          Print 3 times x.
```
---

`python example.py test -x`

```
test command called
XXX
```

## Python Requirements

* Tested on Python 2.7

## ToDo

* Python 3 support
* `help` command with man support
* Add setup.py
* Add unit tests

## License

comparse is released under the BSD-3 license. See [LICENSE](./LICENSE) for
more information.
