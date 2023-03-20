from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 
from django.views.decorators.csrf import csrf_exempt

import joblib
import os
import pandas as pd

base_dir = os.path.dirname(__file__)


# Create your views here.
@csrf_exempt
@api_view(['POST'])
def predict(request, model_name):
    data = request.data["input"]
    input_data = pd.DataFrame({
        'age': data[0],
        'sex': data[1],
        'cp': data[2],
        'trestbps': data[3],
        'chol': data[4],
        'fbs': data[5],
        'restecg': data[6],
        'thalach': data[7],
        'exang': data[8],
        'oldpeak': data[9],
        'slope': data[10],
        'ca': data[11],
        'thal': data[12]
    }, index=range(1)) if model_name == "XGB" else [data]
    load_model = joblib.load(open(base_dir + "/saved_models/" + model_name + ".joblib", 'rb'))
    y_pred = load_model.predict(input_data)
    return JsonResponse(int(y_pred[0]), safe=False)