my_dict = {1: 2, 2: 1, "Hello": 1234}

# Sort the dictionary items by values (ascending order)
sorted_dict = sorted(my_dict.items(), key=lambda x: x[1], reverse=True)

print("Sorted dictionary by values (ascending):")
for key, value in sorted_dict:
    print(f"{key}: {value}")