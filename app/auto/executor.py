import requests


def run_job(id):
    s = requests.Session()
    requests.Session()
    s.post("http://127.0.0.1:5000/api/v1/user/",
           data={"username": "admin", "password": "123456", "method": "sign_in"})

    s.get("http://127.0.0.1:5000/test_run/auto/%s" % id)
