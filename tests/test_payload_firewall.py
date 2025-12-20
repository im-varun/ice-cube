"""
Tests for PayloadFirewall - SQL injection protection layer.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from controllers.payload_firewall import PayloadFirewall


class TestPayloadFirewallBasic:
    """Basic functionality tests for PayloadFirewall."""

    def test_empty_payload_is_safe(self):
        """Empty payloads should always pass validation."""
        firewall = PayloadFirewall()
        assert firewall.verify_payload({}) is True
        assert firewall.verify_payload(None) is True

    def test_normal_input_passes(self):
        """Regular text input should pass."""
        firewall = PayloadFirewall()
        payload = {"name": "Connor McDavid", "team": "Edmonton Oilers"}
        assert firewall.verify_payload(payload) is True

    def test_numeric_values_pass(self):
        """Numeric values should pass validation."""
        firewall = PayloadFirewall()
        payload = {"goals": 50, "assists": 67, "games": 82}
        assert firewall.verify_payload(payload) is True


class TestPayloadFirewallBlocking:
    """Tests for blocking malicious input."""

    def test_blocks_semicolon(self):
        """Semicolons should be blocked."""
        firewall = PayloadFirewall()
        payload = {"query": "SELECT * FROM users; DROP TABLE users"}
        assert firewall.verify_payload(payload) is False

    def test_blocks_comment_syntax(self):
        """SQL comment syntax should be blocked."""
        firewall = PayloadFirewall()
        assert firewall.verify_payload({"input": "test -- comment"}) is False
        assert firewall.verify_payload({"input": "test /* comment */"}) is False

    def test_blocks_drop_keyword(self):
        """DROP keyword should be blocked."""
        firewall = PayloadFirewall()
        payload = {"query": "DROP TABLE players"}
        assert firewall.verify_payload(payload) is False

    def test_blocks_union_keyword(self):
        """UNION keyword should be blocked."""
        firewall = PayloadFirewall()
        payload = {"query": "SELECT * FROM game UNION SELECT * FROM users"}
        assert firewall.verify_payload(payload) is False

    def test_blocks_delete_keyword(self):
        """DELETE keyword should be blocked."""
        firewall = PayloadFirewall()
        payload = {"query": "DELETE FROM players"}
        assert firewall.verify_payload(payload) is False

    def test_blocks_boolean_injection(self):
        """Boolean injection patterns should be blocked."""
        firewall = PayloadFirewall()
        payload = {"username": "admin' OR '1'='1"}
        assert firewall.verify_payload(payload) is False

    def test_blocks_or_equals_pattern(self):
        """OR 1=1 pattern should be blocked."""
        firewall = PayloadFirewall()
        payload = {"input": "test OR 1=1"}
        assert firewall.verify_payload(payload) is False


class TestPayloadFirewallNested:
    """Tests for nested payload validation."""

    def test_nested_dict_validation(self):
        """Nested dictionaries should be validated."""
        firewall = PayloadFirewall()
        payload = {
            "player": {"name": "Sidney Crosby", "team": "Pittsburgh Penguins"},
            "stats": {"goals": 30, "assists": 60},
        }
        assert firewall.verify_payload(payload) is True

    def test_nested_malicious_blocked(self):
        """Malicious input in nested dicts should be blocked."""
        firewall = PayloadFirewall()
        payload = {
            "player": {"name": "test; DROP TABLE players"},
        }
        assert firewall.verify_payload(payload) is False

    def test_list_values_validated(self):
        """Lists should have each element validated."""
        firewall = PayloadFirewall()
        payload = {"players": ["Connor McDavid", "Sidney Crosby"]}
        assert firewall.verify_payload(payload) is True

    def test_list_with_malicious_blocked(self):
        """Lists with malicious elements should be blocked."""
        firewall = PayloadFirewall()
        payload = {"players": ["Connor McDavid", "test; DROP"]}
        assert firewall.verify_payload(payload) is False


class TestPayloadFirewallStrict:
    """Tests for strict mode validation."""

    def test_strict_mode_blocks_special_chars(self):
        """Strict mode blocks special characters."""
        firewall = PayloadFirewall(strict=True)
        payload = {"input": "test$value"}
        assert firewall.verify_payload(payload) is False

    def test_strict_mode_allows_alphanumeric(self):
        """Strict mode allows alphanumeric and basic chars."""
        firewall = PayloadFirewall(strict=True)
        payload = {"input": "Connor McDavid 97"}
        assert firewall.verify_payload(payload) is True


class TestPayloadFirewallEdgeCases:
    """Edge case tests."""

    def test_case_insensitive_keyword_blocking(self):
        """Keywords should be blocked regardless of case."""
        firewall = PayloadFirewall()
        assert firewall.verify_payload({"x": "drop table"}) is False
        assert firewall.verify_payload({"x": "DROP TABLE"}) is False
        assert firewall.verify_payload({"x": "DrOp TaBlE"}) is False

    def test_allows_safe_hockey_terms(self):
        """Common hockey terms should pass."""
        firewall = PayloadFirewall()
        terms = ["power play", "penalty kill", "hat trick", "overtime"]
        for term in terms:
            assert firewall.verify_payload({"term": term}) is True
