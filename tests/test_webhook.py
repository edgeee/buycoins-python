import json


def test_verify_webhook_payload():
    from buycoins import webhook

    webhook_token = "webhook-token"
    body = json.dumps(
        dict(
            hook_id=10,
            hook_key="d814153e-2ced-4d81-82f1-327d000a3ca2",
            payload=dict(event="coins.incoming"),
        )
    ).encode("utf-8")
    header_signature = "4d9db82c8f4fa74f9282c694b7780b80ab466a6f"

    assert webhook.verify_payload(body, webhook_token, header_signature)
