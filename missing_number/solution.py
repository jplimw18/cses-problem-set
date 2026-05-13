import sys

input = sys.stdin.readline

print(sum(range(1, int(input())+1)) - sum([int(x) for x in input().split()]))