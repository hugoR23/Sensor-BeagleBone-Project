## Installation

```
    virtualenv .
    bin/python setup.py develop
```

## Testing

```
The tests should be launched from the BeagleBone (from its directory python3) from one side and on the local computer from the other side (otherwise lots of tests will be skipped)
    nosetests -v
```