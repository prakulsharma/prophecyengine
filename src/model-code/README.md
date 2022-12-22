# anomaly-detection-engine
Anomaly detection engine is an analytic to detect outlier in given multivariate timeseries dataset.
Analytic work as semi-supervised learning using ensemble of machine learning algorithm listed below
- PCA
- KNN
- Autoencoder 
- OCSVM (Only to be used with less training data)

# Training the model
Training dataset should be carefully crafted where data-set shows normal behavior (No outlier in 
the training data)
- Use 'src/train.py' file to train the model.A csv filepath can be specified for reading the training data 

# Scoring the model
Scoring of model can be done executing  'src/score.py'. scoring data can be read using csv file locally

# Configuration File
'src/config/config.yaml' should be created using config.yaml.template with placeholder replaced.
See 'src/config/config.yaml.template' file comments for more details of parameters

# Thresholding and Normalization of Anomaly Score
configuration file "config.yaml" contains parameters 'norm_flag' and 'threshold'
'threshold' is project specific and to be set with some trial and error. This is avearge of score above which 
process should be considered anomalous. Default could be set around 1.2*Number of methods used
'norm_flag' set as '1' will enable normalization of anomaly score where threshold score will be set as 1
Note that anomaly score values are clipped at 10. Hence anomaly score value can be 0-10 with value more than 1
will be considered anomalous
# Environment variable setup
path of the folder where trained model will be saved should be added in local environment variable

TRAINING_OUTPUT_PATH = path of the folder where model is saved  

# Chennel Creation requirement
This project requires creation of two channels with key "alert_indicator", and "anomaly_threshold" apart from anomaly_score in the asset of interest
These channels must be added to the analytic output interface

# Virtual Environment Setup
-   Create virtual environment

        mkvirtualenv -p `which python3.6` ade
 

-   Install dependencies: Create pip.conf from pip.conf.template with placeholders replaced
    
        export PIP_CONFIG_FILE=pip.conf
        pip install -r requirements.txt --extra-index-url https://pypi.python.org/simple


