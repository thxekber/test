"""A small interactive command-line calculator."""
import math
import operator

OPERATORS = {
	"+": operator.add,
	"-": operator.sub,
	"*": operator.mul,
	"/": operator.truediv,
	"//": operator.floordiv,
	"%": operator.mod,
	"**": operator.pow,
}

CONSTANTS = {
	"pi": math.pi,
	"e": math.e,
}

class Calculator:
	"""Evaluate basic arithmetic and retain a session history."""

	def __init__(self):
		self.history = []

	@staticmethod
	def parse_value(text):
		"""Parse a numeric value or a supported constant."""
		value = text.strip().lower()
		if value in CONSTANTS:
			return CONSTANTS[value]
		return float(value)

	@staticmethod
	def format_value(value):
		"""Format results without unnecessary decimal places."""
		if isinstance(value, float) and value.is_integer():
			return str(int(value))
		return f"{value:.12g}" if isinstance(value, float) else str(value)

	def calculate(self, expression):
		"""Evaluate an expression containing two values and an operator."""
		parts = expression.split()
		if len(parts) != 3:
			raise ValueError("Use: number operator number")
		left_text, symbol, right_text = parts
		left = self.parse_value(left_text)
		right = self.parse_value(right_text)
		if symbol not in OPERATORS:
			raise ValueError(f"Unsupported operator: {symbol}")
		if symbol in {"/", "//", "%"} and right == 0:
			raise ZeroDivisionError("Cannot divide by zero")
		result = OPERATORS[symbol](left, right)
		if isinstance(result, float) and not math.isfinite(result):
			raise OverflowError("Result is not finite")
		return result

	def remember(self, expression, result):
		"""Store a formatted calculation in session history."""
		display = self.format_value(result)
		self.history.append(f"{expression} = {display}")

	def show_history(self):
		"""Print previous calculations, if any."""
		if not self.history:
			print("History is empty.")
			return
		for number, entry in enumerate(self.history, start=1):
			print(f"{number}. {entry}")

	def run(self):
		"""Read commands and calculations until the user exits."""
		print("Simple Calculator (type help for commands)")
		while True:
			try:
				expression = input("calc> ").strip()
			except (EOFError, KeyboardInterrupt):
				print("\nGoodbye.")
				return
			if not expression:
				continue
			command = expression.lower()
			if command in {"quit", "exit", "q"}:
				print("Goodbye.")
				return
			if command == "history":
				self.show_history()
				continue
			if command == "clear":
				self.history.clear()
				print("History cleared.")
				continue
			if command == "help":
				print("Enter: 2 + 3 (operators: + - * / // % **)")
				print("Constants: pi, e; commands: history, clear, quit")
				continue
			try:
				result = self.calculate(expression)
				display = self.format_value(result)
				print(display)
				self.remember(expression, result)
			except (ValueError, ZeroDivisionError, OverflowError) as error:
				print(f"Error: {error}")

def main():
	"""Start the calculator application."""
	calculator = Calculator()
	calculator.run()

if __name__ == "__main__":
	main()
