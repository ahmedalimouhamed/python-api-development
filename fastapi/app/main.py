from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
  title:      str
  content:    str
  published:  bool = True   
  rating:     Optional[int] = None 

myPosts = [
  {"title": "title post 1", "content": "content post 1", "published": True, "rating": 4, "id": 1},
  {"title": "title post 2", "content": "content post 2", "published": True, "rating": 3.5, "id": 2},
  {"title": "title post 3", "content": "content post 3", "published": True, "rating": 5, "id": 3},
]  

def find_post(id):
  for p in myPosts:
    if p["id"] == id:
      return p
    
def find_index_post(id):
  for i, p in enumerate(myPosts):
    if p['id'] == id:
      return i

@app.get("/")
def root():
  return {"message": "Hello world!!!"}

@app.get("/posts")
def getPosts():
  return {"data": myPosts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
  post_dict = post.dict()
  post_dict['id'] = randrange(0, 100000000)
  myPosts.append(post_dict)
  return {"new_post": post}

@app.get("/posts/latest")
def get_latest_post():
  post = myPosts[len(myPosts) - 1]
  return {"detail": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
  post = find_post(id)
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
  return {"post": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
  index = find_index_post(id)
  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    myPosts.pop(index)
  return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
  index = find_index_post(id)

  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
  post_dict = post.dict()
  post_dict['id'] = id
  myPosts[index] = post_dict

  return {"data": post_dict}



