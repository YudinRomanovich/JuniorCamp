from conftest import client

def test_create_friends_list():
    
    response = client.post("/friends/update_friends_list")

    assert response.status_code == 200

def test_add_friend():
    
    response = client.post("/friends/add/{user_id}?new_friend_id=1")

    assert response.status_code == 200

def test_get_friend():

    response = client.get("/friends/")

    assert response.status_code == 200

def test_delete_friend():

    response = client.delete("/friends/delete?deleted_friend_id=1")

    assert response.status_code == 200

