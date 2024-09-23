import unittest
from pycron.modules.jobs.cache import Cache
import uuid
import os
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class TestCacheBasicFunctions(unittest.TestCase):

    def setUp(self) -> None:
        self.cache_id = str(uuid.uuid4())
        self.path = os.path.dirname(__file__)

    def test_cache_creation(self):

        cache = Cache(id=self.cache_id)
        self.assertEqual(cache._id, self.cache_id)
        self.assertEqual(cache.cache, {})

    def test_cache_add(self):

        cache = Cache(id=self.cache_id, prefix=self.path)

        cache.add("key", "value")
        self.assertEqual(cache.cache, {"key": "value"})

        cache.add("key", "value2")
        self.assertEqual(cache.cache, {"key": "value2"})

        cache.add("key2", {"subkey": "subvalue"})
        self.assertEqual(cache.cache, {"key": "value2", "key2": {"subkey": "subvalue"}})

        cache.add("key3", ["1", "2", "3"])
        self.assertEqual(
            cache.cache,
            {"key": "value2", "key2": {"subkey": "subvalue"}, "key3": ["1", "2", "3"]},
        )

    def test_cache_get(self):

        cache = Cache(id=self.cache_id, prefix=self.path)
        cache.add("key", "value")
        cache.add("key2", {"subkey": "subvalue"})
        cache.add("key3", ["1", "2", "3"])

        self.assertEqual(cache.get("key"), "value")
        self.assertEqual(cache.get("key2"), {"subkey": "subvalue"})
        self.assertEqual(cache.get("key3"), ["1", "2", "3"])

    def test_cache_dump_and_load(self):

        cache = Cache(id=self.cache_id, prefix=self.path)
        cache.add("key", "value")
        cache.add("key2", {"subkey": "subvalue"})
        cache.add("key3", ["1", "2", "3"])

        cache.dump()
        cache.load()

        self.assertEqual(cache.get("key"), "value")
        self.assertEqual(cache.get("key2"), {"subkey": "subvalue"})
        self.assertEqual(cache.get("key3"), ["1", "2", "3"])
