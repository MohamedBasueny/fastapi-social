# def test_get_all_post(client):
#     user_data = {"email": "test@gmail.com",
#                  "password": "123"}
#     res = client.post("/auth/login", json=user_data)
#     new_user= res.json()
#     new_user['password'] = user_data['password']

#     from app.oauth2 import create_access_token
#     token = create_access_token({"user_id": new_user['id']})
#     headers = {
#         **client.headers,
#         "Authorization": f"Bearer {token}"
#     }
#     body={
#     "title" : "test post" , 
#     "content" : "this is the pla post " , 
#     "published" : True 
#     } 
#     res = client.post("/posts/create-post", headers=headers , data=body)
#     print(res.json())
#     assert res.status_code == 200 
from typing import Any
from fastapi.testclient import TestClient
from app.schemas import PostOut , Post
import pytest
def test_posts(authorized_client: Any , test_posts: Any):
    res = authorized_client.get("/posts/get-all-posts")
    posts = res.json()
    # print(posts)
    assert res.status_code == 200 
    assert len(posts) == len(test_posts)
    def validate (post) :
        return PostOut(**post)
    posts_mapped = list(map(validate , posts))
    print(posts_mapped[0].Post.title)



def test_unotherized_get_all_posts(client: TestClient,test_posts: Any):
    res = client.get("/posts/get-all-posts")
    assert res.status_code == 401 #unotherized 

def test_unotherized_get_post_by_id(client: TestClient,test_posts:[Post]):
    res = client.get(f"/posts/get-post-by-id/{test_posts[0].id}")
    assert res.status_code == 401 #unotherized 

def test_get_post_by_id(authorized_client: Any,test_posts: Any):
    post_id = test_posts[0].id 
    print(post_id)
    res = authorized_client.get(f"/posts/get-post-by-id/{post_id}")
    assert res.status_code == 200 
    print("********************",type(res.json()))
    # def validate(post) : 
    #         try :   
    #             Post(**post)
    #             return True 
    #         except : 
    #             return False
    # assert validate(res.json()) == True 


def test_get_post_by_id_not_exist(authorized_client: Any , test_posts: Any):
    res = authorized_client.get(f"/posts/get-post-by-id/{444}")
    assert res.status_code == 404 
  
@pytest.mark.parametrize("title,content,published" , [
    ("my first title" , "this is  my first title " , True ),
    ("my second title" , "this is  my secone title " , True ), 
    ("my third title" , "this is  my third title " , False ),  
])
def test_create_post(authorized_client , test_user  , test_posts , title , content , published) : 
    res  = authorized_client.post("/posts/create-post/" , json={
        "title" : title , 
        "content" : content , 
        "published" : published 
    })
    assert res.status_code == 201 
    post = Post(**res.json()) 
    assert post.title == title 
    assert post.content == content 
    assert post.published == published
    assert post.owner_id == test_user["id"]

@pytest.mark.parametrize("title,content" , [
    ("my first title" , "this is  my first title "  )])
def test_create_post_default_published_value(authorized_client , test_user  , test_posts , title , content):
    res  = authorized_client.post("/posts/create-post/" , json={
        "title" : title , 
        "content" : content 
    })
    assert res.status_code == 201 
    post = Post(**res.json()) 
    assert post.published == True 
    assert post.title == title 
    assert post.content == content 

@pytest.mark.parametrize("title,content,published" , [
    ("my first title" , "this is  my first title " , True )])
def test_unautherized_user_create_post(client , test_user  , test_posts , title , content , published):
    res  = client.post("/posts/create-post/" , json={
        "title" : title , 
        "content" : content , 
        "published" : published 
    })
    assert res.status_code == 401 


def test_unautherized_user_delete_post(client , test_user , test_posts ):
    res = client.delete("/posts/delete-post-by-id/1")
    assert res.status_code == 401 

def test_delete_post(authorized_client , test_posts):
    post_id = test_posts[0].id 
    res = authorized_client.delete(f"/posts/delete-post-by-id/{post_id}")
    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client , test_posts):
    res = authorized_client.delete(f"/posts/delete-post-by-id/{444}")
    assert res.status_code == 404

def test_delete_post_not_owned_by_user(authorized_client , test_posts):
    res = authorized_client.delete(f"/posts/delete-post-by-id/{test_posts[3].id}")
    assert res.status_code == 404

def test_update_post(authorized_client,test_user , test_posts) :
    data  ={
    "title" : "updated post test", 
    "content" : "this is my test updated post " , 
    "published" : False
 } 
    res = authorized_client.put(f"/posts/update-post-by-id/{test_posts[0].id}" , json=data)
    assert res.status_code == 204 
    
def test_update_post_not_owned_by_user(authorized_client,test_user , test_posts) :
    data  ={
    "title" : "updated post test", 
    "content" : "this is my test updated post " , 
    "published" : False
 } 
    res = authorized_client.put(f"/posts/update-post-by-id/{test_posts[3].id}" , json=data)
    assert res.status_code == 404 
    
def test_update_post_by_unautherized_user(client,test_user , test_posts) :
    data  ={
    "title" : "updated post test", 
    "content" : "this is my test updated post " , 
    "published" : False
 } 
    res = client.put(f"/posts/update-post-by-id/{test_posts[3].id}" , json=data)
    assert res.status_code ==  401

def test_update_post_not_exist(authorized_client,test_user , test_posts) :
    data  ={
    "title" : "updated post test", 
    "content" : "this is my test updated post " , 
    "published" : False
 } 
    res = authorized_client.put(f"/posts/update-post-by-id/{33333}" , json=data)
    assert res.status_code ==  404