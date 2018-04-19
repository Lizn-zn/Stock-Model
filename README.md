## Stock Model

This repository implements the Stock Forecasting Model based on research reports of  Huatai Securities.

###package dependencies

run the following command to install dependencies before running the code: `pip install -r requirements.txt`

### About Research Reports

The `document/` folder contains more detail about research reports.

### About data acquisition

We have downloaded some data from Wind, and others will be calculated by ourselves. The data could be access from [data](https://pan.baidu.com/s/1x7df0ip4P-1fVL8_p702Cw) and password is 'gksv'. This is a whole dataset.

### About data preparation
#### 1. Handle missing data:
&emsp; For those which have previous records but do not have current records, we use forward fill;
&emsp; For those which do not contain any value throughout our time range, we use the average of values of our stock pool.
#### 2. Label data class: