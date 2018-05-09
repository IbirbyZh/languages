from functools import wraps
from linq import Linq


def print_result(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        for r in f(*args, **kwargs):
            print("DEBUG", r)
            yield r

    return wrapped


@print_result
def fibonacci():
    prev = 1
    yield prev
    now = 1
    while True:
        yield now
        now, prev = now + prev, now


def main():
    print(
        '\n'.join(
            map(
                str,
                Linq(fibonacci())
                    .where(lambda x: x % 3 == 0)
                    .select(lambda x: (x ** 2) if x % 2 == 0 else x)
                    .take(5)
                    .to_list()
            )
        )
    )


if __name__ == '__main__':
    main()
