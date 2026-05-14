import sys
input = sys.stdin.readline

steps = 0

n = int(input())
nums = [int(x) for x in input().split()]

for i in range(1, n):
    if nums[i] < nums[i-1]:
        diff = nums[i-1] - nums[i]
        steps += diff
        nums[i] += diff

print(steps)