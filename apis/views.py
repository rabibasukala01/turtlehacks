from PIL import Image
from django.shortcuts import render
from django.http import JsonResponse
import folium
import requests
from django.views.decorators.csrf import csrf_exempt

from django.core.files.storage import FileSystemStorage

API_URL = "https://api-inference.huggingface.co/models/yangy50/garbage-classification"
headers = {"Authorization": "Bearer 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"}


# model
def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()


# --------------------------------


# Create your views here.
def make_maps():
    coordinates = [
        [27.705194, 85.391806],
        [27.649790, 85.403445],
        [27.676529, 85.516931],
    ]

    map = folium.Map(
        location=[27.705194, 85.391806],
        tiles="OpenStreetMap",
        zoom_start=14,
        width="50%",
        height="50%",
    )
    for coordinate in coordinates:
        folium.Marker(coordinate).add_to(map)
    # folium.Marker(coordinate, popup="lmao", tooltip="click").add_to(map)

    # rendering map html
    map = map._repr_html_()
    return map

@csrf_exempt
def home(request):
    m = make_maps()
    if request.method == "POST":
        # print(request.FILES["image"])
        img_file = request.FILES["image"]
        #but i like this way
        with open("static/images/uploaded_image.jpg", "wb") as f:
            f.write(img_file.read())

        query_result = query("static/images/uploaded_image.jpg")
        # print(query_result[0]["label"])
        print(query_result)

        context={
            
            "classified":query_result[0]["label"],
            "m": m,
        
        }
        return render(request, "home.html",context)

    return render(request, "home.html",{"m": m})





# @csrf_exempt
# def upload_image(request):
#     if request.method == "POST":
#         # print(request.FILES["image"])
#         img_file = request.FILES["image"]

#         # we can do this too
#         # fs = FileSystemStorage(location="static/images/")
#         # image_name = fs.save("uploaded_image.jpg", img_file)
#         # img_file.save("static/images/uploaded_image.jpg")

#         #but i like this way
#         with open("static/images/uploaded_image.jpg", "wb") as f:
#             f.write(img_file.read())

#         query_result = query("static/images/uploaded_image.jpg")
#         print(query_result[0]["label"])

#         context={
#         "classified":query_result[0]["label"]
#         }
#         return render( request, "upload_image.html",context) 

#     return render(request, "upload_image.html")
