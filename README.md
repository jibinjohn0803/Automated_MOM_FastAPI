# Automated Minutes of Meeting using AI

This is a project to identify the sentiment of the recorded audio along with converting the audio into text and thereafter summarizing it.

### Prerequisites
You must have Scikit Learn, Pandas (for Machine Leraning Model) and FastAPI (for API) installed.

### Project Structure
This project has three major parts :
1. Text_Summarization.ipynb - Under. ML Build folder, this python code is used to convert audio to text and thereafter generating summary of the same.
2. app.py - This contains Flask APIs that receives crop details through GUI, computes the precited value based on our model and returns it.
4. templates - This folder contains the HTML template to allow user to enter crop details (images as well) to predict ideal crop (or disease identification for images).

### Running the project
As the trained model is already saved in the repository , the model can be downladed in the location where you intend to run this code. After which you will need to do following things:

1. Run app.py using below command to start Flask API (in Pycharm)
```
python app.py
```

Make sure the DecisionModel.pkl, scale.pkl and CNNModel.h5 files are downloaded as well in the same repository

By default, flask will run on port 5000.

3. Navigate to URL http://localhost:5000

You should be able to view the homepage, enter the details and see the results.

Enjoy!!
