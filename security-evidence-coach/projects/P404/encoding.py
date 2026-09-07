"""Pure desktop adapter; no native invocation."""

def snapshot(text):
    data = text.encode("utf-8")
    return data, len(data)
