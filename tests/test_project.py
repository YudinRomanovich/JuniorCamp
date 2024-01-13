from conftest import client


def test_create_project():

    data = {
        "id": 0,
        "name": "string",
        "description": "string",
        "author_id": 0,
        "needed_skills": "string"
    }

    response = client.post("/projects/api/create", json=data)

    assert response.status_code == 200


def test_get_project():

    response = client.get("/projects/api/get")

    assert response.status_code == 200


def test_update_project():

    response = client.put("/projects/api/edit?new_description=test&new_name=test&new_needed_skills=test&current_project_id=0&current_project_author_id=0")

    assert response.status_code == 200


def test_delete_project():

    response = client.delete("/projects/api/delete?current_project_id=0&current_project_author_id=0")

    assert response.status_code == 200