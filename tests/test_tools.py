"""Unit tests for the tools package."""

import pytest
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Calculator tool tests
# ---------------------------------------------------------------------------

class TestCalculator:
      """Tests for the calculator tool."""

    def test_basic_addition(self):
              from tools.calculator import calculate
              result = calculate("2 + 3")
              assert result == 5

    def test_basic_subtraction(self):
              from tools.calculator import calculate
              result = calculate("10 - 4")
              assert result == 6

    def test_multiplication(self):
              from tools.calculator import calculate
              result = calculate("6 * 7")
              assert result == 42

    def test_division(self):
              from tools.calculator import calculate
              result = calculate("15 / 3")
              assert result == 5.0

    def test_division_by_zero(self):
              from tools.calculator import calculate
              with pytest.raises((ZeroDivisionError, ValueError)):
                            calculate("10 / 0")

          def test_complex_expression(self):
                    from tools.calculator import calculate
                    result = calculate("(2 + 3) * 4")
                    assert result == 20


# ---------------------------------------------------------------------------
# File reader tool tests
# ---------------------------------------------------------------------------

class TestFileReader:
      """Tests for the file reader tool."""

    def test_read_existing_file(self, tmp_path):
              from tools.file_reader import read_file
              test_file = tmp_path / "test.txt"
              test_file.write_text("Hello, World!")
              result = read_file(str(test_file))
              assert "Hello, World!" in result

    def test_read_nonexistent_file(self):
              from tools.file_reader import read_file
              with pytest.raises((FileNotFoundError, IOError, Exception)):
                            read_file("/nonexistent/path/file.txt")

          def test_read_empty_file(self, tmp_path):
                    from tools.file_reader import read_file
                    test_file = tmp_path / "empty.txt"
                    test_file.write_text("")
                    result = read_file(str(test_file))
                    assert result == "" or result is not None


# ---------------------------------------------------------------------------
# Tool registry tests
# ---------------------------------------------------------------------------

class TestToolRegistry:
      """Tests for the tool registry."""

    def test_registry_has_tools(self):
              from tools.tool_registry import ToolRegistry
              registry = ToolRegistry()
              tools = registry.get_all_tools()
              assert len(tools) > 0

    def test_registry_get_tool_by_name(self):
              from tools.tool_registry import ToolRegistry
              registry = ToolRegistry()
              tool = registry.get_tool("calculate")
              assert tool is not None

    def test_registry_unknown_tool_returns_none(self):
              from tools.tool_registry import ToolRegistry
              registry = ToolRegistry()
              tool = registry.get_tool("nonexistent_tool")
              assert tool is None


# ---------------------------------------------------------------------------
# Summarize tool tests
# ---------------------------------------------------------------------------

class TestSummarize:
      """Tests for the summarize tool."""

    @patch("tools.summarize.boto3")
    def test_summarize_returns_string(self, mock_boto3):
              """Summarize should call Bedrock and return a string summary."""
              mock_client = MagicMock()
              mock_boto3.client.return_value = mock_client
              mock_client.invoke_model.return_value = {
                  "body": MagicMock(read=lambda: b'{"completion": "Summary text"}')
              }

        from tools.summarize import summarize_text
        result = summarize_text("Some long text to summarize")
        assert isinstance(result, str)

    def test_summarize_empty_input(self):
              from tools.summarize import summarize_text
              with pytest.raises((ValueError, Exception)):
                            summarize_text("")


# ---------------------------------------------------------------------------
# Lambda handler tests
# ---------------------------------------------------------------------------

class TestLambdaHandler:
      """Tests for the Lambda API handler."""

    def test_missing_input_returns_400(self):
              import json
              from api.lambda_handler import handler
              event = {"body": json.dumps({})}
              response = handler(event, None)
              assert response["statusCode"] == 400

    def test_invalid_json_body_returns_400(self):
              from api.lambda_handler import handler
              event = {"body": "not-valid-json"}
              response = handler(event, None)
              assert response["statusCode"] == 400

    @patch("api.lambda_handler.SupervisorAgent")
    def test_valid_request_returns_200(self, mock_supervisor_cls):
              import json
              mock_supervisor = MagicMock()
              mock_supervisor.run.return_value = {"answer": "42"}
              mock_supervisor_cls.return_value = mock_supervisor

        from api.lambda_handler import handler
        event = {"body": json.dumps({"input": "What is the answer?"})}
        response = handler(event, None)
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert "result" in body
