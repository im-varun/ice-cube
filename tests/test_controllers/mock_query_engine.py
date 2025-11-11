# tests/test_controllers/mock_query_engine.py
class MockQueryEngine:
    def execute_query(self, request: QueryRequest) -> QueryResponse:
        return QueryResponse(
            success=True,
            data=[{"id": 1, "name": "Gretzky"}],
            rows_affected=1
        )