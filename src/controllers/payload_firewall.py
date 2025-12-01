import re
from typing import Any


class PayloadFirewall:
    """
    A security layer to validate user input payloads and prevent SQL injection attacks.

    This firewall inspects dictionaries (and nested structures) for:
    1. Dangerous characters (e.g., ';', '--', '/*')
    2. SQL keywords used in malicious contexts (e.g., 'DROP', 'DELETE')
    """

    def __init__(self):
        # Characters that are often used to chain commands or comment out code
        self.blacklist_chars = [";", "--", "/*", "*/", "xp_"]

        # SQL keywords that should not appear in user input
        # We use word boundaries to avoid false positives (e.g., "UPDATE" in "UPDATED")
        self.blacklist_keywords = [
            "DROP",
            "DELETE",
            "INSERT",
            "UPDATE",
            "ALTER",
            "TRUNCATE",
            "UNION",
            "EXEC",
            "SHUTDOWN",
        ]

        # Pre-compile regex patterns
        self.keyword_patterns = [
            re.compile(r"\b" + keyword + r"\b", re.IGNORECASE)
            for keyword in self.blacklist_keywords
        ]

    def verify_payload(self, payload: dict[str, Any]) -> bool:
        """
        Recursively verifies that the payload does not contain malicious content.

        Args:
            payload: The input dictionary to verify.

        Returns:
            bool: True if the payload is safe, False if a threat is detected.
        """
        if not payload:
            return True

        for value in payload.values():
            if not self._is_safe_value(value):
                return False

        return True

    def _is_safe_value(self, value: Any) -> bool:
        """
        Check if a single value (string, list, or dict) is safe.
        """
        if isinstance(value, str):
            return self._is_safe_string(value)

        elif isinstance(value, dict):
            return self.verify_payload(value)

        elif isinstance(value, list):
            for item in value:
                if not self._is_safe_value(item):
                    return False

        return True

    def _is_safe_string(self, value: str) -> bool:
        """
        Check if a string contains any blacklisted characters or keywords.
        """
        # Check for blacklisted characters
        for char in self.blacklist_chars:
            if char in value:
                return False

        # Check for blacklisted keywords using regex (whole words only)
        for pattern in self.keyword_patterns:
            if pattern.search(value):
                return False

        return True
