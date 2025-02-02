from unittest import TestCase

from qh3.quic.retry import QuicRetryTokenHandler


class QuicRetryTokenHandlerTest(TestCase):
    def test_retry_token(self):
        addr = ("127.0.0.1", 1234)
        original_destination_connection_id = b"\x08\x07\x06\05\x04\x03\x02\x01"
        retry_source_connection_id = b"abcdefgh"

        handler = QuicRetryTokenHandler()

        # create token
        token = handler.create_token(
            addr, original_destination_connection_id, retry_source_connection_id
        )
        self.assertIsNotNone(token)

        # validate token - ok
        self.assertEqual(
            handler.validate_token(addr, token),
            (original_destination_connection_id, retry_source_connection_id),
        )

        # validate token - empty
        with self.assertRaises(ValueError) as cm:
            handler.validate_token(addr, b"")
        self.assertEqual(
            str(cm.exception), "Ciphertext length must be equal to key size."
        )

        # validate token - wrong address
        with self.assertRaises(ValueError) as cm:
            handler.validate_token(("1.2.3.4", 12345), token)
        self.assertEqual(str(cm.exception), "Remote address does not match.")
