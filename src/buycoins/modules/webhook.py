import hashlib
import hmac


def verify_payload(body: bytes, webhook_token: str, header_signature: str) -> bool:
    signing_key = webhook_token.encode("utf-8")
    if not isinstance(body, bytes):
        body = bytes(body)

    hashed = hmac.new(signing_key, body, hashlib.sha1)
    return hashed.hexdigest() == header_signature
