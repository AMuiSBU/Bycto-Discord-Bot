import unittest
import time
from requests_cache import CachedSession
from ebay_browser import ebay_api_call


class Test_Caching_Speed(unittest.TestCase):
    def setUp(self):
        # Clear Cache for testing
        session = CachedSession('http_cache', backend='sqlite', expire_after=300)
        session.cache.clear()

    def test(self):
        # Establish request details
        query = "laptop"
        limit = 100

        # Test response time for uncached API call
        start_time_uncached = time.time()
        ebay_api_call(query, limit)
        end_time_uncached = time.time()
        response_time_uncached = end_time_uncached - start_time_uncached

        # Test response time for cached API call
        start_time_cached = time.time()
        ebay_api_call(query, limit)
        end_time_cached = time.time()
        response_time_cached = end_time_cached - start_time_cached

        # Calculate time saved through caching
        cached_time_saved = response_time_uncached - response_time_cached

        # Print out analysis results
        print(f"Uncached Response Time: {response_time_uncached:.6f} seconds")
        print(f"Cached Response Time: {response_time_cached:.6f} seconds")
        print(f"\nCaching Saved {cached_time_saved:.6f} seconds")

