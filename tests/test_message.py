from conftest import client

def test_create_message():

    response = client.post("/messages/api/send?to_user=1&new_message=test")

    assert response.status_code == 200


def test_get_messages():

    response = client.get("/messages/api/get")

    assert response.status_code == 200


def test_update_message():

    response = client.put("/messages/api/edit/0?new_text_message=Test")

    assert response.status_code == 200

def test_delete_message():

    response = client.delete("/messages/api/delete/1")

    assert response.status_code == 200