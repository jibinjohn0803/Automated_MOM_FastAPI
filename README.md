# Automated Minutes of Meeting using AI

This is a project to create a summary text of an uploaded (recorded) audio and also capturing the emotion of the speaker and predicting the overall sentiment.

### Prerequisites
You must have Scikit Learn, Pandas (for Machine Leraning Model) and FastAPI (for API) installed.

### Project Structure
This project has three major parts :
1. Text_Summarization.ipynb - Under ML Build folder, this python code is used to convert audio to text and thereafter generating summary of the same.
2. MOM using AI.ipynb -  Under ML Build folder, this code showcases how the model was developed and saved which was finally used in main.py file.
4. templates - This folder contains the HTML template to allow user to enter crop details (images as well) to predict ideal crop (or disease identification for images).

### Running the project
As the trained model is already saved in the repository , the model can be downladed in the location where you intend to run this code. After which you will need to do following things:

1. Run main.py using below command to start FastAPI (in Pycharm)
```
python main.py
```

Make sure the ModelCNN.h5, scale.pkl and MOM_App.py files are downloaded as well in the same repository

By default, fastapi will run on port 8000.

3. Navigate to URL http://localhost:8000

You should be able to view the homepage, enter the details and see the results.

Enjoy!!
