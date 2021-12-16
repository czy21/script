import math
from pathlib import Path

p=Path(".")
p.anchor.replace("\\","\\\\")
print(p.resolve())
print(p)