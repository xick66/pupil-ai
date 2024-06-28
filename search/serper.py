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
  # print(serper.search(query="site:https://codeforces.com/problemset/problem/1929/A"))
  response = serper.search(query="what does 1 + 1 equal to?")
  print(response["answerBox"])
  print(response["answerBox"]["answer"])

  response = serper.get_answer(query="what does 1 + 1 equal to?")
  print(response)
  response = serper.get_answer(query="asdf")
  print(response)

# allintitle: google one OR two "australia" -bukan site:codeforces.com filetype:pdf 1..3

# https://www.google.com/complete/search?q=allintitle%3A%20google%20one%20OR%20two%20%22australia%22%20-bukan%20site%3Acodeforces.com%20filetype%3Apdf%201..3&cp=0&client=gws-wiz-serp&xssi=t&gs_pcrt=3&hl=en-ID&authuser=0&pq=allintitle%3A%20google%20one%20OR%20two%20%22australia%22%20-bukan%20site%3Acodeforces.com%20filetype%3Apdf%201..3&psi=x5AjZq2EOuOO4-EPhNWk4AM.1713606856856&dpr=1&ofp=EAE
# https://www.google.com/complete/search?q&cp=0&client=gws-wiz-serp&xssi=t&gs_pcrt=2&hl=en-ID&authuser=0&pq=allintitle%3A%20google%20one%20OR%20two%20%22australia%22%20-bukan%20site%3Acodeforces.com%20filetype%3Apdf%201..3&psi=x5AjZq2EOuOO4-EPhNWk4AM.1713606856856&dpr=1&nolsbt=1
# https://www.google.com/search?q=allintitle%3A+google+one+OR+two+%22australia%22+-bukan+site%3Acodeforces.com+filetype%3Apdf+1..3&lr=lang_id&cr=countryAU&sca_esv=dc237e1a21ded4e7&sca_upv=1&tbs=sur%3Af%2Cqdr%3Ay%2Clr%3Alang_1id%2Cctr%3AcountryAU&ei=vZAjZsuWK-iQ4-EPnM6_qAQ&ved=0ahUKEwiL6cr6wtCFAxVoyDgGHRznD0UQ4dUDCBA&uact=5&oq=allintitle%3A+google+one+OR+two+%22australia%22+-bukan+site%3Acodeforces.com+filetype%3Apdf+1..3&gs_lp=Egxnd3Mtd2l6LXNlcnAiVmFsbGludGl0bGU6IGdvb2dsZSBvbmUgT1IgdHdvICJhdXN0cmFsaWEiIC1idWthbiBzaXRlOmNvZGVmb3JjZXMuY29tIGZpbGV0eXBlOnBkZiAxLi4zSABQAFgAcAB4AJABAJgBAKABAKoBALgBA8gBAPgBAZgCAKACAJgDAJIHAKAHAA&sclient=gws-wiz-serp
