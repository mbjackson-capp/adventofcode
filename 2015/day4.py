from hashlib import md5

# md5 hash syntax: https://www.geeksforgeeks.org/md5-hash-python/


def hash_search(part=1):
    # Replace with your input: https://adventofcode.com/2015/day/4
    SECRET_KEY = "ckczppom"
    pos_num = 1
    zeros_needed = 4 + part
    zeros = "0" * zeros_needed
    while True:
        input = SECRET_KEY + str(pos_num)
        result = md5(input.encode()).hexdigest()
        if result[:zeros_needed] == zeros:
            return pos_num
        pos_num += 1


print(f"Part 1 solution: {hash_search()}")
print(f"Part 2 solution: {hash_search(part=2)}")  # takes a few seconds
