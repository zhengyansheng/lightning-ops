import requests


class Http(object):

    @staticmethod
    def get(url, params, timeout=10):
        try:
            req = requests.get(url, params=params, timeout=timeout)
        except Exception as e:
            return e.args, False
        else:
            if not req.ok:
                return req.text, False
            return req.json(), True

    @staticmethod
    def post(url, data, header=None, timeout=10):
        if not header:
            header = {
                "Content-Type": "application/json"
            }

        try:
            req = requests.post(url, data=data, header=header, timeout=timeout)
        except Exception as e:
            return e.args, False
        else:
            if not req.ok:
                return req.text, False
            return req.json(), True

    @staticmethod
    def put(url, data, header=None):
        pass

    @staticmethod
    def delete(url, data):
        pass
