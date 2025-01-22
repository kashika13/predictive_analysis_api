import os
import sys
import pickle
from dataclasses import dataclass
import pandas as pd


from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,precision_score, recall_score, f1_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
from src.logger import logging


@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_data_path,test_data_path):
        try:
            train_df=pd.read_csv(train_data_path)
            test_df=pd.read_csv(test_data_path)

            logging.info("Reading of train and test data completed")

            X_train,X_test,y_train,y_test=(
                                            train_df.drop(columns=['Target','Failure Type','UDI','Product ID','Type'],axis=1),
                                            test_df.drop(columns=['Target','Failure Type','UDI','Product ID','Type'],axis=1),
                                            train_df['Target'],
                                            test_df['Target']
                                        )
            
            logging.info("Training and Testing dataframe formed.")

            clasifier=DecisionTreeClassifier()
            logging.info(f"Model trained.")
            param={
                'criterion':['gini', 'entropy', 'log_loss'],
                'splitter':['best', 'random'],
                'max_depth':[1,2,3,4,5],
                'max_features':['sqrt','log2'],
            }

            grid=GridSearchCV(clasifier,param,cv=3)
            grid.fit(X_train,y_train)

            clasifier.set_params(**grid.best_params_)
            clasifier.fit(X_train,y_train)

            logging.info(f"Hyperparameter Tuning performed on the model.")

            file_path=self.model_trainer_config.trained_model_file_path
            dir_path = os.path.dirname(file_path)
            os.makedirs(dir_path, exist_ok=True)
            with open(file_path, "wb") as file_obj:
                pickle.dump(clasifier, file_obj)

            y_predicted=clasifier.predict(X_test)

            model_test_accuracy = accuracy_score(y_test, y_predicted) # Calculate Accuracy
            model_test_f1 = f1_score(y_test, y_predicted, average='weighted') # Calculate F1-score

            return model_test_accuracy,model_test_f1


        except Exception as e:
            raise CustomException(e,sys)
            

