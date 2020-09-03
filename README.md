# DSC180A_assignment-2

This assignment consists of:

1.  Statistically assessing the quality of the data, justifying the
    data-cleaning logic, and explaining/analyzing the
    features/statistics/target needed for the replication (report).
    
2.  Development and justification of data cleaning (code).

* * * * *

### Part 1

* (Cleaning) Initial EDA is performed to statistically assess the quality of the data
and its appropriateness for addressing the problem at hand, **justifying
data cleaning logic**. This addresses issues with accuracy,
precision, and missingness of specific attributes, tying these issues
to their possible impact over eventual results.

* (Descriptive Stats) The relevant, cleaned attributes are statistically summarize and 
features are derived (e.g. in univariate and bivariate analyses) for San Diego.

* (Traffic Stop Analysis) The differences in
  stop rates and post-stop outcomes are calculate and documented. This analysis addresses
  possible reasons for such differences (including addressing possible
  confounders). Additionally:
      - The significance of these differences is tested using
        statistical inference.
      - These differences are calculated across other
        variables of interest (e.g. service area).
        
* (Veil of Darkness) The Veil of Darkness analysis is performed for San
  Diego. Included is an introduction to the technique and interpretation of the
  results.


### Part 2

Development of the code to clean data (as defined and justified in Part 1),
create the features for the replication, and compute the statistics
for the report. 

In particular, this project contains a `run.py` with the following
targets:
1. `data` creates the data needed for analysis.
2. `process` cleans and prepares the data for analysis (e.g. cleaning
   and feature creation).
3. `data-test` ingests a small amount of *test data* (that `process`
   can then process).

## Usage Instructions

* Description of targets and using `run.py`

## Description of Contents

The project consists of these portions:
```
PROJECT
├── .env
├── .gitignore
├── README.md
├── config
│   ├── data-params.json
│   └── test-params.json
├── data
│   ├── log
│   ├── out
│   ├── raw
│   └── temp
├── lib
├── notebooks
│   └── .gitkeep
├── references
│   └── .gitkeep
├── requirements.txt
├── run.py
└── src
    └── etl.py
```

### `src`

* `etl.py`: Library code that executes tasks useful for getting data.

### `config`

* `data-params.json`: Common parameters for getting data, serving as
  inputs to library code.
  
* `test-params.json`: parameters for running small process on small
  test data.

### `references`

* Data Dictionaries, references to external sources

### `notebooks`

* Jupyter notebooks for *analyses*
  - notebooks are not for data processing; they should import code
    from `src`.
