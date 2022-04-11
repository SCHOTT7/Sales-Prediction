# Sales-Prediction
My attempt to the 'Predict Future Sales' Kaggle competition : https://www.kaggle.com/competitions/competitive-data-science-predict-future-sales/data

## Progress of the Project:

### April 5th 2022:
First version of my data pre-processing. I've identified the most evident issues with this dataset such as sparsity & location variations.

Before going into the model training I have to be sure that I'm totally aware of how RNN works and how to implement them correctly. 
https://towardsdatascience.com/temporal-loops-intro-to-recurrent-neural-networks-for-time-series-forecasting-in-python-b0398963dc1f

### April 7th 2022:
Second version of my data pre-processing. One-hot encodagind of temporal features, daily time lag added.

Data seems to come from mutlimedia stores, meaning that product are DVDs, Blu-rays, video-games, computer, pc, etc.
-> This has huge implications. In fact, GLOBAL sales may be following monthly/yearly trends but, when looking at the product level, sales are highly sparsed in time. 
For example, most sales for a video game are made right after the game comes out.


### April 9-10th 2022:

First attempt predicting future sales using Amazon DeepAR algorithm 
RMSE = 4.48 
