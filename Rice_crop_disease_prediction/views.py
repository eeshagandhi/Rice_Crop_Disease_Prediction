from django.http import HttpResponse
from django.shortcuts import render
import joblib


from skimage.io import imread
from skimage.transform import resize
import skimage
from PIL import Image
import os

def load_image(file):
    dimension=(104, 104)
    image = Image.open(file)
    flat_data = []
    img = skimage.io.imread(file)
    img_resized = resize(img, dimension, anti_aliasing=True, mode='reflect')
    flat_data.append(img_resized.flatten()) 
    return image,flat_data

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def predict_disease(request):
    return render(request, "predict_disease.html")

def disease_sev(request):
    return render(request, "disease_sev.html")

def result(request):
    clf=joblib.load("final_model.sav")
    plot , img = load_image(request.FILES['image'])
    ans=clf.predict(img)
    if ans==0:
        ans="Healthy"
        sol="None"
    elif ans==1:
        ans="Blast"
        sol="Spray Tricyclazole75 0.6g/litre"+"\n"+"Isoprothiolane 40 EC 1.5ml/litre"
    elif ans==2:
        ans="BrownSpot"
        sol="Mancozeb 75 WP 2.5 g/litre"+"\n"+"Carbendazim 50 WP 2 g/kg"
    elif ans==3:
        ans="Tungro"
        sol="Incorporate Phorate 10 G @ 12-15 kg/ha"+"\n"+"Fipronil 0.4 G @ 25 kg/ha"
    else:
        ans="Bacterial Leaf Blight"
        sol="None"
    #context={'The disease is':ans,'The solution is':sol}
    disease={'name':ans, 'solution':sol}
    context={
        'disease':disease,
    }
    return render(request, "result.html",context)







