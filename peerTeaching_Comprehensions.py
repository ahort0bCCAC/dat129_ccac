#!/usr/bin/env python
# coding: utf-8

# In[60]:


# --- List Comprehensions ---
# List comprehensions are a concise way to make a list from an object 
# where you might otherwise use a for loop.
# The object can be a string, tuple, another list, etc.

# A list comprehension looks like this:
# list_variable = [x for x in object optional conditions]

# Let's look at some examples.


# In[37]:


# Here we are using a list comprehension to loop through a string 
# and add each character as an elemenet in a list.

lc_string = [x for x in 'Hello World!']

print (lc_string)


# In[38]:


# If we wrote the above as a for loop it would look like this

string_letters = [ ]

for letter in 'Hello World!':
    string_letters.append(letter)

print (string_letters)

# As you can see list comprehension used one line of code
# to perform the task of three lines in a for loop


# In[39]:


# here we are using a list comprehension to loop through 
# a range of 10 numbers and add each number as an element in a list

lc_numbers = [i for i in range(1, 11)]

print (lc_numbers)


# In[40]:


# Now let's add some conditions to our list comprehensions


# In[41]:


# Here we will iterate through 10 numbers
# and add them to a list only if they are even.

lc_numbers_even = [i for i in range(1, 11) if i%2 == 0]

print (lc_numbers_even)


# In[42]:


# Here is another example of conditions
# let's get a new list of fish, without fish that start with an 's'

lc_tuple = ('cod', 'salmon', 'tilapia', 'shrimp', 'flounder')

fish_list = [fish for fish in lc_tuple if not fish.startswith('s')]

print(fish_list)


# In[43]:


# try it for yourself:
# make this for loop into a list comprehension

odd_numbers = []

for i in range(1, 25):
    if i%2 != 0:
        odd_numbers.append(i)

print (odd_numbers)


# In[44]:


# --- Nested Loops in List Comprehensions ---
# list comprehensions can be nested


# In[45]:


# Here's a nested for loop that multiplies 
# each of the numbers in the first list
# by each of the numbers in the second list

my_list = []

for x in [10, 20, 30, 40]:
    for y in [1, 2, 3, 4]:
        my_list.append(x * y)

print(my_list)


# In[46]:


# We can accomplish the same task with a list comprehension
# using less lines of code.

my_list = [x * y for x in [10, 20, 30, 40] for y in [1, 2, 3, 4]]

print(my_list)


# In[55]:


# Now that you've mastered list comprehensions lets look at
# --- Dictionary Comprehensions ---

# Similar to list comprehensions,the dictionary comprehensions
# create a dictionary from an iterable object.
# I found these a little harder to understand so let me break it down,
# then we'll put it back together

# First assign the dictionary name, and open the dictionary

#     mydict = {

# then the write the desired results of key:value,
# here you can simply result a key : value combination,
# or you can transform the key and/or value in some way
# before storing them in the dictionary.
# For example you can change the case of the text, 
# or like in this example we will square the value.

# In this example num is my key and num*num is my value

#     num : num*num

# Now let's get our keys and values with a for loop,
# in this example we'll use a range() function
# to get 5 numbers and then we'll close our dictionary

#     for num in range(1,6)}

# Now, let's put this together and see what it does.

mydict = {num : num*num for num in range(1,6)}

print(mydict)


# In[48]:


# Here we have a list of fruits, let use dictionary comprehensions 
# with a condition. We'll create a dictionary of the fruits as keys
# with the length of the fruit name as values however,
# we'll only include them in the dictionary if the length is greater than 4 

fruits = ['Apple', 'Orange', 'Banana', 'Strawberry', 'Kiwi']

fruits_dict = {f:len(f) for f in fruits if len(f) > 4}

print(fruits_dict, '\n')

#let's use our fruits again to see how we can transform the key 
# with our dictionary comprehension. Nnotice this time I've set 
# the condition to name length greater than zero.

fruits_dict_upper = {f.upper() : len(f) for f in fruits if len(f) > 0}

print(fruits_dict_upper)


# In[49]:


# Bonus learning! With the help of the zip function
# you can use dictionary comprehension to merge two lists into a dictionary,
# using one list as the key and the other as the values.

# zip() is a built-in function that pairs the items of iterable objects
# together with other items in the same postition of other iterable object

keys = ['Jan','Feb','Mar','Apr','May', 'Jun', 
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

myDict = {k:v for (k,v) in zip(keys, values)}
print (myDict,'\n')

#let's see what zip does by it's self

zipdict = list(zip(keys, values))

print (zipdict)


# In[ ]:


# try it for yourself
# can you write a dictionary comprehension
# where the keys are numbers between 1 and 15 (both included)
# and the values are the cube of the keys
# for even numbers only?

