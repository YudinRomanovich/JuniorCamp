from conftest import client

def get_access_token(username="string", password="string"):
    data = {
        "grant_type": "",
        "username": username,
        "password": password,
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }

    response = client.post("/auth/jwt/login", data=data)

    if response.status_code == 204:
        access_token = response.cookies.get("junior_cookie")
        return access_token
    else:
        print(f"Authentication failed: {response.text}")
        return None


def test_register():

    response = client.post("/auth/register", json={
        "email": "string",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "id": 0,
        "username": "string",
        "skills": "string",
        "profession": "string"
    })


    assert response.status_code == 201

def test_get_user():

    response = client.get("/get?username=string")

    assert response.status_code == 200


def test_login():

    data = {
        "grant_type": "",
        "username": "string",
        "password": "string",
        "scope": "",
        "client_id": "",
        "client_secret": "" 
    }

    response = client.post("/auth/jwt/login", data=data)

    assert response.status_code == 204

def test_update_user():

    access_token = get_access_token()

    client.cookies.update({"junior_cookie": access_token})

    response = client.put("/edit?new_username=test&new_profession=test&new_skills=test")

    assert response.status_code == 200

def test_get_user2():

    response = client.get("/get?username=test")

    assert response.status_code == 200

