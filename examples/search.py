
from scripts.collect import Collect

c = Collect("config.ini")
c.search("brasil", limit_pages=1, max_per_request=10, folder="coleta/teste1", id="coletabrasil1")