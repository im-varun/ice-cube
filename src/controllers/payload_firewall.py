import re
import unicodedata
from typing import Any


class PayloadFirewall:
    """
    A more robust security layer to validate user input payloads
    and reduce the risk of SQL injection through input validation.
    """

    def __init__(self, strict: bool = False):
        self.strict = strict

        # Dangerous meta-characters and operators
        self.blacklist_tokens = [
            ";",
            "--",
            "/*",
            "*/",
            "#",
            "@@",
            "@",
            "||",
            "%00",  # null byte
        ]

        # SQL keywords attackers commonly use
        self.blacklist_keywords = [
            "UPDATE",
            "DELETE",
            "INSERT",
            "DROP",
            "ALTER",
            "TRUNCATE",
            "EXEC",
            "UNION",
            "INTERSECT",
            "MERGE",
            "REPLACE",
            "CALL",
            "DECLARE",
            "SHUTDOWN",
        ]

        # Pre compile patterns
        self.keyword_patterns = [
            re.compile(r"\b" + kw + r"\b", re.IGNORECASE) for kw in self.blacklist_keywords
        ]

        # Common boolean-injection patterns
        self.boolean_injection_pattern = re.compile(
            r"\b(OR|AND)\b\s+[\'\"]?\w+[\'\"]?\s*=\s*[\'\"]?\w+[\'\"]?",
            re.IGNORECASE,
        )

        # Common hex-encoded SQL keywords (e.g., 0x44454C455445)
        self.hex_keyword_pattern = re.compile(r"0x[0-9a-fA-F]{4,}")

        # Common Base64-encoded SQL keywords
        self.base64_keyword_pattern = re.compile(r"(?:[A-Za-z0-9+/]{8,}={0,2})")

    def verify_payload(self, payload: dict[str, Any]) -> bool:
        if not payload or payload == {}:
            return True

        for value in payload.values():
            if value and not self._is_safe_value(value):
                return False

        return True

    def _is_safe_value(self, value: Any) -> bool:
        if isinstance(value, str):
            return self._is_safe_string(value)

        if isinstance(value, dict):
            return self.verify_payload(value)

        if isinstance(value, list):
            return all(self._is_safe_value(v) for v in value)

        return True

    def _normalize(self, s: str) -> str:
        # Unicode normalization to avoid attacks like " D R O P"
        s = unicodedata.normalize("NFKC", s)

        # Collapse whitespace
        return " ".join(s.split())

    def _is_safe_string(self, s: str) -> bool:
        s = self._normalize(s)

        # Block meta characters
        # eg- "hello; DROP TABLE users"
        if any(token in s for token in self.blacklist_tokens):
            return False

        # Block explicit SQL keywords
        # eg- "DROP TABLE accounts"
        for pattern in self.keyword_patterns:
            if pattern.search(s):
                return False

        # Block boolean-based SQL injection ("OR 1=1", "AND 'a'='a'")
        # eg- "username' OR '1'='1"
        if self.boolean_injection_pattern.search(s):
            return False

        # Block encoded attack patterns
        # eg- "0x444F50205441424C45"   (hex for "DROP TABLE")
        if self.hex_keyword_pattern.search(s):
            return False

        # Block base64 encoded patters
        # eg- "RFJPUCBUQUJMRQ=="   (base64 for "DROP TABLE")
        if self.base64_keyword_pattern.search(s):
            # decode to check for hidden SQL
            try:
                import base64

                decoded = base64.b64decode(s).decode("utf-8", "ignore")
                for kw in self.blacklist_keywords:
                    if kw.lower() in decoded.lower():
                        return False
            except Exception:
                pass  # not valid base64, so ignore

        # Strict mode (only letters, digits, _, -, space)
        # eg- "hello$world" not allowed
        if self.strict:
            if not re.fullmatch(r"[A-Za-z0-9 _.-]*", s):
                return False

        return True
