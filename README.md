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
- `setup.py`: For installing the application as a package.
- `app.py`: The main FastAPI application file.
- 

---

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
5. Click the **Send** button.

#### Expected Response:
```json
{
  "message": "File uploaded and train-test split completed successfully."
}
```

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
     "air_temperature": 30.5,
     "process_temperature": 75.2,
     "rotational_speed": 1500,
     "torque": 2.3,
     "tool_wear": 12
   }
   ```
5. Click the **Send** button.

#### Expected Response:
```json
{
  "prediction": "Failure"
}
```

---



