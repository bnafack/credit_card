# Credit Card Fraud Detection

## Approach used
The dataset we used was already clean with no missing data. Therefore, we chose XGBoost as our base model for the modelling phase. XGBoost is insensitive to feature scaling and outliers, so we didn't need to worry about them in the dataset. 

After that, we split the dataset into 10% for testing and 90% for training using the train_test_split method. We then employed the GridSearchCV technique for hyperparameter tuning to find the optimal hyperparameters for XGBoost within a specified grid of parameter values. We set 'n_jobs' to 10 to leverage multithreading for enhanced parallel computation. 

Once we got the optimal parameters from the grid search, we used those parameters to train different data-centric models for imbalanced, unsampled, and downsampled datasets on train dataset. Before performing upsampling/downsampling, we split the dataset into train and test datasets to prevent data leakage.

After the fitting step, we selected the best model with a higher Area Under the Precision-Recall Curve (AUPRC) value indicating better performance in terms of both precision and recall. We stored that model in a pickle file.

NB: At each step, I use the seed for reproductibility.


## Running and model testing

* In order to execute this project, ensure that Python 3 is installed on your machine along with all the necessary packages listed in the `requirements.txt` file. These packages can be installed by following the provided instructions ` pip install -r requirements. txt`. 

* To replicate the experiment, execute the Jupyter Notebook named `credit_fraud_detection.ipynb`.

* For model testing, utilize the final block in the aforementioned notebook. Alternatively, from your development environment,  run the command `python prediction.py directory_to_test_dataset`, where `directory_to_test_dataset` is the path to the test dataset (e.g., `python prediction.py dataset/test_dataset.csv`). The resulting output will be stored in the `output` folder in CSV format. 




# Deployement
The dataset contains information on transactions that took place during two days around 285,299 transactions. To handle this high volume of transactions request, deploying the model using Kubernetes (k8s) is a reasonable choice compare to docker-compose. This decision is based on the need to improve the scalability of the model deployment and ensure efficient handling of the high transaction load. Additionally, using Kubernetes enables seamless updates to the deployed model in a production environment, making it easy and reliable to maintain and improve the model over time.

Our deployment architecture (`system_designe.pdf`) follows a comprehensive approach where the client starts a transaction request by providing transaction information. The bank system, which serves as the initial point of contact, forwards this request to the model via the Nginx Plus web server. Nginx Plus interfaces communicate with the application via uWSGI such the the server web with no direct access to the apps/model. Once the request is received by uWSGI, the Flask application is triggered to meticulously examine the provided information through the Machine learning model to determine whether the transaction is fraudulent or non-fraudulent. The Flask app then communicates the result back to the bank in JSON format via the designated communication protocol.

Our network utilizes a load balancer to optimize resource utilization and enhance system reliability. This load balancer dynamically allocates computation resources and manages the deployment of pods. If a pod is shut down, the load balancer takes responsibility for replacing it. Moreover, the load balancer efficiently delegates tasks to worker nodes available, ensuring continuous operations even when certain nodes are temporarily unavailable, this helps to avoid the crash of the system. This intricately designed deployment architecture guarantees robustness, scalability, and resilience in processing vast numbers of transaction requests.
