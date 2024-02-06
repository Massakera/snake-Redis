import unittest

from serialisers.serialisers import deserialize_resp, serialize_resp

class TestRESPSerialization(unittest.TestCase):
    def test_bulk_string_null(self):
        self.assertEqual(serialize_resp(None), "$-1\r\n")

    def test_simple_string(self):
        self.assertEqual(serialize_resp("+OK"), "+OK\r\n")

    def test_error(self):
        self.assertEqual(serialize_resp("-Error message"), "-Error message\r\n")

    def test_integer(self):
        self.assertEqual(serialize_resp(123), ":123\r\n")

    def test_bulk_string_empty(self):
        self.assertEqual(serialize_resp(""), "$0\r\n\r\n")

    def test_bulk_string_hello_world(self):
        self.assertEqual(serialize_resp("hello world"), "$11\r\nhello world\r\n")

    def test_array_of_bulk_strings(self):
        self.assertEqual(serialize_resp(["ping"]), "*1\r\n$4\r\nping\r\n")

    def test_array_with_multiple_bulk_strings(self):
        self.assertEqual(serialize_resp(["echo", "hello world"]), "*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n")

    def test_deserialize_bulk_string_null(self):
        self.assertIsNone(deserialize_resp("$-1\r\n"))

if __name__ == "__main__":
    unittest.main()
