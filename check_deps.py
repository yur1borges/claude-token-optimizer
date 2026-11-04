"""Check: selenium installed and playwright available."""
import importlib
print("selenium:", "OK" if importlib.util.find_spec("selenium") else "MISSING")
print("playwright:", "OK" if importlib.util.find_spec("playwright") else "MISSING")
