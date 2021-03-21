from pathlib import Path

p = list(map(lambda p: p.resolve().as_posix(), Path("./files").glob("*")))
print("s")
