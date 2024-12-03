from collections import defaultdict


def extract_lists(data: str) -> tuple[list[int], list[int]]:
    l1: list[int] = []
    l2: list[int] = []

    for line in data.splitlines():
        v1, v2 = line.split(maxsplit=1)
        l1.append(int(v1))
        l2.append(int(v2))

    return l1, l2


def run(data: str) -> None:
    l1, l2 = extract_lists(data)

    l1.sort()
    l2.sort()
    total_distance = sum(abs(n1 - n2) for n1, n2 in zip(l1, l2))

    similarities: defaultdict[int, int] = defaultdict(int)
    for n in l2:
        similarities[n] += n
    similarity_score = sum(similarities[n] for n in l1)

    print(total_distance)
    print(similarity_score)
