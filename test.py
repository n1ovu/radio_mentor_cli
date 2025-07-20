def trace_ids(func):
    def wrapper(*args, **kwargs):
        print("IDs in  ➡", [id(a) for a in args])
        out = func(*args, **kwargs)
        print("IDs out ➡", id(out))
        return out
    return wrapper


@trace_ids
def bar(x):
    x.append(99)
    return x


a = [1]
bar(a)
print(a)
