
from twarc.client2 import Twarc2
import threading
import jsonlines


from twarc.expansions import flatten
import configparser

class Collect:

    def __init__(self, config_file):

        # Load config file
        config = configparser.RawConfigParser()
        config.read(config_file)

        BEARER_TOKEN = config['TWITTER']['BEARER_TOKEN']

        # Twitter authentication
        self.api = Twarc2(bearer_token=BEARER_TOKEN)

    def search(self, query, limit_pages=1, id="collecting_search", max_per_request=10, folder=None):
        pages = 0
        found_tweets = 0
        try:

            if folder:
                file_output = folder + "/" + id + ".jsonl"
            else:
                file_output = id + ".jsonl"

            for response_page in self.api.search_recent(query, sort_order='recency',max_results=max_per_request):
                pages += 1

                tweets = flatten(response_page)
                
                found_tweets += len(tweets)

                with jsonlines.open(file_output, mode="a") as writer:
                    for t in tweets:
                        writer.write(t)


                if pages == limit_pages:
                    break

            print("Total collected: %i" % found_tweets)
        except Exception as e:
            print("Collect error.")
            print(e)

    def stream(self, search_rules, id="collecting_stream", limit=100, folder=None):

        try:

            # Clear all rules
            rules = self.api.get_stream_rules()
            if "data" in rules and len(rules["data"]) > 0:
                rule_ids = [r["id"] for r in rules["data"]]
                self.api.delete_stream_rule_ids(rule_ids)

            # Add rules
            new_rules = [{"value": r, "tag":  r} for r in search_rules]
            rules = self.api.add_stream_rules(new_rules)
            
            # Collecting
            print("Collecting rules: %s" % ([r["value"] for r in rules["data"]]))

            event = threading.Event()
            if folder:
                file_output = folder + "/" + id + ".jsonl"
            else:
                file_output = id + ".jsonl"

            with jsonlines.open(file_output, mode="a") as writer:
                for count, result in enumerate(self.api.stream(event=event)):
                    tweet_ = flatten(result)
                    writer.write(tweet_[0])

                    if limit:
                        if count >= limit - 1:
                            event.set()

            # Deleting all rules
            rule_ids = [r["id"] for r in rules["data"]]
            self.api.delete_stream_rule_ids(rule_ids)

        except Exception as e:
            print("Collect error.")
            print(e)

    

