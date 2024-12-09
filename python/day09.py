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


def parse_files_free(
    data: str,
) -> tuple[dict[int, tuple[int, int]], dict[int, tuple[int, int]]]:
    files: dict[int, tuple[int, int]] = {}
    free: dict[int, tuple[int, int]] = {}

    index = 0
    filenum = 0
    freenum = 0
    occupied = False

    for lenstr in data.strip():
        occupied = not occupied

        length = int(lenstr)
        if length == 0:
            continue

        info = (index, length)
        if occupied:
            files[filenum] = info
            filenum += 1
        else:
            free[freenum] = info
            freenum += 1
        index += length

    return files, free


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
    files, free = parse_files_free(data)

    for filenum in reversed(files):
        file_start, file_length = files[filenum]
        for freenum, (free_start, free_length) in free.items():
            # Free space not big enough
            if free_length < file_length:
                continue

            # Free space not to left of file
            if free_start > file_start:
                continue

            # File will fit, move it
            files[filenum] = (free_start, file_length)
            free[freenum] = (free_start + file_length, free_length - file_length)
            break

    checksum = 0
    for filenum, (start, length) in files.items():
        for i in range(length):
            checksum += filenum * (start + i)
    return checksum


def run(data: str) -> None:
    checksum1 = compact1(data)
    checksum2 = compact2(data)

    print(checksum1)
    print(checksum2)
