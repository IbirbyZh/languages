from linq import Linq


def main():
    with open(__file__) as h:
        print(
            '\n'.join(
                Linq(''.join(map(lambda c: c if c.isalnum() or c == '_' else ' ', h.read())).split())
                    .group_by(lambda token: token)
                    .select(lambda token_tuples: (token_tuples[0], sum(1 for _ in token_tuples[1])))
                    .order_by(lambda token_tuple: token_tuple[1])
                    .select(lambda token_tuple: '{} {}'.format(*token_tuple))
                    .to_list()
            )
        )


if __name__ == '__main__':
    main()
