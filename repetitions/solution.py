import sys

# ATTCGGGA <- DNA sequence

# grater sequence of repetitions  is 3: 'GGG'
# we need to find the longest sequence of repetitions in the given DNA sequence
def get_max_sequence(s: str) -> int:
    if len(s) == 1:
        return 1
    
    max_seq = 1
    curr_seq = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            curr_seq += 1
        else:
            max_seq = max(max_seq, curr_seq)
            curr_seq = 1

    return max_seq

input = sys.stdin.readline
n = input()
print(get_max_sequence(n))