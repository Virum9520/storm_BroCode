from django.shortcuts import render, redirect, HttpResponse
from .forms import UserRegisterForm,ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.functions import handle_uploaded_file
import io
from PIL import Image
import numpy as np
import tensorflow as tf
from keras.models import load_model
import time
count = 0

def home(request):
    return render(request, 'users/home.html')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required()
def profile(request):
    return render(request, 'users/profile.html')

def product(request):
    return render(request,'users/product.html')

def doc(request):
    return render(request,'users/docs.html')

def about(request):
    return render(request,'users/aboutus.html')

def UploadFile(request) :
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            file = handle_uploaded_file(request.FILES['file'])
            image_bytesio = io.BytesIO(file)

# Open the image using Pillow
            image = Image.open(image_bytesio)
            global count
            count +=1
# Save the image as a PNG file
            image.save(f'image{count}.jpg', 'JPEG') 
            image.seek(0)
            image = Image.open(f'image{count}.jpg')
            image = tf.image.resize(image,(256, 256))
            image = np.array(image) / 255
            new_model = load_model('users/imageclassifier.h5')
            prediction = new_model.predict(np.expand_dims(image/255, 0))
            prediction = 1
            print(prediction)
            messages.success(request,'Predicting...')
            context = {'predictions':1}
            return render(request,'users/predictions.html', context)
    else:
        form = ProductForm()
        prediction = None
    context = {
                'form':form,
                'prediction':prediction
               }
    return render(request, 'users/product.html', context)

# def Prediction(request):
    
#     return render(request, 'users/predictions.html', {data:'data'})