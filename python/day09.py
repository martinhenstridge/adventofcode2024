def parse_blocks_free(data: str) -> tuple[list[int], list[tuple[int, int]]]:
    blocks: list[int] = []
    free: list[tuple[int, int]] = []

    occupied = False
    filenum = 0

    for lenstr in data.strip():
        occupied = not occupied

        length = int(lenstr)
        if length == 0:
            continue

        if occupied:
            for _ in range(length):
                blocks.append(filenum)
            filenum += 1
        else:
            free.append((len(blocks), length))
            for _ in range(length):
                blocks.append(-1)

    return blocks, free


class FreeNode:
    __slots__ = ("start", "length", "prev", "next")

    start: int
    length: int
    prev: "FreeNode | None"
    next: "FreeNode | None"

    def __init__(self, start: int, length: int) -> None:
        self.start = start
        self.length = length
        self.prev = None
        self.next = None


def parse_files_free(data: str) -> tuple[list[tuple[int, int, int]], FreeNode]:
    filelist: list[tuple[int, int, int]] = []
    freehead: FreeNode | None = None
    freetail: FreeNode | None = None

    index = 0
    file_id = 0
    occupied = False

    for lenstr in data.strip():
        occupied = not occupied

        length = int(lenstr)
        if length == 0:
            continue

        if occupied:
            filelist.append((file_id, index, length))
            file_id += 1
        else:
            node = FreeNode(index, length)
            if freehead is None:
                freehead = node
            elif freetail is not None:
                node.prev = freetail
                freetail.next = node
            freetail = node

        index += length

    assert freehead is not None
    return filelist, freehead


def compact1(data: str) -> int:
    blocks, free = parse_blocks_free(data)

    while free:
        block = blocks.pop()

        # Handle free space at the end
        if block == -1:
            start, length = free.pop()
            if length > 1:
                free.append((start, length - 1))
            continue

        # Move block into leftmost free space
        start, length = free.pop(0)
        blocks[start] = block
        if length > 1:
            free.insert(0, (start + 1, length - 1))

    return sum(i * b for i, b in enumerate(blocks))


def compact2(data: str) -> int:
    filelist, freelist = parse_files_free(data)
    checksum = 0

    for file_id, file_start, file_length in filelist[::-1]:
        free: "FreeNode | None" = freelist
        while free is not None:
            # Free space not big enough
            if free.length < file_length:
                free = free.next
                continue

            # Free space not to left of file
            if free.start > file_start:
                free = free.next
                continue

            # File will fit, move it and shrink the free space
            file_start = free.start
            free.start += file_length
            free.length -= file_length

            # Unlink the free space from the list if now empty
            if free.length == 0:
                if free.prev is not None:
                    free.prev.next = free.next
                if free.next is not None:
                    free.next.prev = free.prev
            break

        checksum += file_id * file_length * (2 * file_start + file_length - 1) // 2

    return checksum


def run(data: str) -> None:
    checksum1 = compact1(data)
    checksum2 = compact2(data)

    print(checksum1)
    print(checksum2)
