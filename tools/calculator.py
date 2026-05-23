"""Tool 5: Calculator."""
import ast, operator, logging
logger = logging.getLogger(__name__)
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
                ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
                ast.USub: operator.neg}

def _eval(node):
      if isinstance(node, ast.Constant): return node.value
            if isinstance(node, ast.BinOp):
                      return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
                  if isinstance(node, ast.UnaryOp):
                            return _OPS[type(node.op)](_eval(node.operand))
                        raise ValueError(f"Unsupported: {type(node)}")

def calculate(expression: str) -> str:
      """Evaluate a math expression safely."""
    try:
              result = _eval(ast.parse(expression, mode="eval").body)
              return f"{expression} = {result}"
except ZeroDivisionError: return "Error: Division by zero."
except Exception as e: return f"Calculation error: {e}"
—
