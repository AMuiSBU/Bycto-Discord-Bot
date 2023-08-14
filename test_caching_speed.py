import unittest
import time

import requests
from requests_cache import CachedSession
from ebay_browser import ebay_api_call


class Test_Caching_Speed(unittest.TestCase):

    def test(self):
        # Establish request details
        query = "laptop"
        limit = 1000
        session_standard = requests.Session()
        session_cache = CachedSession('api_cache', expire_after=300)
        session_cache.cache.clear()
        # Test response time for uncached API call
        start_time_uncached = time.time()
        ebay_api_call(session_standard, query, limit)
        end_time_uncached = time.time()
        response_time_uncached = end_time_uncached - start_time_uncached

        # Initial iteration to fill the cache
        ebay_api_call(session_cache, query, limit)

        # Test response time for cached API call
        average_cache_time = 0
        for i in range(10):
            start_time_cached = time.time()
            ebay_api_call(session_cache, query, limit)
            end_time_cached = time.time()
            response_time_cached = end_time_cached - start_time_cached
            average_cache_time += response_time_cached

        # Calculate time saved through caching
        average_cache_time = average_cache_time / 10
        cached_time_saved = response_time_uncached - average_cache_time
        time_saved_percentage = ((response_time_uncached - average_cache_time) / response_time_uncached) * 100
        time_saved_percentage = round(time_saved_percentage, 2)

        # Print out analysis results
        print(f"Uncached Response Time: {response_time_uncached:.6f} seconds")
        print(f"Cached Response Time: {average_cache_time:.6f} seconds")
        print(f"\nCaching Saved {cached_time_saved:.6f} seconds")
        print(f"Caching was {time_saved_percentage}% faster")

