#https://www.geeksforgeeks.org/python-count-occurrences-of-each-word-in-given-text-file/
# Open the file in read mode
text = open("lyricstest.txt", "r")
  
# Create an empty dictionary
d = dict()
  
# Loop through each line of the file
for line in text:
    # Remove the leading spaces and newline character
    line = line.strip()
  
    # Convert the characters in line to
    # lowercase to avoid case mismatch
    line = line.lower()
  
    # Split the line into words
    words = line.split(" ")
                         
  
    # Iterate over each word in line
    for word in words:
        # Check if the word is already in dictionary
        if word in d:
            # Increment count of word by 1
            d[word] = d[word] + 1
        else:
            # Add the word to dictionary with count 1
            d[word] = 1
  
# Print the contents of dictionary

sorted_values = sorted(d.items(), key=lambda x:x[1], reverse=True)
converted_dict = dict(sorted_values)
# print(sorted_values)

for key in list(converted_dict.keys()):
     print(key, ":", d[key])