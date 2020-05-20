# Cyclone DDS Python API

## Overview
**cdds-python** is a simple Python API for [Cyclone DDS](https://github.com/eclipse-cyclonedds/cyclonedds#getting-started)

This API supports:

- **IDL-based Topic Types**. In this case the equivalent python type 
  has to be defined using the appropriate ctype structure.
  
- **Python Objects**. Python objects can be used as Topic types, in this
  case the wire representation is that of flexy-types, meaning a 
  key/value pair.
  
Regardless of the kinds of type definition interoperability and instance management are maintained (see code examples).

## Installation
**pydds** depends on:

- [**jsonpickle**](https://github.com/jsonpickle/jsonpickle), please refer to the project page for installation informations.

- [**Cyclone DDS**](https://github.com/eclipse-cyclonedds), refer to the installation instructions to see how to get it set up.
as
Once the dependencies are intalled simply do (assuming your are running on Linux):

```
$ cd python-cdds
$ ./configure
$ python3 setup.py install 
```


The setup my requires admin rights on some plartforms.

To test your installation do:


	$ python3 test_flexy_writer.py 
	$ python3 test_flexy_reader.py 





 
