from app.schemas import UserOut , Token
import pytest 

# def test_root_path (client):
#     res = client.get("/")
#     assert res.status_code == 200
#     assert res.json() == {"message" : "hello World!"}
#     print(res.json() , "," , res.status_code)

# def test_create_user (client):
#     res = client.post("/users/create-user/" , 
#                       json={"email" : "test@gmail.com" , 
#                             "password" : "123"})
#     assert res.status_code == 201
#     new_user = UserOut(**res.json())
#     print(new_user)

def test_user_login(client , test_user) : 
    res2 = client.post("/auth/login" , 
                      data={"username" : test_user["email"] , 
                            "password" : test_user["password"]})
    assert res2.status_code == 200 
    access_token = Token(**res2.json()).access_token
    from app.oauth2 import verify_acces_token 
    assert verify_acces_token(access_token ,Exception()).id == "1"



@pytest.mark.parametrize("email,password,status_code" , [
    ("wrongtest@gm.com" , "12334" , 403) , 
    ("test@gmail.com" , "12345" , 403 ) , 
    (None , None , 422) ,
    ("email@gmail.com" , None , 422)
])
def test_incorrect_login(test_user , client ,email, password,status_code ) : 
    res = client.post("/auth/login" , 
                      data={"username" : email , 
                            "password" : password})
    

    assert res.status_code == status_code 
    # print("Response:\n",res.json())
    # assert res.json()["detail"] == detail
