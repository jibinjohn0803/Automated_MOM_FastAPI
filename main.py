import os
import traceback
import sys
from datetime import datetime, date

import shutil
from werkzeug.utils import secure_filename
from typing import Optional
import wave
from MOM_App import predictMOM

import uvicorn
from fastapi import FastAPI, Request, Response, Depends, File, UploadFile, Cookie, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

# CONSTANT VARIABLES
UPLOAD_FOLDER = 'files\\uploaded'
ALLOWED_EXTENSIONS = set(['wav'])

# APP CONFIG
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

def allowed_file(filename):
	# Build the filename + extension after checking if allowed
	# Note: \ == explicit line continuation
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get('/')
async def home(request: Request,response: Response, response_class=HTMLResponse):
	return templates.TemplateResponse("index.html",{"request":request,"response":response})

@app.post('/upload')
async def upload(request: Request, response: Response, file: UploadFile = File(...),
		   response_class=HTMLResponse):
	enableProcessBtn = False
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		ip_address = str(request.client.host).replace(".","_")
		filename = "{}_{:%Y_%m_%d_%H_%M_%S}_{}".format(ip_address,datetime.now(),file.filename)
		fileLoc = os.path.join(UPLOAD_FOLDER, filename)
		with open(fileLoc, "wb") as buffer:
			shutil.copyfileobj(file.file, buffer)
		print("saved file :",fileLoc)
		enableProcessBtn = True
		message = "Success : audio file has been uploaded"
	else:
		fileLoc = ""
		enableProcessBtn = False
		message = "Error : File format not allowed"
	return templates.TemplateResponse("index.html", {"request": request, "response": response,
													 "message":message,"enableProcessBtn":enableProcessBtn,"fileLoc":fileLoc})

@app.post('/saveRecord')
def saveRecord(request: Request, response: Response, file: UploadFile = File(...),
		   response_class=HTMLResponse):
	enableProcessBtn = False
	message = ""
	fileLoc = ""
	try:

		print(file.filename)
		filename = "recording.wav"
		ip_address = str(request.client.host).replace(".","_")
		filename = "{}_{:%Y_%m_%d_%H_%M_%S}_{}".format(ip_address, datetime.now(), filename)
		fileLoc = os.path.join(UPLOAD_FOLDER, filename)
		audio = wave.open(fileLoc, 'wb')
		audio.setnchannels(1)
		audio.setsampwidth(1)
		audio.setframerate(8000)
		audio.setnframes(1)
		audio.writeframes(file.file.read())
		audio.close()
		print("saved file :", fileLoc)
		fileLoc1 = os.path.join(UPLOAD_FOLDER, "ORG_{}".format(filename))
		with open(fileLoc1, "wb") as buffer:
			shutil.copyfileobj(file.file, buffer)
		print("saved file :", fileLoc1)
		enableProcessBtn = True
		message = "Success : audio recording has stopped and file has been saved"
		return templates.TemplateResponse("index.html", {"request": request, "response": response,
														 "message": message, "enableProcessBtn": enableProcessBtn,
														 "fileLoc": fileLoc})
	except Exception as e:
		enableProcessBtn = False
		message = "Error : {}".format(e)
		fileLoc = ""
		print("Exception",e)
		print(traceback.format_exc())
		return templates.TemplateResponse("index.html", {"request": request, "response": response,
													 "message": message, "enableProcessBtn": enableProcessBtn,
													 "fileLoc": fileLoc})

@app.post('/processMOM')
def processMOM(request: Request, response: Response, fileLoc : str = Form(...),
		   response_class=HTMLResponse):
	print("Inside processMOM with file location :",fileLoc)
	resultSummaryText = ""
	resultSentimentText = ""
	message = ""
	resultFullText = ""
	try:
		resultSummaryText, resultSentimentText, resultFullText = predictMOM(fileLoc)
		print("resultFullText : ", resultFullText)
		print("resultSentimentText : ", resultSentimentText)
		print("resultSummaryText : ", resultSummaryText)
		fileLoc = ""
		message = "Success : processed the audio"
		return templates.TemplateResponse("index.html", {"request": request, "response": response,
														 "message": message, "resultSentimentText": resultSentimentText,
														 "resultSummaryText": resultSummaryText,
														 "resultFullText": resultFullText, "fileLoc": fileLoc})

	except Exception as e:
		print("Exception : ",e)
		print("resultFullText : ", resultFullText)
		print("resultSentimentText : ", resultSentimentText)
		print("resultSummaryText : ", resultSummaryText)
		fileLoc = ""
		message = "Error : {}".format(e)
		return templates.TemplateResponse("index.html", {"request": request, "response": response,
														 "message": message, "resultSentimentText": resultSentimentText,
														 "resultSummaryText": resultSummaryText,
														 "resultFullText": resultFullText, "fileLoc": fileLoc})

if __name__ == '__main__':
   uvicorn.run("main:app")