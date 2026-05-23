"""Sandboxed Python code execution tool for the multi-agent platform."""

import ast
import builtins
import contextlib
import io
import os
import signal
import traceback
from typing import Any, Dict


# Allowed built-in names (restricted safe set)
_SAFE_BUILTINS = {
      name: getattr(builtins, name)
      for name in (
                "abs", "all", "any", "bin", "bool", "bytes", "callable", "chr",
                "dict", "dir", "divmod", "enumerate", "filter", "float", "format",
                "frozenset", "getattr", "hasattr", "hash", "hex", "int", "isinstance",
                "issubclass", "iter", "len", "list", "map", "max", "min", "next",
                "oct", "ord", "pow", "print", "range", "repr", "reversed", "round",
                "set", "slice", "sorted", "str", "sum", "tuple", "type", "zip",
      )
}
_SAFE_BUILTINS["__builtins__"] = {}

_TIMEOUT_SECONDS = int(os.environ.get("CODE_EXECUTOR_TIMEOUT", "10"))


def _timeout_handler(signum, frame):  # noqa: ANN001
      raise TimeoutError(f"Code execution timed out after {_TIMEOUT_SECONDS} seconds.")


def execute_code(code: str, timeout: int = _TIMEOUT_SECONDS) -> Dict[str, Any]:
      """
          Execute Python *code* in a restricted sandbox and return the result.

              Args:
                      code: Python source code string to execute.
                              timeout: Maximum execution time in seconds (default from env).

                                  Returns:
                                          A dict with keys:
                                                    - ``stdout`` (str): captured standard output
                                                              - ``result`` (Any): value of the last expression, or None
                                                                        - ``error`` (str | None): exception message if execution failed
                                                                            """
      if not code or not code.strip():
                return {"stdout": "", "result": None, "error": "Empty code provided."}

      # Syntax check
      try:
                tree = ast.parse(code, mode="exec")
except SyntaxError as exc:
        return {"stdout": "", "result": None, "error": f"SyntaxError: {exc}"}

    stdout_buffer = io.StringIO()
    local_ns: Dict[str, Any] = {}
    result = None

    # Register timeout on POSIX systems
    use_signal = hasattr(signal, "SIGALRM")
    if use_signal:
              signal.signal(signal.SIGALRM, _timeout_handler)
              signal.alarm(timeout)

    try:
              with contextlib.redirect_stdout(stdout_buffer):
                            exec(compile(tree, "<sandbox>", "exec"), {"__builtins__": _SAFE_BUILTINS}, local_ns)  # noqa: S102

        # Capture the value of the last expression if it is an Expr node
              if tree.body and isinstance(tree.body[-1], ast.Expr):
                            last_expr = ast.Expression(body=tree.body[-1].value)
                            result = eval(compile(last_expr, "<sandbox>", "eval"), {"__builtins__": _SAFE_BUILTINS}, local_ns)  # noqa: S307, S eval

except TimeoutError as exc:
          return {"stdout": stdout_buffer.getvalue(), "result": None, "error": str(exc)}
except Exception:  # noqa: BLE001
          return {
                        "stdout": stdout_buffer.getvalue(),
                        "result": None,
                        "error": traceback.format_exc(),
          }
finally:
          if use_signal:
                        signal.alarm(0)

      return {"stdout": stdout_buffer.getvalue(), "result": result, "error": None}
