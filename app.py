import os
import sys
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from src.components.data_ingestion import DataIngestion
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException
from src.logger import logging
import pickle

# Define the input schema
class InputData(BaseModel):
    air_temperature: float
    process_temperature: float
    rotational_speed: int
    torque: float
    tool_wear: int

# Create the app object
app = FastAPI()

# Load the model
with open("artifacts/model.pkl", "rb") as model_file:
    model = pickle.load(model_file)


@app.get("/")
def index():
    return {'message': 'Welcome to the Prediction API!'}


@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    """
    Upload a CSV file and split it into train and test datasets.

    """
    
    try:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

        # Save the uploaded file to 'notebook/dataset/'
        upload_folder = os.path.join("notebook", "dataset")
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        temp_file_path = os.path.join(upload_folder, file.filename)
        with open(temp_file_path, "wb") as f:
            f.write(file.file.read())

        # Use DataIngestion to process the file
        data_ingestion = DataIngestion(file_path=temp_file_path)
        global train_data_path, test_data_path
        train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()

        logging.info("CSV File has been uploaded.")
        return {"message": "File uploaded and train-test split completed successfully."}

    except Exception as e:
        raise CustomException(e,sys)
    

@app.post("/train")
def train_model():
    """
    Train a model using the uploaded dataset.
    """
    try:
        if not train_data_path or not test_data_path:
            raise HTTPException(status_code=400, detail="No data uploaded. Please upload a dataset first.")

        # Use ModelTrainer to train the model
        model_trainer = ModelTrainer()
        global model
        accuracy, f1_score = model_trainer.initiate_model_trainer(train_data_path, test_data_path)

        # Load the trained model for future predictions
        model_path = model_trainer.model_trainer_config.trained_model_file_path
        with open(model_path, "rb") as f:
            model = pickle.load(f)

        logging.info("Prediction has been done.")
        return {"message": "Model trained successfully.", "accuracy": accuracy, "f1_score": f1_score}

    except Exception as e:
        raise CustomException(e,sys)
    


@app.post("/predict")
def predict(data: InputData):
    try:
        if model is None:
            raise HTTPException(status_code=400, detail="Model is not trained. Please train the model first.")
        
        data = data.dict()
        air_temperature = data['air_temperature']
        process_temperature = data['process_temperature']
        rotational_speed = data['rotational_speed']
        torque = data['torque']
        tool_wear = data['tool_wear']

        input_data = [[air_temperature, process_temperature, rotational_speed, torque, tool_wear]]
        
        prediction_probs = model.predict_proba(input_data) 
        
        # Get the predicted class (0: No Failure, 1: Failure)
        predicted_class = model.predict(input_data)[0]
        
        confidence = prediction_probs[0][predicted_class]  
        
        # Map the prediction to labels
        prediction_label = "No Failure" if predicted_class == 0 else "Failure"

        # Return both prediction and confidence
        return {
            'prediction': prediction_label,
            'confidence': round(confidence,4)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {str(e)}")

    


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
