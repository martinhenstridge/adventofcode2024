from typing import Any


def fchecksum(file_id: int, start: int, length: int) -> int:
    # Gauss sum of arithmetic sequence
    return file_id * length * (2 * start + length - 1) // 2


def compact1(original: list[int]) -> int:
    disk = original.copy()

    target = len(disk) - 1
    written = 0

    checksum = 0
    for idx in range(len(disk)):
        length = disk[idx]
        if length == 0:
            continue

        # Handle file
        if idx % 2 == 0:
            checksum += fchecksum(idx // 2, written, length)
            written += length
            continue

        # Handle space
        while length > 0:
            file_length = disk[target]
            if file_length <= length:
                # Whole file move
                checksum += fchecksum(target // 2, written, file_length)
                written += file_length

                disk[target] = 0
                length -= file_length
                target -= 2
                disk[target + 1] = 0
            else:
                # Partial file move
                checksum += fchecksum(target // 2, written, length)
                written += length

                disk[target] -= length
                length = 0

    return checksum


def compact2(original: list[int]) -> int:
    disk = original.copy()

    starts = []
    start = 0
    for length in disk:
        starts.append(start)
        start += length

    checksum = 0
    for file in range(len(disk) - 1, -1, -2):
        file_length = disk[file]
        if file_length == 0:
            continue

        start = starts[file]
        for space in range(1, file, 2):
            space_length = disk[space]
            if space_length < file_length:
                continue

            disk[space] -= file_length
            start = starts[space]
            starts[space] += file_length
            break

        checksum += fchecksum(file // 2, start, file_length)

    return checksum


def run(text: str) -> tuple[Any, Any]:
    disk_map = [int(n) for n in text.strip()]

    checksum1 = compact1(disk_map)
    checksum2 = compact2(disk_map)

    return checksum1, checksum2
