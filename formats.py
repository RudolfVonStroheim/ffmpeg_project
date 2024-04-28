from pickle import load

with open("formats.pickle", "rb") as f:
    formats = list(load(f))
    print(formats)
print()
print(formats)
