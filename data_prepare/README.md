## Data Prepare
You should put this .py file under GPSJ folder. It generates .csv files by stock, as well as by feature. In addition, a .txt file which discribes feature is also available.
### Work to Be Completed
#### 1. Data missing 
For some feature, some stock do not even have one piece of data. e.g. For stock 000001.SZ, there is no record for its ROIC data.

About this problem, in machine learning, we have four methods to solve:

&emsp; a. Replace the missing data with median, mode or some other values, but it dostn't work well because we add some noise unexpectedly.

&emsp; b. Create a prediction model by other variables to calculate missing values, but there is a fundamental problem need to solve: In one hand, if other variables are not related to the missing variables, the predicted results are meaningless. In the other hand, if the prediction result is quite accurate, it indicates that this variable is not necessarily added to the model.

&emsp; c. Map variables to high dimensional space. For example, gender, male, female, missing three cases, then mapped into three variables: whether male, female, whether missing. Continuous variables can also be handled this way. The advantage of doing so is to completely retain all the information of the original data, do not consider missing values, and do not consider the problem of linear inseparability. The disadvantage is that the amount of computation is greatly increased.

&emsp; d.Just delete this whole piece of data because we already have a lot of data

  I think finally we will use the method (d), but maybe we can use (b) to restore some data because we have lots of factors and we won't take all of them into our model.

#### 2. Factor Analysis
  Colinearity etc.

#### 3. Other important data, which should be calculated in the future (man man lai ba, md 70 ge yin zi)
