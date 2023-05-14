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
        [48.586773, -107.802121],
        [48.415872, -107.836715],
        [52.004794, -106.804044],
        [43.574346, -79.573363],
        [43.571244, -79.574720],
        [43.569942, -79.577262],
        [43.570136, -79.568010],
        [43.571623, -79.584946],
        [43.582261, -79.591414],
        [43.566270, -79.612333],
        [43.545537, -79.600272],
        [43.563424, -79.627759],
        [85.403445, 27.649790],
        [85.516931, 27.676529],
    ]
    start_p = "85.403445,27.649790,"
    end_p = "85.516931,27.676529"
    url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248f2b95ebb2fcc45cfb91bae62c6b3735c&start={start_p}&end={end_p}"
    result = requests.get(url)
    # print(result.json())
    way_coordinates = result.json()["features"][0]["geometry"]["coordinates"]

    map = folium.Map(
        location=[43.5717165, -79.5715712],
        tiles="OpenStreetMap",
        zoom_start=14,
        width="100%",
        height="100%",
    )

    for coordinate in coordinates:
        folium.Marker(coordinate).add_to(map)

    folium.PolyLine(
        locations=[list(reversed(coord)) for coord in way_coordinates], color="blue"
    ).add_to(map)

    # rendering map html
    map = map._repr_html_()
    return map


@csrf_exempt
def home(request):
    m = make_maps()
    if request.method == "POST":
        # print(request.FILES["image"])
        img_file = request.FILES["image"]
        # but i like this way
        with open("static/images/uploaded_image.jpg", "wb") as f:
            f.write(img_file.read())

        query_result = query("static/images/uploaded_image.jpg")
        # print(query_result[0]["label"])
        # print(query_result)

        context = {
            "classified": query_result[0]["label"],
            "m": m,
        }
        return render(request, "home.html", context)

    return render(request, "home.html", {"m": m})


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


@csrf_exempt
def loc(request):
    if request.method == "POST":
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        locality = request.POST.get("locality")
        city = request.POST.get("city")

        # Do something with the latitude and longitude data

        print(latitude, longitude, locality, city)
    return render(request, "loc.html")
