from alerts_ai.core.security import hash_password, verify_password


def test_hash_roundtrip():
    stored = hash_password("12345678")
    assert verify_password("12345678", stored)
    assert not verify_password("wrong", stored)
    assert stored != hash_password("12345678")  # salted
