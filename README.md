# Reddit Text Classification

In this project, we considered the problem of classifying the comments into 20 difference subreddits by applying classifiers, including Logistic Regression(LR), Decision Trees, Support Vector Machines, Bernoulli Naive Bayes’, and Multinomial Naive Bayes’. We also experimented with Recurrent Neural Network with the Keras library run on the TensorFlow backend. We investigated how changing the parameters and preprocessing texts can affect the performances of the classifiers. In the end, with the help of Gridsearch for hyperparameter tuning, and model validation pipeline, we found that among all of the classifiers, Support Vector Machines performs the best, while the Decision trees method performs the worst in our environment.

- Training and testing data are stored in the folder: `data`.

- In Bernouli_Bayes.py, we implement it from scratch.
- In Sklearn_models.py, we use the following packages:
  - pandas, sklearn, nltk
- In RNN.py, we use the following packages:
  - pandas, keras, sklearn
