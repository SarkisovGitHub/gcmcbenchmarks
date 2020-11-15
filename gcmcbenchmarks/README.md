# GCMCbenchmarks


[![DOI](https://zenodo.org/badge/60168211.svg)](https://zenodo.org/badge/latestdoi/60168211)


Python package to accompany the GCMC benchmarking work.
This package includes case studies for GCMC adsorption to verify the accuracy of programs,
as well as analysis tools to quantify the statistical length of MC simulations.

How to install 
--------------

This package requires:

* numpy
* scipy
* pandas
* statsmodels
* docopt

To install and use the Python package run the following commands

```
git clone https://github.com/SarkisovGroup/gcmcbenchmarks.git
cd gcmcbenchmarks
pip install -r requirements.txt .
```


List of supported simulation programs
-------------------------------------

 - Cassandra v1.2
 - DL_Monte2 v2.0.1-2016_May-Beta
 - Music v4.0
 - RASPA v2.0
 - Towhee v7.1.0


Reference system details
------------------------

All of the benchmarks in this package are built around a 2 x 2 x 2 unit cell of IRMOF-1 adsorbent (8 x 424 atoms (3392))
with CO2 adsorbate.

These are modelled at a temperature of 208.0 K and pressures of 5, 10, 20, 30, 40, 50, 60 and 70 kPa.

3 setups of simulations were performed with all software:

 - Setup 1: Only LJ interactions between all components
 - Setup 2: As 1) but with fluid-fluid electrostatics
 - Setup 3: As 2) but with solid-fluid electrostatics

Creating simulations
--------------------

The input files for simulations can be created using the Python `make_*` scripts
in this directory.  The following scripts are available::

 * `make_cassandra_sims.py`
 * `make_dlm_sims.py`
 * `make_music_sims.py`
 * `make_raspa_sims.py`
 * `make_towhee_sims.py`

These generally follow the signature `make_X_sims.py <setup> <destination>` where `<setup>` refers to one of the conditions listed above and `<destination>` refers to the
directory in which they will be made.

For example:

`make_raspa_sims.py setup2 rsp_sims_setup2 -n 10000000`

Makes a set of Raspa simulations for all pressures in the directory "`rsp_sims_setup2`",
with a length of 10M steps.

Full details of the available options are detailed in the `-h` option for each script.
