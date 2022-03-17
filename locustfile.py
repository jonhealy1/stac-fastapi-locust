from locust import HttpUser, task, between

class WebsiteTestUser(HttpUser):

    wait_time = between(0.5, 3.0)
    
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        pass

    @task(1)
    def get_root_catalog(self):
        self.client.get("http://localhost:8083")

    @task(2)
    def get_all_collections(self):
        self.client.get("http://localhost:8083/collections")
