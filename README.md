# pylot16

Tool to predict class labels of TiMBL data and evaluate the prediction.

#### How to use
	usage: main.py [-h] -f test_file -t train_file [-sep [sep]] [-n [neighbours]]
	
	Diminutive predictor and evaluator
	
	optional arguments:
	  -h, --help       show this help message and exit
	  -f test_file     path to a test file with data
	  -t train_file    path to a train file with data
	  -sep [sep]       specifies the seperator the data file uses for its items (default=",")
	  -n [neighbours]  specifies how many neighbours should be used in calculating
	                   a best match (default="1")

#### Example output
```sh
Some statistics:
	 Number of items: 950
	 Number of features: 13
	 Unique class labels (relative proportion):
		 1 	 E (100/950 (11%))
		 2 	 J (352/950 (37%))
		 3 	 K (16/950 (2%))
		 4 	 P (27/950 (3%))
		 5 	 T (455/950 (48%))
		 
Evaluation statistics:
	 Average number of correct predictions: 0.85 (808/950)
		 Class label (correct/total (%))
			 T (437/455 (96%))
			 J (293/352 (83%))
			 E (57/100 (56%))
			 K (9/16 (56%))
			 P (12/27 (44%))
```



### Requirements

* distance package (https://pypi.python.org/pypi/Distance/)
