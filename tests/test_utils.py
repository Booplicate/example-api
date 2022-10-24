"""
Test cases for utils
"""

import unittest
# import asyncio

from example_api.utils import create_async_cache


class AsyncCacheTestCase(unittest.IsolatedAsyncioTestCase):
    """
    Test case for create_async_cache
    """
    async def test_cache(self):
        obj = object()
        counter = 0
        MAX_CACHE_SIZE = 2

        @create_async_cache(MAX_CACHE_SIZE)
        async def test_func(param):
            nonlocal counter
            counter += 1
            return param

        with self.subTest("Verify empty cache"):
            self.assertEqual(len(test_func.__cache__), 0)

        result = await test_func(obj)

        with self.subTest("Verify correct result"):
            self.assertIs(result, obj)

        with self.subTest("Verify cache size 1"):
            self.assertEqual(len(test_func.__cache__), 1)

        for i in range(3):
            with self.subTest("Verify counter", i=i):
                self.assertEqual(counter, 1)

        for i in range(2):
            await test_func(object())
            with self.subTest("Verify cache size 2", i=i):
                self.assertEqual(len(test_func.__cache__), 2)

            if i == 0:
                with self.subTest("Verify old cache exists", i=i):
                    self.assertIn(obj, test_func.__cache__.values())

            elif i == 1:
                with self.subTest("Verify old cache gone", i=i):
                    self.assertNotIn(obj, test_func.__cache__.values())

        with self.subTest("Verify counter"):
            self.assertEqual(counter, 3)

    async def test_clear_key(self):
        @create_async_cache(10)
        async def test_func(param):
            return param

        VAR_1 = 1.0
        VAR_2 = "2"
        VAR_3 = 3
        VAR_4 = object()

        await test_func(VAR_4)
        await test_func(VAR_3)
        await test_func(VAR_2)
        await test_func(VAR_1)

        with self.subTest("Verify all cache exists"):
            for i in (VAR_1, VAR_2, VAR_3, VAR_4):
                self.assertIn(i, test_func.__cache__.values())

        test_func.clear_key(VAR_2)

        with self.subTest(f"Verify {VAR_1}, {VAR_3}, {VAR_4} cache exists"):
            for i in (VAR_1, VAR_3, VAR_4):
                self.assertIn(i, test_func.__cache__.values())

        with self.subTest(f"Verify {VAR_2} cache doesn't exist"):
            self.assertNotIn(VAR_2, test_func.__cache__.values())

        test_func.clear_key(VAR_4)

        with self.subTest(f"Verify {VAR_4} cache doesn't exist"):
            self.assertNotIn(VAR_4, test_func.__cache__.values())

    async def test_clear_all(self):
        MAX_SIZE = 5
        @create_async_cache(MAX_SIZE)
        async def test_func(param):
            return param

        for i in range(MAX_SIZE):
            await test_func(i)

        with self.subTest("Verify cache full"):
            self.assertEqual(len(test_func.__cache__), MAX_SIZE)

        test_func.clear_all()

        with self.subTest("Verify cache empty"):
            self.assertEqual(len(test_func.__cache__), 0)
