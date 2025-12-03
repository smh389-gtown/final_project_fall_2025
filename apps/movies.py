import random
import requests
import os
from dotenv import load_dotenv

load_dotenv() # loads environment variables from the ".env" file

TMDB_API_KEY = os.getenv("TMDB_API_KEY")


page_number = random.randint(1, 500)

movie_number = random.randint(0, 19)



url = f"https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={page_number}&api_key={TMDB_API_KEY}"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

movie_list = response.json()

movie_list = movie_list["results"]

print(movie_list)