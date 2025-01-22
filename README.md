# Predictive Analysis API Testing with Postman

This guide provides instructions to test API endpoints locally using Postman.

## Prerequisites

1. **FastAPI Application**: Ensure you have a FastAPI app ready for testing.
2. **Postman**: Download and install Postman from [Postman’s website](https://www.postman.com/).

---

## Step 1: Clone the GitHub Repository

Download the FastAPI application from the GitHub repository:

```bash
git clone https://github.com/kashika13/predictive_analysis_api.git
cd predictive_analysis_api
```

The repository contains the following files:
- `setup.py`: Script to install the application as a Python package.
- `app.py`: Main FastAPI application file to start the API server.
- `requirements.txt`: Lists the required Python modules for the project.
- `src/`: Directory containing core modules and logic.
  - `__init__.py`: Marks the folder as a Python package.
  - `data_ingestion.py`: Handles data ingestion processes.
  - `model_trainer.py`: Contains logic for model training.
- `notebook/`: Directory for data exploration and analysis.
  - `notebook.ipynb` Jupyter Notebook used for exploring the dataset.
  - `dataset/`: Folder containing the dataset required for analysis.
    - `data.csv` the dataset used in the application.


## Step 2: Install Dependencies

Install the required dependencies using `setup.py`:

```bash
pip install -e .
```

Ensure all dependencies are successfully installed.

---

## Step 3: Start FastAPI Application

Run your FastAPI application using the following command:

```bash
uvicorn app:app --reload
```

---

## Step 4: Open Postman

1. Install Postman if you haven’t already.
2. Open the Postman application.

---

## Step 5: Test Endpoints

### 1. Test `GET /` (Root Endpoint)

- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/`

#### Steps:
1. Select `GET` from the dropdown menu next to the URL bar in Postman.
2. Enter `http://127.0.0.1:8000/` in the URL field.
3. Click the **Send** button.

#### Expected Response:
```json
{
  "message": "Welcome to the Predictive Maintenance API!"
}
```

![Screenshot 2025-01-22 214942](https://github.com/user-attachments/assets/21f4f6b7-e6c9-4afc-b39e-32cc53a77f9f)


---

### 2. Test `POST /upload` (File Upload Endpoint)

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/upload`
- **Body**: `form-data`

#### Steps:
1. Select `POST` from the dropdown menu.
2. Enter `http://127.0.0.1:8000/upload` in the URL field.
3. Go to the **Body** tab and select `form-data`.
4. Add a key-value pair:
   - **Key**: `file`
   - **Value**: Upload a `.csv` file from your system.
       - Get the csv file from notebook->dataset->predictive_maintenance.csv
       - You can upload your own csv file but make sure that column names and their types remains same as of above dataset.
5. Click the **Send** button.

#### Expected Response:
```json
{
  "message": "File uploaded and train-test split completed successfully."
}
```
![Screenshot 2025-01-22 215036](https://github.com/user-attachments/assets/4215fe3a-725e-4ac6-9961-116dc14e13bc)


---

### 3. Test `POST /train` (Model Training Endpoint)

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/train`

#### Steps:
1. Select `POST` from the dropdown menu.
2. Enter `http://127.0.0.1:8000/train` in the URL field.
3. Click the **Send** button.

#### Expected Response:
```json
{
  "message": "Model trained successfully.",
  "accuracy": 0.85,
  "f1_score": 0.80
}
```
![Screenshot 2025-01-22 215058](https://github.com/user-attachments/assets/8fb4b918-1a25-43a7-9490-679f332573fe)


---

### 4. Test `POST /predict` (Prediction Endpoint)

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/predict`
- **Body**: `raw` JSON

#### Steps:
1. Select `POST` from the dropdown menu.
2. Enter `http://127.0.0.1:8000/predict` in the URL field.
3. Go to the **Body** tab, select `raw`, and choose `JSON` from the dropdown menu.
4. Enter the following sample payload:
   ```json
   {
     "air_temperature": 300.3,
     "process_temperature": 321.5,
     "rotational_speed": 245,
     "torque": 45.6,
     "tool_wear": 3
   }
   ```
5. Click the **Send** button.

#### Expected Response:
```json
{
  "prediction": "Failure"
}
```

![Screenshot 2025-01-22 215449](https://github.com/user-attachments/assets/3ef9b93d-c93a-4058-95ff-8b1e10a17406)

---



