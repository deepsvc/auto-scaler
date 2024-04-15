import requests
import time


class AutoScaler:
    def __init__(self, app_url, high_threshold, low_threshold):
        self.app_url = app_url
        self.high_threshold = high_threshold
        self.low_threshold = low_threshold
        self.replica_count = 10  # Initial replica count

    def get_cpu_utilization(self):
        try:
            response = requests.get(
                f"{self.app_url}/app/status",
                headers={
                    "Accept": "application/json",
                },
            )
            return (
                response.json()["cpu"]["highPriority"]
            ) * 100  # Multiplying by 100 to make the value readable.

        except (requests.RequestException, ValueError):
            # Handle API errors or invalid responses
            return None

    def update_replicas(self, replicas):
        rep_count = {"replicas": replicas}
        try:
            requests.put(
                f"{self.app_url}/app/replicas",
                json=rep_count,
                headers={
                    "Content-Type": "application/json",
                },
            )

        except (requests.RequestException, ValueError):
            # Handle API errors or invalid responses
            print("Error Scaling Replicas. Retrying later.\n")

    def scale(self):
        cpu_usage = self.get_cpu_utilization()
        if cpu_usage is None:
            print("Error fetching CPU utilization. Retrying later.\n")
            return

        if cpu_usage > self.high_threshold:
            self.replica_count += 1
            self.update_replicas(self.replica_count)
            print(f"Current CPU Usage: {cpu_usage:.1f}%")
            print(f"Scaling up: Increased replicas to {self.replica_count}\n")
        elif cpu_usage < self.low_threshold and self.replica_count > 1:
            self.replica_count -= 1
            self.update_replicas(self.replica_count)
            print(f"Current CPU Usage: {cpu_usage:.1f}%")
            print(f"Scaling down: Decreased replicas to {self.replica_count}\n")
        else:
            print(f"CPU utilization within acceptable range: {cpu_usage:.1f}%\n")


if __name__ == "__main__":
    app_url = "http://localhost:8123"  # Application URL
    high_threshold = 85  # High CPU threshold value
    low_threshold = 75  # Low CPU threshold value

    autoscaler = AutoScaler(app_url, high_threshold, low_threshold)

    while True:
        autoscaler.scale()
        time.sleep(2)  # Interval for CPU Utilization check
