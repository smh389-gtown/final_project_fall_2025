import random
import requests
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt




load_dotenv() # loads environment variables from the ".env" file

TMDB_API_KEY = os.getenv("TMDB_API_KEY")


page_number = random.randint(1, 500)

movie_number = random.randint(0, 19)



url = f"https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={page_number}&api_key={TMDB_API_KEY}"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

movie_list = response.json()

movie_list = movie_list["results"]


poster_path = movie_list[movie_number]["poster_path"]
full_url = f"https://image.tmdb.org/t/p/w500{poster_path}"

response = requests.get(full_url)
img = Image.open(BytesIO(response.content))

plt.imshow(img)
plt.axis("off")
plt.show()


print(movie_list)

