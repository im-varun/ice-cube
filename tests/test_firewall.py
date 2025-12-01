import os
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from controllers.payload_firewall import PayloadFirewall


def test_firewall():
    firewall = PayloadFirewall()

    # Test cases
    safe_payloads = [
        {"name": "Connor McDavid"},
        {"team": "Edmonton Oilers", "year": 2023},
        {"query": "SELECT * FROM players"},  # This might fail if I block SELECT, but I didn't.
        {"nested": {"name": "Sidney Crosby"}},
        {"list": ["Ovechkin", "Matthews"]},
    ]

    unsafe_payloads = [
        {"name": "Connor; DROP TABLE players"},
        {"name": "Connor -- comment"},
        {"name": "/* comment */"},
        {"query": "DELETE FROM players"},
        {"query": "UPDATE players SET name='Hacked'"},
        {"nested": {"name": "Connor; DROP TABLE players"}},
        {"list": ["Ovechkin", "Matthews; DROP TABLE players"]},
    ]

    print("Testing Safe Payloads...")
    for p in safe_payloads:
        if firewall.verify_payload(p):
            print(f"PASS: {p}")
        else:
            print(f"FAIL: {p} was blocked but should be safe")

    print("\nTesting Unsafe Payloads...")
    for p in unsafe_payloads:
        if not firewall.verify_payload(p):
            print(f"PASS: {p} was blocked")
        else:
            print(f"FAIL: {p} was NOT blocked")


if __name__ == "__main__":
    test_firewall()
