import unittest
from src import serialize_resp, deserialize_resp

class TestRESPProtocol(unittest.TestCase):

    def test_deserialize_simple_string(self):
        self.assertEqual(deserialize_resp(b"+OK\r\n")[0], "OK")

    def test_deserialize_errors(self):
        self.assertEqual(deserialize_resp(b"-Error message\r\n")[0], "Error message")

    def test_deserialize_integers(self):
        self.assertEqual(deserialize_resp(b":1000\r\n")[0], 1000)

    def test_deserialize_bulk_strings(self):
        self.assertEqual(deserialize_resp(b"$6\r\nfoobar\r\n")[0], "foobar")
        self.assertEqual(deserialize_resp(b"$0\r\n\r\n")[0], "")
        self.assertEqual(deserialize_resp(b"$-1\r\n")[0], None)

    def test_deserialize_arrays(self):
        self.assertEqual(deserialize_resp(b"*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n")[0], ["foo", "bar"])

    def test_serialize_simple_string(self):
        self.assertEqual(serialize_resp("OK"), b"+OK\r\n")

    def test_serialize_errors(self):
        self.assertEqual(serialize_resp("Error message"), b"+Error message\r\n")

    def test_serialize_integers(self):
        self.assertEqual(serialize_resp(1000), b":1000\r\n")

    def test_serialize_bulk_strings(self):
        self.assertEqual(serialize_resp("foobar"), b"+foobar\r\n")
        self.assertEqual(serialize_resp(""), b"$0\r\n\r\n")
        self.assertEqual(serialize_resp(None), b"$-1\r\n")

    def test_serialize_arrays(self):
        self.assertEqual(serialize_resp(["foo", "bar"]), b"*2\r\n+foo\r\n+bar\r\n")


if __name__ == '__main__':
    unittest.main()
