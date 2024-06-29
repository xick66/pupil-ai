from dotenv import load_dotenv
import google.generativeai as genai
import os
import re
from tavily import TavilyClient

load_dotenv()

class Searcher():
    def __init__(self,
      include_answer:bool=True,
      include_domains:[str]=None, # all
      include_images:bool=False,
      include_raw_content:bool=False,
      exclude_domains:[str]=None,
      max_results:int=5,
      search_depth:str="advanced",
    ):
      self.tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
      self.config = {
        "include_answer": include_answer,
        "include_domains": include_domains,
        "include_images": include_images,
        "include_raw_content": include_raw_content,
        "exclude_domains": exclude_domains,
        "max_results": max_results,
        "search_depth": search_depth,
      }

      self.BASE_PARAMS = [
        "include_answer",
        "include_domains",
        "include_images",
        "include_raw_content",
        "exclude_domains",
        "max_results",
        "search_depth",
      ]
      self.QNA_PARAMS = [p for p in self.BASE_PARAMS if p != "include_answer"]
      self.DOMAIN_REGEX = r'([-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b)'
      self.URL_REGEX = r'((?:https?://www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&//=]*)'

    def remove_http(self, url: str) -> str:
      http = 'http://'
      https = 'https://'
      if url.startswith(http):
        return url[len(http)]
      elif url.startswith(https):
        return url[len(https):]
      return url

    def get_domain_from_url(self, url: str) -> str:
      m = re.search(self.DOMAIN_REGEX, url)
      return m.group(0) if m else None

    def get_domains(self, query: str) -> [str]:
      domains = re.findall(self.DOMAIN_REGEX, query)
      return domains

    def get_urls(self, query: str) -> [str]:
      urls = re.findall(self.URL_REGEX, query)
      return urls

    def dict_select(self, h, params):
      ret = {}
      for p in params:
        if p in h:
          ret[p] = h[p]
      return ret

    def search(self, query:str, include_full_url:bool = False, **kwargs) -> dict:
      urls = [url if include_full_url else self.get_domain_from_url(url) for url in self.get_urls(query)]
      params = {
        **self.dict_select(self.config, self.BASE_PARAMS),
        **self.dict_select(kwargs, self.BASE_PARAMS),
      }
      if params["include_domains"]:
        params["include_domains"] += urls
      else:
        params["include_domains"] = urls
      return self.tavily.search(
        query=query,
        **params
      )

    def get_search_context(self, query:str, **kwargs) -> str:
      return self.tavily.get_search_context(
        query=query,
        **{
          **self.dict_select(self.config, self.BASE_PARAMS),
          **self.dict_select(kwargs, self.BASE_PARAMS),
        },
      )

    # returns the answer
    def qna_search(self, query:str, **kwargs) -> str:
      return self.tavily.qna_search(
        query=query,
        **{
          **self.dict_select(self.config, self.QNA_PARAMS),
          **self.dict_select(kwargs, self.QNA_PARAMS),
        },
      )

if __name__ == "__main__":
  searcher = Searcher()
  response = searcher.search(
    query="who is indonesia current president based on https://kemlu.go.id/bucharest/en/pages/presiden_republik_indonesia/3947/etc-menu",
    include_answer=True,
    include_raw_content=False,
    include_full_url=False,
    include_domains=['codeforces.com']
  ) # output bener tp ga reasonable

  print(response["answer"])
  print(response)

  print("============Context==========")
  response = searcher.get_search_context(query="what is mathematic")
  print(response)

  print("============QNA==========")
  response = searcher.qna_search(query="what is 1 + 1 equal to?")
  print(response)

  """
  {'query': 'Summarize Sasha and the Beautiful Array problem in codeforces', 'follow_up_questions': None, 'answer': "The Sasha and the Beautiful Array problem on Codeforces involves processing queries on an initially empty array. During each query, an integer is given, and it must be appended to the array if doing so maintains the array's beauty. The array remains beautiful if appending the integer does not disrupt its beauty.", 'images': None, 'results': [{'title': 'Problem - 1155D - Codeforces', 'url': 'https://codeforces.com/problemset/problem/1155/D', 'content': 'You are given an array a a consisting of n n integers. Beauty of array is the maximum sum of some consecutive subarray of this array (this subarray may be empty). For example, the beauty of the array [10, -5, 10, -4, 1] is 15, and the beauty of the array [-3, -5, -1] is 0. You may choose at most one consecutive subarray of a a and multiply all ...', 'score': 0.97352, 'raw_content': "You are given an array $$$a$$$ consisting of $$$n$$$ integers. Beauty of array is the maximum sum of some consecutive subarray of this array (this subarray may be empty). For example, the beauty of the array [10, -5, 10, -4, 1] is 15, and the beauty of the array [-3, -5, -1] is 0.\nYou may choose at most one consecutive subarray of $$$a$$$ and multiply all values contained in this subarray by $$$x$$$. You want to maximize the beauty of array after applying at most one such operation.\nThe first line contains two integers $$$n$$$ and $$$x$$$ ($$$1 \\le n \\le 3 \\cdot 10^5, -100 \\le x \\le 100$$$) — the length of array $$$a$$$ and the integer $$$x$$$ respectively.\nThe second line contains $$$n$$$ integers $$$a_1, a_2, \\dots, a_n$$$ ($$$-10^9 \\le a_i \\le 10^9$$$) — the array $$$a$$$.\nPrint one integer — the maximum possible beauty of array $$$a$$$ after multiplying all values belonging to some consecutive subarray $$$x$$$.\nIn the first test case we need to multiply the subarray [-2, 1, -6], and the array becomes [-3, 8, 4, -2, 12] with beauty 22 ([-3, 8, 4, -2, 12]).\nIn the second test case we don't need to multiply any subarray at all.\nIn the third test case no matter which subarray we multiply, the beauty of array will be equal to 0."}, {'title': 'Problem - 1841B - Codeforces', 'url': 'https://codeforces.com/problemset/problem/1841/B', 'content': 'You are given an array a a, which is initially empty. You have to process q q queries to it. During the i i -th query, you will be given one integer xi x i, and you have to do the following: if you can append the integer xi x i to the back of the array a a so that the array a a stays beautiful, you have to append it; otherwise, do nothing.', 'score': 0.93766, 'raw_content': 'The array $$$[a_1, a_2, \\dots, a_k]$$$ is called beautiful if it is possible to remove several (maybe zero) elements from the beginning of the array and insert all these elements to the back of the array in the same order in such a way that the resulting array is sorted in non-descending order.\nIn other words, the array $$$[a_1, a_2, \\dots, a_k]$$$ is beautiful if there exists an integer $$$i \\in [0, k-1]$$$ such that the array $$$[a_{i+1}, a_{i+2}, \\dots, a_{k-1}, a_k, a_1, a_2, \\dots, a_i]$$$ is sorted in non-descending order.\nFor example:\nNote that any array consisting of zero elements or one element is beautiful.\nYou are given an array $$$a$$$, which is initially empty. You have to process $$$q$$$ queries to it. During the $$$i$$$-th query, you will be given one integer $$$x_i$$$, and you have to do the following:\nAfter each query, report whether you appended the given integer $$$x_i$$$, or not.\nThe first line contains one integer $$$t$$$ ($$$1 \\le t \\le 10^4$$$) — the number of test cases.\nEach test case consists of two lines. The first line contains one integer $$$q$$$ ($$$1 \\le q \\le 2 \\cdot 10^5$$$) — the number of queries. The second line contains $$$q$$$ integers $$$x_1, x_2, \\dots, x_q$$$ ($$$0 \\le x_i \\le 10^9$$$).\nAdditional constraint on the input: the sum of $$$q$$$ over all test cases does not exceed $$$2 \\cdot 10^5$$$).\nFor each test case, print one string consisting of exactly $$$q$$$ characters. The $$$i$$$-th character of the string should be 1 if you appended the integer during the $$$i$$$-th query; otherwise, it should be 0.\nConsider the first test case of the example. Initially, the array is $$$[]$$$.'}, {'title': 'Problem - 1929A - Codeforces', 'url': 'https://codeforces.com/problemset/problem/1929/A', 'content': 'The first line contains a single integer t t ( 1 ≤ t ≤ 500 1 ≤ t ≤ 500) — the number of test cases. The description of the test cases follows. The first line of each test case contains a single integer n n ( 2 ≤ n ≤ 100 2 ≤ n ≤ 100) — the length of the array a a. The second line of each test case contains n n integers a1,a2 ...', 'score': 0.92485, 'raw_content': 'Sasha decided to give his girlfriend an array $$$a_1, a_2, \\ldots, a_n$$$. He found out that his girlfriend evaluates the beauty of the array as the sum of the values $$$(a_i - a_{i - 1})$$$ for all integers $$$i$$$ from $$$2$$$ to $$$n$$$.\nHelp Sasha and tell him the maximum beauty of the array $$$a$$$ that he can obtain, if he can rearrange its elements in any way.\nEach test consists of multiple test cases. The first line contains a single integer $$$t$$$ ($$$1 \\le t \\le 500$$$) — the number of test cases. The description of the test cases follows.\nThe first line of each test case contains a single integer $$$n$$$ ($$$2 \\leq n \\leq 100$$$) — the length of the array $$$a$$$.\nThe second line of each test case contains $$$n$$$ integers $$$a_1, a_2, \\ldots, a_n$$$ ($$$1 \\leq a_i \\leq 10^9$$$) — the elements of the array $$$a$$$.\nFor each test case, output a single integer — the maximum beauty of the array $$$a$$$ that can be obtained.\nIn the first test case, the elements of the array $$$a$$$ can be rearranged to make $$$a = [1, 2, 3]$$$. Then its beauty will be equal to $$$(a_2 - a_1) + (a_3 - a_2) = (2 - 1) + (3 - 2) = 2$$$.\nIn the second test case, there is no need to rearrange the elements of the array $$$a$$$. Then its beauty will be equal to $$$0$$$.'}, {'title': 'Problem - 1929C - Codeforces', 'url': 'https://codeforces.com/problemset/problem/1929/C', 'content': '256 megabytes. input. standard input. output. standard output. Sasha decided to give his girlfriend the best handbag, but unfortunately for Sasha, it is very expensive. Therefore, Sasha wants to earn it. After looking at earning tips on the internet, he decided to go to the casino. Sasha knows that the casino operates under the following rules.', 'score': 0.90903, 'raw_content': 'Sasha decided to give his girlfriend the best handbag, but unfortunately for Sasha, it is very expensive. Therefore, Sasha wants to earn it. After looking at earning tips on the internet, he decided to go to the casino.\nSasha knows that the casino operates under the following rules. If Sasha places a bet of $$$y$$$ coins (where $$$y$$$ is a positive integer), then in case of winning, he will receive $$$y \\cdot k$$$ coins (i.e., his number of coins will increase by $$$y \\cdot (k - 1)$$$). And in case of losing, he will lose the entire bet amount (i.e., his number of coins will decrease by $$$y$$$).\nNote that the bet amount must always be a positive ($$$> 0$$$) integer and cannot exceed Sasha\'s current number of coins.\nSasha also knows that there is a promotion at the casino: he cannot lose more than $$$x$$$ times in a row.\nInitially, Sasha has $$$a$$$ coins. He wonders whether he can place bets such that he is guaranteed to win any number of coins. In other words, is it true that for any integer $$$n$$$, Sasha can make bets so that for any outcome that does not contradict the rules described above, at some moment of time he will have at least $$$n$$$ coins.\nEach test consists of multiple test cases. The first line contains a single integer $$$t$$$ ($$$1 \\le t \\le 1000$$$) — the number of test cases. The description of the test cases follows.\nThe single line of each test case contains three integers $$$k, x$$$ and $$$a$$$ ($$$2 \\leq k \\leq 30$$$, $$$1 \\leq x \\leq 100$$$, $$$1 \\leq a \\leq 10^9$$$) — the number of times the bet is increased in case of a win, the maximum number of consecutive losses, and the initial number of coins Sasha has.\nFor each test case, output "YES" (without quotes) if Sasha can achieve it and "NO" (without quotes) otherwise.\nYou can output "YES" and "NO" in any case (for example, the strings "yEs", "yes" and "Yes" will be recognized as a positive answer).\nIn the first test case, Sasha can proceed as follows:\nNote that Sasha cannot lose more than once in a row.\nIt can be proven that with this strategy, Sasha can obtain as many coins as he wants.\nIn the second test case, Sasha can only place $$$1$$$ coin for the first time. But in case of a loss, he will not be able to place any more bets, so he will not be able to guarantee having as many coins as he wants.'}, {'title': 'Problem - 1954B - Codeforces', 'url': 'https://codeforces.com/problemset/problem/1954/B', 'content': 'In the first testcase, it is impossible to modify the array in such a way that it stops being beautiful. An array consisting of identical numbers will remain beautiful no matter how many numbers we remove from it. In the second testcase, you can remove the number at the index $$$5$$$, for example. The resulting array will be $$$[1, 2, 1, 2]$$$.', 'score': 0.90586, 'raw_content': "Let's call an array $$$a$$$ beautiful if you can make all its elements the same by using the following operation an arbitrary number of times (possibly, zero):\nYou are given a beautiful array $$$a_1, a_2, \\dots, a_n$$$. What is the minimum number of elements you have to remove from it in order for it to stop being beautiful? Swapping elements is prohibited. If it is impossible to do so, then output -1.\nThe first line contains a single integer $$$t$$$ ($$$1 \\le t \\le 10^4$$$)\xa0— the number of test cases.\nThe first line of each test case contains a single integer $$$n$$$ ($$$1 \\le n \\le 3 \\cdot 10^5$$$).\nThe second line contains $$$n$$$ integers $$$a_1, a_2, \\dots, a_n$$$ ($$$1 \\le a_i \\le n$$$).\nAdditional constraints on the input:\nFor each test case, output a single integer\xa0— the minimum number of elements you have to remove from the array $$$a$$$ in order for it to stop being beautiful. If it is impossible, then output -1.\nIn the first testcase, it is impossible to modify the array in such a way that it stops being beautiful. An array consisting of identical numbers will remain beautiful no matter how many numbers we remove from it.\nIn the second testcase, you can remove the number at the index $$$5$$$, for example.\nThe resulting array will be $$$[1, 2, 1, 2]$$$. Let's check if it is beautiful. Two operations are available:\nThus, the array $$$[1, 2, 1, 2]$$$ is not beautiful.\nIn the fourth testcase, you can remove the first three elements, for example. The resulting array $$$[5, 3, 3, 3]$$$ is not beautiful."}], 'response_time': 3.74}
  """

  # response = searcher.qna_search(
  #   query="Can you summarize Sasha and the Beautiful Array problem in codeforces",
  #   max_results=5,
  #   include_raw_content=True,
  #   include_domains=["codeforces.com"])
  # print("response", response, end="\n\n\n\n\n")

  """
  "[\"{\\\"url\\\": \\\"https://mirror.codeforces.com/blog/entry/47322\\\", \\\"content\\\": \\\"We calculate the answer for \\\\u03b1 and \\\\u03b2 separately (on two different segment trees) and then combine them together when we query. Now, each range increment is equivalent to multiplying \\\\u03b1k in a range [l, r] and we can find \\\\u03b1k using binary exponentiation. (divide and conquer) The rest can be easily handled with a lazy propogation segment tree.\\\"}\", \"{\\\"url\\\": \\\"https://codeforces.com/problemset/problem/1929/C\\\", \\\"content\\\": \\\"In the first test case, Sasha can proceed as follows: If Sasha places a bet for the first time or if he won the previous bet, then he places 1 1 coin. If Sasha lost the previous bet, then he places 2 2 coins. Note that Sasha cannot lose more than once in a row. It can be proven that with this strategy, Sasha can obtain as many coins as he wants.\\\"}\", \"{\\\"url\\\": \\\"https://codeforces.com/problemset/problem/1841/B\\\", \\\"content\\\": \\\"You are given an array a a, which is initially empty. You have to process q q queries to it. During the i i -th query, you will be given one integer xi x i, and you have to do the following: if you can append the integer xi x i to the back of the array a a so that the array a a stays beautiful, you have to append it; otherwise, do nothing.\\\"}\", \"{\\\"url\\\": \\\"https://codeforces.com/problemset/problem/1929/A\\\", \\\"content\\\": \\\"The first line contains a single integer t t ( 1 \\\\u2264 t \\\\u2264 500 1 \\\\u2264 t \\\\u2264 500) \\\\u2014 the number of test cases. The description of the test cases follows. The first line of each test case contains a single integer n n ( 2 \\\\u2264 n \\\\u2264 100 2 \\\\u2264 n \\\\u2264 100) \\\\u2014 the length of the array a a. The second line of each test case contains n n integers a1,a2 ...\\\"}\"]"
  """

  # response = searcher.get_search_context(
  #   query="Can you summarize Sasha and the Beautiful Array problem in codeforces",
  #   max_results=5,
  #   include_raw_content=True,
  #   include_domains=["codeforces.com"])
  # print(response, end="\n\n\n\n\n")
  """
  The Sasha and the Beautiful Array problem on Codeforces requires processing queries to append integers to an array while maintaining its beauty. During each query, an integer can be appended to the array if it doesn't affect its beauty. The beauty of the array is defined as the maximum sum of some consecutive subarray.
  """


'''
response format

answer: The answer to your search query.
query: Your search query.
response_time: Your search result response time.
images: A list of query related image urls.
follow_up_questions: A list of suggested research follow up questions related to original query.
results: A list of sorted search results ranked by relevancy.
  title: The title of the search result url.
  url: The url of the search result.
  content: The most query related content from the scraped url. We use proprietary AI and algorithms to extract only the most relevant content from each url, to optimize for context quality and size.
  raw_content: The parsed and cleaned HTML of the site. For now includes parsed text only.
  score: The relevance score of the search result.


400: Bad Request — Your request is invalid.
401: Unauthorized — Your API key is wrong.
403: Forbidden — The endpoint requested is hidden for administrators only.
404: Not Found — The specified endpoint could not be found.
405: Method Not Allowed — You tried to access an endpoint with an invalid method.
429: Too Many Requests — You're requesting too many results! Slow down!
500: Internal Server Error — We had a problem with our server. Try again later.
503: Service Unavailable — We're temporarily offline for maintenance. Please try again later.
504: Gateway Timeout — We're temporarily offline for maintenance. Please try again later.


Tavily Search API has a rate limit of 20 requests per minute.
'''