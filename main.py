from prometheus_client import start_http_server, Gauge
import requests
import time

URLS = [
    "https://httpstat.us/503",
    "https://httpstat.us/200"
]

# Метрики  
url_up = Gauge('sample_external_url_up', 'Whether the URL is up (1 = up, 0 = down)', ['url'])
url_response_time = Gauge('sample_external_url_response_ms', 'Response time in ms', ['url'])

def check_urls():
    while True:
        for url in URLS:
            try:
                start = time.time()
                response = requests.get(url, timeout=5)
                elapsed = (time.time() - start) * 1000  # in milliseconds
                url_response_time.labels(url=url).set(elapsed)
                url_up.labels(url=url).set(1 if response.status_code == 200 else 0)
            except Exception:
                url_response_time.labels(url=url).set(0)
                url_up.labels(url=url).set(0)
        time.sleep(10)  # refresh every 10 seconds

if __name__ == "__main__":
    start_http_server(8000)
    check_urls()
