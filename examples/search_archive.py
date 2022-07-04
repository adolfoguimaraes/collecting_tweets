
from scripts.collect import Collect
import datetime


c = Collect("config.ini")
time = {"end": datetime.datetime.strptime("2022-07-02 23:59:59", "%Y-%m-%d %H:%M:%S"), "delta": 5, "delta_type": "minute"}
c.search_archive("brasil OR sergipe", max_per_request=100, time=time, id="coletabrasil2", folder="coleta/teste1")