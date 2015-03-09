STRP Project back-end
=======

This repository holds the back-end for the FHICT Delta STRP project 2015. The logic for the clustering of entities and the behaviour of the entities and clusters is part of the back-end.

[![Build Status](https://travis-ci.org/ldebruijn/STRP.svg?branch=dev)](https://travis-ci.org/ldebruijn/STRP)

Requirements
------------

To run this project, the following software and libraries are required:
* Python 3.x
* Scikit Learn 0.15
* Numpy 1.9.1
* MatPlotLib 1.4.3


ToDo
----

* Wait for the input group to determine what their input to us will look like
* Transform input to a format which yields the best results for our algorithm
* Temper with the input data every now and then to simulate a living ecosystem
* Have a buffer of algorithms where each buffer item represents a state in the ecosystem. This buffer will be used to allow the front-end to simulate movement for entities between two states.
* Output the results of our algorithm somewhere.


Data Input
----------

The below JSON will be the format in which we receive input data.

{ 
	"profiles" : [
		{ 
		  "1" : true, 
		  "2" : false,  
		  "3" : true, 
		  "4" : false, 
		  "5" : true, 
		  "6" : false, 
		  "7" : false, 
		  "hb" : 160 , 
		  "c1" : "ff0000", 
		  "c1" : "ff0000", 
		  "c1" : "ff0000", 
		  "c1" : "ff0000", 
		  "c1" : "ff0000" 
		}
	]
}

Each entity represents a sensor with it's given output data.


Data Output
-----------

The below JSON will be the format in which we output our calculations.

```
{
	"timestamp": 1,
	"nodes": [
		{
			"userId": 1,
			"input_data": [],
			"cluster": 3,
			"position": [3, 4]
		},
		{
			"userId": 2,
			"input_data": [],
			"cluster": 6,
			"position": [16, 3]
		}
	],
	"clusters": [ 
		{
			"1": [20, 24],
			"2": [14, 7]
		}
	]

}
```

* The timestamp is incremental and will be used to keep track of the different stages of the ecosystem
* The `nodes` array will contain all data about an individual node. 
   * `userId` is a unique identifier of which user the node represents.
   * the `input_data` contains the data we got as input.
   * `cluster` is the identifier for which cluster the node belongs to
   * `position` contains an [x, y] coördinate for the position of the node in the ecosystem
* `clusters` contains an array with each cluster position. The label represents the cluster number used in the `nodes` data.