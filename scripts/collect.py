

from itertools import count
from twarc.client2 import Twarc2
import threading
import jsonlines
import datetime
import math

import pytz


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

    def search_archive(self, query, id="collecting_search", max_per_request=10, folder=None, time={"end": datetime.datetime.now(tz=pytz.timezone("UTC")), "delta": 1, "delta_type": "minute"}):
        
        try: 
            
            end_ = time["end"]
            
            if time["delta_type"] == "hour":
                start_ = end_ - datetime.timedelta(hours=time["delta"])
            elif time["delta_type"] == "minute":
                start_ = end_ - datetime.timedelta(minutes=time["delta"])
            else: 
                raise Exception("Choose one option for delta_type: hour, minute or second.")
            
            print("Start search: %s " % datetime.datetime.strftime(start_, "%d/%m/%Y %H:%M:%S"))
            print("End Search: %s " % datetime.datetime.strftime(end_, "%d/%m/%Y %H:%M:%S"))
            
            if folder:
                file_output = folder + "/" + id 
            else:
                file_output = id 

            for response_page in self.api.counts_all(query,start_time=start_, end_time=end_, granularity=time["delta_type"]):
                counts = response_page["data"]
            

            total_count = 0
            file_id = 0
            for count_ in counts:
                end_count = datetime.datetime.strptime(count_['end'], "%Y-%m-%dT%H:%M:%S.000Z")
                start_count = datetime.datetime.strptime(count_['start'], "%Y-%m-%dT%H:%M:%S.000Z")

                number_of_pages = count_['tweet_count'] / max_per_request

                start_count_str = datetime.datetime.strftime(start_count, "%d/%m/%Y %H:%M:%S")
                end_count_str = datetime.datetime.strftime(end_count, "%d/%m/%Y %H:%M:%S")
                print("Collecting %i tweets from %s to %s" % (count_['tweet_count'], start_count_str, end_count_str))
                
                
                
                pages = 0
                found_tweets = 0
                for response_page in self.api.search_all(query, sort_order='recency', max_results=max_per_request, start_time=start_count, end_time=end_count):
                    pages += 1

                    file_output_id = file_output + "_" + str(file_id) + "_page" + str(pages) + ".jsonl"
                    
                    tweets = flatten(response_page)

                    found_tweets += len(tweets)
                    

                    print("\tPage %i: %i tweets collected " % (pages, len(tweets)))

                    with jsonlines.open(file_output_id, mode="a") as writer:
                        writer.write_all(tweets)


                    if pages == number_of_pages:
                        break

                print("Total collected: %i" % found_tweets)
                total_count += found_tweets
                file_id += 1

            print("Total collected of all search: %i" % total_count)
            
            


        except Exception as e:
            print("Collecting error")
            print(e)

    

    def search(self, query, limit_pages=1, id="collecting_search", max_per_request=10, folder=None):
        pages = 0
        found_tweets = 0
        try:

            if folder:
                file_output = folder + "/" + id
            else:
                file_output = id + ".jsonl"

            # Collecting
            print("Collecting query: %s" % (query))

            for response_page in self.api.search_recent(query, sort_order='recency',max_results=max_per_request):
                pages += 1

                print("\tPage %i: " % pages, end=' ')

                tweets = flatten(response_page)

                file_output_id = file_output + "_page" + str(pages) + ".jsonl"
                
                found_tweets += len(tweets)

                print("%i tweets collected." % len(tweets))

                with jsonlines.open(file_output_id, mode="a") as writer:
                    writer.write_all(tweets)


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

    

