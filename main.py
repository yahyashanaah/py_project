# nums = [2, 7, 11, 15]
# result = nums[0] + nums[1]
# print(result)

# input = ["s", "t", "r", "i", "n", "g"]	

# def reverse_string(input):
#     return input[::-1]

# result = reverse_string(input)
# print(result)

s = "()[]{}"
def isValid(s):
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in mapping:
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
    return not stack

result = isValid(s)
print(result)