"""AWS Lambda handler for the multi-agent orchestration serverless API."""

import json
import logging
import os
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
      """
          AWS Lambda entry point for the multi-agent orchestration API.

              Args:
                      event: API Gateway event containing the HTTP request details.
                              context: Lambda context object with runtime information.

                                  Returns:
                                          API Gateway response with statusCode and body.
                                              """
      try:
                logger.info("Received event: %s", json.dumps(event))

          # Parse the request body
                body = event.get("body", "{}")
                if isinstance(body, str):
                              body = json.loads(body)

                user_input = body.get("input", "")
                session_id = body.get("session_id", "default")

          if not user_input:
                        return _response(400, {"error": "Missing required field: input"})

        # Import supervisor here to avoid cold-start penalty at module level
        from agents.supervisor import SupervisorAgent

        supervisor = SupervisorAgent()
        result = supervisor.run(user_input=user_input, session_id=session_id)

        return _response(200, {"session_id": session_id, "result": result})

except json.JSONDecodeError as exc:
        logger.error("Invalid JSON in request body: %s", exc)
        return _response(400, {"error": "Invalid JSON in request body"})
except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Unhandled exception in Lambda handler")
        return _response(500, {"error": str(exc)})


def _response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
      """Build a standard API Gateway response."""
    return {
              "statusCode": status_code,
              "headers": {
                            "Content-Type": "application/json",
                            "Access-Control-Allow-Origin": "*",
              },
              "body": json.dumps(body),
    }
