from locust import HttpUser, task, between

class WebsiteTestUser(HttpUser):

    # wait_time = between(0.0001, 0.0002)
    
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

    @task(3)
    def get_collection(self):
        self.client.get("http://localhost:8083/collections/test-collection")

    @task(4)
    def get_item_collection(self):
        self.client.get("http://localhost:8083/collections/test-collection/items")

    @task(5)
    def get_item(self):
        self.client.get("http://localhost:8083/collections/test-collection/items/S2B_1CCV_20181004_0_L2A")
