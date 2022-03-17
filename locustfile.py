from locust import HttpUser, task, between

class WebsiteTestUser(HttpUser):

    @task(1)
    def get_root_cataalog(self):
        self.client.get("http://localhost:8083")