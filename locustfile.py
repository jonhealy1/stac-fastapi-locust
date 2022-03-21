from locust import HttpUser, task, constant, tag, run_single_user
from helpers import test_item

import random
import json


class WebsiteTestUser(HttpUser):
    ### TODO integrate with debug call of WebsiteTestUser
    host = "http://localhost:8083"
    ###
    default_load_mulitplier = 0

    wait_time = constant(0.01)

    def on_start(self):
        """on_start is called when a Locust start before any task is scheduled"""
        pass

    def on_stop(self):
        """on_stop is called when the TaskSet is stopping"""
        pass

    def load_file(self, file) -> dict:
        f = open(file)
        data = json.load(f)
        return data

    @tag("root_catalog")
    @task(default_load_mulitplier)
    def get_root_catalog(self):
        self.client.get("/")

    @tag("all_collections")
    @task(default_load_mulitplier)
    def get_all_collections(self):
        self.client.get("/collections")

    @tag("get_collection")
    @task(default_load_mulitplier)
    def get_collection(self):
        self.client.get("/collections/test-collection")

    @tag("item_collection")
    @task(default_load_mulitplier)
    def get_item_collection(self):
        self.client.get("/collections/test-collection/items")

    @tag("get_item")
    @task(default_load_mulitplier)
    def get_item(self):
        random_number = random.randint(1, 11)
        item = self.load_file("data_loader/setup_data/sentinel-s2-l2a-cogs_0_100.json")
        random_id = item["features"][random_number]["id"]
        self.client.get(f"/collections/test-collection/items/{random_id}", name="/item")

    @tag("get_bbox")
    @task(default_load_mulitplier)
    def get_bbox_search(self):
        self.client.get("/search?bbox=-16.171875,-79.095963,179.992188,19.824820")

    @tag("post_bbox")
    @task(default_load_mulitplier)
    def post_bbox_search(self):
        self.client.post(
            "/search",
            json={"bbox": [16.171875, -79.095963, 179.992188, 19.824820]},
            name="bbox",
        )

    @tag("point_intersects")
    @task(default_load_mulitplier)
    def post_intersects_search(self):
        self.client.post(
            "/search",
            json={
                "collections": ["test-collection"],
                "intersects": {"type": "Point", "coordinates": [150.04, -33.14]},
            },
            name="point-intersects",
        )

    def get_collection_ids(self):
        collections_response = self.client.get("/collections")
        if collections_response.status_code == 200:
            collections_body = collections_response.json()
            print(f"Found {len(collections_body['collections'])} collections")
            collection_ids = [
                collection["id"] for collection in collections_body["collections"]
            ]
            return collection_ids
        else:
            # TODO proper error handling
            print("Get collections: non-200 response status code")
            return None

    def parse_request_items(self, collection_id, items_response):
        # parse response, if > 0 items then request Items
        if items_response.status_code == 200:
            items_body = items_response.json()
            item_ids = [feature["id"] for feature in items_body["features"]]
        else:
            # TODO proper error handling
            print("Get items: non-200 response status code")
            return None

        # request between 1 and min(10, result count) Items, serially
        for item_id in item_ids:
            self.client.get(
                f"/collections/{collection_id}/items/{item_id}", name="/item"
            )

    @tag("basic_nonspatial")
    @task(1)
    def basic_nonspatial_search(self):
        collection_ids = self.request_collection_ids()

        # /search request for random valid collection id
        # use default limit and sortby, randomize GET / POST
        collection_id = random.choice(collection_ids)
        get_post = random.choice([self.client.get, self.client.post])
        items_response = get_post("/search", json={"collections": [collection_id]})

        self.parse_request_items(collection_id, items_response)

    @tag("paged_poi")
    @task(1)
    def paged_poi_search(self):
        # get the bbox of a random collection
        collection_ids = self.get_collection_ids()
        collection_id = random.choice(collection_ids)
        collection_response = self.client.get(f"collections/{collection_id}")
        bbox = collection_response.json()["extent"]["spatial"]["bbox"]

        # execute a /search request with randomised intersects point within the bbox
        # randomise whether request is submitted via GET or Post
        # TODO request a randomised page of search results using the token parameters
        # TODO randomise the sort order among available fields
        get_post = random.choice([self.client.get, self.client.post])
        x = random.random() * (bbox[0] - bbox[2]) + bbox[0]
        y = random.random() * (bbox[1] - bbox[3]) + bbox[1]
        items_response = get_post(
            "/search", json={"intersects": {"type": "Point", "coordinates": [x, y]}}
        )

        self.parse_request_items(collection_id, items_response)

    #### CRUD routes
    @tag("create_item")
    @task(default_load_mulitplier)
    def create_item(self):
        random_number = random.randint(1, 100000)
        item = test_item
        item["id"] = f"test-item-{random_number}"
        item["collection"] = "test-collection"
        self.client.post(
            "/collections/test-collection/items", json=item, name="create-item"
        )


# run tests in debugger
# if launched directly, e.g. "python3 debugging.py", not "locust -f debugging.py"
if __name__ == "__main__":
    run_single_user(WebsiteTestUser)
