'''
Create a function that accepts a list of numbers and returns the largest number without using Python's built-in max() function.
'''

def largest_num(number):
    if not number:
        return None
    
    largest = number[0]

    for num in number[1:]:
        if num>largest:
            largest = num
    return largest
    
num = [1, 4, 10, 6, 3]
print("Largest Number of the List is: ",largest_num(num))
