import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os


load_dotenv() # loads environment variables from the ".env" file
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

url = f"https://api.themoviedb.org/3/movie/now_playing?originallanguage=en&page=1&api_key={TMDB_API_KEY}"

response = requests.get(url)

movie_now_list = response.json()

##movie_now_list = movie_now_list["results"]

for movie in movie_now_list["results"]:
    if movie["original_language"] == "en":
        print(movie["title"])
        poster_path = movie["poster_path"]
        full_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        response = requests.get(full_url)
        img = Image.open(BytesIO(response.content))
        plt.imshow(img)
        plt.axis("off")
        plt.show()
