
from scripts.collect import Collect

c = Collect("config.ini")
c.stream(search_rules=["sergipe OR bahia", "brasil"], limit=20, folder="coleta/teste1", id="coletabrasil1")