## Stock Model

This repository implements the Stock Forecasting Model based on research reports of  Huatai Securities.

#### package dependencies

run the following command to install dependencies before running the code: `pip install -r requirements.txt`

#### About Research Reports

The `document/` folder contains more detail about research reports.

#### About data acquisition

We have downloaded some data from Wind, and others will be calculated by ourselves. The data could be access from `data_download/`. This is a whole dataset.

#### About data preparation
###### 1. Handle missing data:
&emsp; For those which have previous records but do not have current records, we use forward fill and backward fill together. <br>
&emsp; For those which do not contain any value throughout our time range, we use the average of values of our stock pool.
###### 2. Label data class:
&emsp; We take two methods to label the data, the one is label the data by sorting the earning rate per month; and the other is mark the stock which has (earning rate > 1.1) as 1, and others as 0.

#### Run sequence
The all .py I have saved in stock_model, this is a temp folder which will be deleted later. And two trained model is in `,ethod1_model/` and `method2_model/`
data_download -> data_prepare -> data_preprocess -> data_price -> data_label -> trainmodel