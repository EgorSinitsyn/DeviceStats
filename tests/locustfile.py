from locust import HttpUser, TaskSet, task, between
import random

class DeviceTest(TaskSet):

    @task
    def post_stats(self):
        device_id = random.randint(1, 10)
        payload = {
            "x": random.uniform(0, 100),
            "y": random.uniform(0, 100),
            "z": random.uniform(0, 100)
        }
        self.client.post(f"/devices/{device_id}/data", json=payload)

    @task
    def get_device_stats(self):
        device_id = random.randint(1, 10)
        self.client.get(f"/devices/{device_id}/data/all")

class WebsiteUser(HttpUser):
    tasks = [DeviceTest]
    wait_time = between(1, 5)