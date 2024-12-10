class File:
    __slots__ = ("num", "start", "length")

    num: int
    start: int
    length: int

    def __init__(self, num: int, start: int, length: int) -> None:
        self.num = num
        self.start = start
        self.length = length


class Space:
    __slots__ = ("start", "length", "prev", "next")

    start: int
    length: int
    prev: "Space | None"
    next: "Space | None"

    def __init__(self, start: int, length: int) -> None:
        self.start = start
        self.length = length
        self.prev = None
        self.next = None


def parse_files_spaces(data: str, include_zero: bool) -> tuple[list[File], Space]:
    files: list[File] = []
    head: Space | None = None
    tail: Space | None = None

    index = 0
    file_num = 0
    occupied = False

    for lenstr in data.strip():
        occupied = not occupied

        length = int(lenstr)
        if length == 0 and not include_zero:
            continue

        if occupied:
            files.append(File(file_num, index, length))
            file_num += 1
        else:
            node = Space(index, length)
            if head is None:
                head = node
            elif tail is not None:
                node.prev = tail
                tail.next = node
            tail = node

        index += length

    assert head is not None
    return files, head


def fchecksum(num, start, length) -> int:
    # Gauss sum of arithmetic sequence
    return num * length * (2 * start + length - 1) // 2


def compact1(files: list[File], spaces: Space) -> int:
    checksum = 0
    occupied = False
    s: Space | None = spaces

    while files:
        occupied = not occupied

        # Handling a file in place
        if occupied:
            f = files.pop(0)
            checksum += fchecksum(f.num, f.start, f.length)
            continue

        # Handling an empty space
        assert s is not None
        while files and s.length:
            f = files.pop()

            if f.length <= s.length:
                # Whole file move
                checksum += fchecksum(f.num, s.start, f.length)
                s.start += f.length
                s.length -= f.length
            else:
                # Only partial file move
                checksum += fchecksum(f.num, s.start, s.length)
                f.length -= s.length
                s.length = 0
                files.append(f)

        s = s.next

    return checksum


def compact2(files: list[File], spaces: Space) -> int:
    checksum = 0

    for f in files[::-1]:
        s: Space | None = spaces
        while s is not None:
            # Free space not big enough
            if s.length < f.length:
                s = s.next
                continue

            # Free space not to left of file
            if s.start > f.start:
                s = s.next
                continue

            # File will fit, move it and shrink the s space
            f.start = s.start
            s.start += f.length
            s.length -= f.length

            # Unlink the free space from the list if now empty
            if s.length == 0:
                if s.prev is not None:
                    s.prev.next = s.next
                if s.next is not None:
                    s.next.prev = s.prev
            break

        checksum += fchecksum(f.num, f.start, f.length)

    return checksum


def run(data: str) -> None:
    files, spaces = parse_files_spaces(data, include_zero=True)
    checksum1 = compact1(files, spaces)

    files, spaces = parse_files_spaces(data, include_zero=False)
    checksum2 = compact2(files, spaces)

    print(checksum1)
    print(checksum2)
