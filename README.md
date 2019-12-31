# Reddit Text Classification

In this project, we considered the problem of classifying the comments into 20 difference subreddits by applying classifiers, including Logistic Regression(LR), Decision Trees, Support Vector Machines, Bernoulli Naive Bayes’, and Multinomial Naive Bayes’. We also experimented with Recurrent Neural Network with the Keras library run on the TensorFlow backend. We investigated how changing the parameters and preprocessing texts can affect the performances of the classifiers. In the end, with the help of Gridsearch for hyperparameter tuning, and model validation pipeline, we found that among all of the classifiers, Support Vector Machines performs the best, while the Decision trees method performs the worst in our environment.

- Training and testing data are stored in the folder: `data`.
- Several models are stored in the folder: `models`
  - Bernouli Naive Bayes 
  - Recurrent Neural Network
  - Support Vector Machine
  - Decision Tree
  - Logistic Regression