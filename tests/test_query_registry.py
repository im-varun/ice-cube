"""
Tests for QueryRegistry - query metadata and enum management.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from query_registry import Query, QueryInfo


class TestQueryInfo:
    """Tests for QueryInfo dataclass."""

    def test_query_info_creation(self):
        """Should create QueryInfo with all fields."""
        info = QueryInfo(
            id="test_query",
            title="Test Query",
            description="A test query",
            needs_payload=True,
            payload_labels=["param1", "param2"],
        )
        assert info.id == "test_query"
        assert info.title == "Test Query"
        assert info.needs_payload is True
        assert len(info.payload_labels) == 2

    def test_query_info_no_payload(self):
        """Should create QueryInfo without payload requirements."""
        info = QueryInfo(
            id="simple",
            title="Simple Query",
            description="No params needed",
            needs_payload=False,
            payload_labels=None,
        )
        assert info.needs_payload is False
        assert info.payload_labels is None

    def test_query_info_frozen(self):
        """QueryInfo should be immutable (frozen dataclass)."""
        info = Query.HEAD_TO_HEAD.value
        try:
            info.id = "changed"
            raise AssertionError("Should have raised error")
        except Exception:
            pass  # Expected


class TestQueryEnum:
    """Tests for Query enum."""

    def test_head_to_head_exists(self):
        """HEAD_TO_HEAD query should exist."""
        assert Query.HEAD_TO_HEAD is not None
        assert Query.HEAD_TO_HEAD.value.id == "head_to_head"

    def test_all_queries_have_required_fields(self):
        """All queries should have required fields."""
        for query in Query:
            info = query.value
            assert info.id is not None
            assert info.title is not None
            assert info.description is not None
            assert isinstance(info.needs_payload, bool)

    def test_queries_with_payload_have_labels(self):
        """Queries needing payload should have labels."""
        for query in Query:
            info = query.value
            if info.needs_payload:
                assert info.payload_labels is not None
                assert len(info.payload_labels) > 0


class TestQueryFromId:
    """Tests for Query.from_id classmethod."""

    def test_from_id_returns_query(self):
        """Should return correct Query from ID string."""
        query = Query.from_id("head_to_head")
        assert query == Query.HEAD_TO_HEAD

    def test_from_id_birthday_curse(self):
        """Should find birthday curse query."""
        query = Query.from_id("birthday_curse")
        assert query == Query.BIRTHDAY_CURSE

    def test_from_id_invalid_raises(self):
        """Invalid ID should raise ValueError."""
        try:
            Query.from_id("not_a_real_query")
            raise AssertionError("Should have raised ValueError")
        except ValueError as e:
            assert "Unknown query ID" in str(e)


class TestQueryGetInfo:
    """Tests for Query.get_info classmethod."""

    def test_get_info_returns_queryinfo(self):
        """Should return QueryInfo for valid ID."""
        info = Query.get_info("head_to_head")
        assert isinstance(info, QueryInfo)
        assert info.title == "Head to Head Duel"

    def test_get_info_invalid_raises(self):
        """Invalid ID should raise ValueError."""
        try:
            Query.get_info("fake_query")
            raise AssertionError("Should have raised ValueError")
        except ValueError:
            pass


class TestQueryListQueries:
    """Tests for Query.list_queries classmethod."""

    def test_list_returns_all_queries(self):
        """Should return list of all Query enums."""
        queries = Query.list_queries()
        assert len(queries) > 0
        assert Query.HEAD_TO_HEAD in queries
        assert Query.BIRTHDAY_CURSE in queries

    def test_list_contains_only_valid_queries(self):
        """All items should be Query enums with QueryInfo values."""
        for query in Query.list_queries():
            assert isinstance(query, Query)
            assert isinstance(query.value, QueryInfo)


class TestQueryTitles:
    """Tests for Query.titles classmethod."""

    def test_titles_returns_strings(self):
        """Should return list of title strings."""
        titles = Query.titles()
        assert isinstance(titles, list)
        assert all(isinstance(t, str) for t in titles)

    def test_titles_contains_expected(self):
        """Should contain known query titles."""
        titles = Query.titles()
        assert "Head to Head Duel" in titles
        assert "Birthday Curse Analysis" in titles
        assert "Longest Games" in titles
