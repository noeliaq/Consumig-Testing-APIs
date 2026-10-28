"""
Exercise: Build Your API Testing Toolkit (Python portion)
Module 4 — REST API Fundamentals
Lesson 10 — Practice Exercise
Estimated time: 40 minutes

Objective: Build a reusable API client class following the base class + subclass pattern.
"""

import requests


# ============================================================
# TODO: Implement the APIClient base class
# It should:
# - Accept base_url and optional default_headers in __init__
# - Use requests.Session() for connection reuse
# - Have get(), post(), patch(), delete() methods
# - Each method should prepend base_url to the path
# - Each method should call response.raise_for_status()
# ============================================================
class APIClient:
    """Base class for API clients. Extend this for each specific API."""

    def __init__(self, base_url: str, default_headers: dict = None):
        # TODO: implement
        self.base_url = base_url.rstrip("/") #removes the trailing slash
        self.session = requests.Session() #creates a reusable connection object
        self.session.headers.update(default_headers or {}) #adds default headers to every request

    def _url(self, path: str) -> str:
        """Combine base_url with a path."""
        # TODO: implement
        return f"{self.base_url}/{path.lstrip('/')}" #removes beginning left character 

#Uses the session to send an HTTP request, sends the method like "GET" or "POST",sends the full URL built from base_url and path.
    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        response = self.session.request(method, self._url(path), **kwargs)
        response.raise_for_status() #checks if the request failed
        return response

     #shortcut methods: instead of writing the same request logic everytime, we wrap it in simple methods,and forward their arguments down to _request().   
    def get(self, path: str, **kwargs):
        # TODO: implement
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        # TODO: implement
        return self._request("POST", path, **kwargs)

    def patch(self, path: str, **kwargs):
        # TODO: implement
        return self._request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs):
        # TODO: implement
        return self._request("DELETE", path, **kwargs)


# ============================================================
# TODO: Implement JSONPlaceholderClient extending APIClient
# ============================================================
class JSONPlaceholderClient(APIClient): #This class specifically knows how to work with the JSONPlaceholder API.
    """Client for https://jsonplaceholder.typicode.com"""


    def __init__(self):
        # TODO: call super().__init__ with the right base_url and headers
        #This tells the parent class: Use this website as the base URL, and Accept JSON responses
        super().__init__(
            "https://jsonplaceholder.typicode.com",
            default_headers= {"Accept": "application/json"},
        )

    def get_user(self, user_id: int) -> dict:
        """Fetch a single user by ID."""
        # TODO: implement
        response = self.get(f"/users/{user_id}")
        #converts the JSON response into python data
        return response.json()

    def get_user_posts(self, user_id: int) -> list:
        """Fetch all posts for a specific user."""
        # TODO: implement
        response = self.get("/posts", params= {"user_Id": user_id})
        return response.json()

    def create_post(self, user_id: int, title: str, body: str) -> dict:
        """Create a new post (simulated). Returns the created post dict."""
        # TODO: implement
        return self.post(f"/posts", json={"userId": user_id, "title": title, "body": body}
        ).json()

    def search_posts(self, query: str) -> list:
        """
        Client-side filter: fetch all posts and return those whose title
        contains `query` (case-insensitive).
        """
        # TODO: implement
        posts= self.get("/posts").json()
        
        return [ 
            post 
            for post in posts 
            if query.lower() in post.get("title", "").lower()]

# ============================================================
# Demo (runs when you execute this file)
# ============================================================
if __name__ == "__main__":
    client = JSONPlaceholderClient() #This creates a client for the API.

    try:
        
        
       
        


    # TODO: Get user 5's profile and print name, email, city
        print("1. User 5 profile:")
        user_profile = client.get_user(5)
        print (f"   Name: {user_profile ['name']}")
        print (f"   Email:{user_profile ['email']}") 
        print (f"   City: {user_profile ["address"] ["city"]}")

        # TODO: Get user 5's posts and print count + first title
        print("\n2. User 5's posts:")
        user_posts = client.get_user_posts (5)
        print (f"User 5 has {len(user_posts) }")
        print (f"Titles: {user_posts[0]['title']}")

        # TODO: Create a post and print its id and title
        print("\n3. Create a new post:")
        new_post = client.create_post(
                        user_id= 5,
                        title = "new post",
                        body = "Create a new post. Returns the created post dict.",
                )
       
        print (f" Post ID {new_post.get('id')}")
        print (f" Title Post: {new_post.get ('title')}")
    
        # TODO: Search posts for keyword "qui" and print count + first 3 titles
        print("\n4. Search posts for 'qui':")

        qui_posts = client.search_posts("qui")
        print (f" Matching posts : {len(qui_posts)}")

        for post in qui_posts [:3]:
            print (f"{post ['title']}" )

    finally:
        client.session.close()



    # Expected output:
    # 1. User 5 profile:
    #    Name:  Chelsey Dietrich
    #    Email: Lucio_Hettinger@annie.ca
    #    City:  Roscoeview
    # ...

"""RESULTS
(venv) noeliaquiroga@Mac consuming_testing_api % python3 starter.py
1. User 5 profile:
   Name: Chelsey Dietrich
   Email:Lucio_Hettinger@annie.ca
   City: Roscoeview

2. User 5's posts:
User 5 has 100
Titles: sunt aut facere repellat provident occaecati excepturi optio reprehenderit

3. Create a new post:
 Post ID 101
 Title Post: new post

4. Search posts for 'qui':
 Matching posts : 33
qui est esse
ea molestias quasi exercitationem repellat qui ipsa sit aut
dolorem eum magni eos aperiam quia
(venv) noeliaquiroga@Mac consuming_testing_api % 




"""

