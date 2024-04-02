![Build Status](https://github.com/drummondj/configtree/actions/workflows/main.yml/badge.svg?subject=build)
![Coverage](coverage.svg)

# ConfigTree

ConfigTree is a configuration management system that uses inheritance based on a hierarchical tree structure. It is intended to be used in complex scientific and engineering data flows, where the flow is developed separately from the configuration and execution of the flow.

`Schema` is a list of variables used to configure a flow, along with their default values, datatypes and possible options. Variables can be grouped into categories to make it easier to handle large configurations.

`Config` is an instance of a `Schema` that the end-user can edit to customize how the flow works.

The underlying data is stored in JSON files which can be managed by your favorite version control system, such as GIT.

ConfigTree provides a locally hosted webserver to enable the flow developers to edit Schemas and the end-users to edit Configs, without the need to edit JSON files directly. 


## Installation

Runs on Ubuntu, assumes you have sudo access and python3 is already on your path:

```
make install
```

This will install the `python3-tk` library plus all the python packages from `environment/requirements.txt`.

For other operating systems, please see the `Makefile` `install` target for a list of commands and modify as approriate.



