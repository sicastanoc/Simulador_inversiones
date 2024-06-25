import json

from datetime import datetime, time
from requests import Session

URL = "https://query2.finance.yahoo.com/v8/finance/chart/{stock}.CL?period1={init_period}&period2={end_period}&interval=1d"


class RequestData:

    def __init__(self) -> None:
        
        self.session = Session()
        self.session.headers.update({
        "updgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86__64) "
        "AppleWebKit/537.36 (KHTML, likle Gecko) "
        "Chrome/114.0.0.0 Safari/537.36",
        })

        self.response = {}

    def get_keys(self, key_name: str, entry: dict):

        if isinstance(entry, dict):
            for key, value in entry.items():

                if isinstance(value, dict):
                    self.get_keys(key_name, value)

                elif isinstance(value, list):
                    self.get_keys(key_name, value[0]) 

                if key == key_name:
                    if isinstance(value, list):
                        value = value[0]
                    self.response.update({key_name: value})
                    break

    def request_data(
            self, 
            stock: str, 
            init_date: datetime = datetime.combine(datetime.now(), time.min), 
            end_date: datetime = datetime.combine(datetime.now(), time.max)
            ) -> json:
        
        datetime.timestamp


        req = self.session.get(
            URL.format(
                stock=stock,
                init_period=int(datetime.timestamp(init_date)),
                end_period=int(datetime.timestamp(end_date))
            )
        )

        response = json.loads(req.content)

        self.get_keys("regularMarketTime", response)
        self.get_keys("close", response)

    @classmethod
    def get_request(cls, stock: str) -> dict:

        request = cls()
        request.request_data(stock)

        request.session.close()

        return request.response


if __name__ == '__main__':

    print(RequestData.get_request("BCOLOMBIA"))