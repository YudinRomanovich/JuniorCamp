from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    @task
    def perform_test1(self):
        self.client.get("/projects/api/get")

    @task
    def perform_test2(self):
        data = {
            "grant_type": "",
            "username": "test@test.com",
            "password": "1234",
            "scope": "",
            "client_id": "",
            "client_secret": "" 
        }

        self.client.post("/auth/jwt/login", data=data)

    @task
    def perform_test3(self):
        self.client.get("/login")


    @task
    def perform_test4(self):
        self.client.get("/register")