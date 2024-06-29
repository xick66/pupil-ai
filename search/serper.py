from dotenv import load_dotenv
import json
import os
import requests

load_dotenv()

class Serper():
  def __init__(self):
    self.API_KEY = os.environ.get("SERPER_API_KEY")
    self.SEARCH_URL = "https://google.serper.dev/search"
    self.IMAGES_URL = "https://google.serper.dev/images"
    self.VIDEOS_URL = "https://google.serper.dev/videos"
    self.PLACES_URL = "https://google.serper.dev/places"
    self.MAPS_URL = "https://google.serper.dev/maps"
    self.NEWS_URL = "https://google.serper.dev/news"
    self.SHOPPING_URL = "https://google.serper.dev/shopping"
    self.SCHOLAR_URL = "https://google.serper.dev/scholar"
    self.AUTOCOMPLETE_URL = "https://google.serper.dev/autocomplete"
    self.params = {
      "gl": "EN", # country
      "hl": "EN", # locale
      "location": "United Kingdom",
      "num": 20,
      "page": 1,
    }

  def get_domain(self, url: str) -> str:
    http = 'http://'
    https = 'https://'
    if url.startswith(http):
      return url[len(http)]
    elif url.startswith(https):
      return url[len(https):]
    return url

  def get_urls(self, query: str) -> [str]:
    urls = re.findall(
      r'(?:https?://)?(?:www\.)?[\w.-]+\.\w\w+\b',
      query)
    return urls

  def search(self, query, **kwargs):
    payload = json.dumps({
      "q": query,
      **self.params,
      **kwargs,
    })
    headers = {
      'X-API-KEY': self.API_KEY,
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", self.SEARCH_URL, headers=headers, data=payload)
    return response.json()

  def get_answer(self, query, **kwargs) -> str|None:
    resp = self.search(query=query)
    return resp["answerBox"]["answer"] if "answerBox" in resp and "answer" in resp["answerBox"] else None



if __name__ == "__main__":
  serper = Serper()
  response = serper.search(query="what does 1 + 1 equal to?")
  print(response["answerBox"])
  print(response["answerBox"]["answer"])

  response = serper.get_answer(query="what does 1 + 1 equal to?")
  print(response)
  response = serper.get_answer(query="asdf")
  print(response)
