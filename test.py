import ast
import operator


_BINARY_OPERATORS = {
	ast.Add: operator.add,
	ast.Sub: operator.sub,
	ast.Mult: operator.mul,
	ast.Div: operator.truediv,
	ast.FloorDiv: operator.floordiv,
	ast.Mod: operator.mod,
	ast.Pow: operator.pow,
}
_UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def calculate(expression):
	"""Evaluate a basic arithmetic expression without using eval()."""
	try:
		tree = ast.parse(expression, mode="eval")
	except SyntaxError as exc:
		raise ValueError("Invalid expression") from exc

	def evaluate(node):
		if isinstance(node, ast.Expression):
			return evaluate(node.body)
		if isinstance(node, ast.Constant) and type(node.value) in (int, float):
			return node.value
		if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
			left, right = evaluate(node.left), evaluate(node.right)
			if isinstance(node.op, ast.Pow) and abs(right) > 1000:
				raise ValueError("Exponent is too large")
			return _BINARY_OPERATORS[type(node.op)](left, right)
		if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
			return _UNARY_OPERATORS[type(node.op)](evaluate(node.operand))
		raise ValueError("Only numbers and basic arithmetic operators are allowed")

	return evaluate(tree)


def main():
	print("Calculator (+, -, *, /, //, %, **). Type 'quit' to exit.")
	while True:
		expression = input("> ").strip()
		if expression.lower() in {"quit", "exit", "q"}:
			break
		if not expression:
			continue
		try:
			print(calculate(expression))
		except (ValueError, ArithmeticError) as exc:
			print(f"Error: {exc}")


if __name__ == "__main__":
	main()

print("Hello world")