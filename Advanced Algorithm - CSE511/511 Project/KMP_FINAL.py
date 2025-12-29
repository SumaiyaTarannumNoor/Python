import time
import matplotlib.pyplot as plt

def kmp_table(pattern):
    # Create a table to store the values of the longest proper prefix that is also a suffix of the substring for each position in the pattern.
    table = [0] * len(pattern)

    # Initialize the left and right pointers to zero and one, respectively.
    left, right = 0, 1

    # Iterate over the pattern from left to right
    while right < len(pattern):
    # If the character at the right pointer is equal to the character at the left pointer, increment both pointers and set the value of the table at the right pointer to the value of the left pointer.
        if pattern[right] == pattern[left]:
            left += 1
            table[right] = left
            right += 1

        else:
            # If the characters are not equal, move the left pointer back to the position in the table corresponding to the previous longest proper prefix that is also a suffix, and continue checking for a match.
            if left != 0:
                left = table[left-1]

            else:
                # If there is no previous longest proper prefix that is also a suffix, set the value of the tabe at the right pointer to zero and move pointer forward.
                table[right] = 0
                right += 1


    return table



def kmp_search(text, pattern):
    # Create a table to store the values of the longest proper prefix that is also a suffix of the substring for each position in the pattern.
    table = kmp_table(pattern)

    # Initialize variables for the indicies of the text and pattern.
    i, j = 0, 0

    # Iterate over the text while the index is less than the length of the text.
    while i < len(text):
        # If the characters at the current indicies match, increment both indicies.
        if text[i] == pattern[j]:
            i += 1
            j += 1

            # If the value of j is equal to the length of the pattern, the pattern has been found in the text, so return the index where it starts.
            if j == len(pattern):
                return i - j
            
        else:
            # If the characters do not match and j is not zero, move the j index to the value in the table corresponding to the previous longest proper prefix that is also a suffix, and continue checking for a match.
            if j != 0:
                j = table[j-1]
            else:
                # If there is no previous longest proper prefix that is also a suffix, move the i index forward.
                i += 1


    # If the pattern is not found, return -1
    return -1


# List of input files
input_files = ['BestCase.txt', 'AverageCase.txt', 'WorstCase.txt']

for file_name in input_files:
    # Read inputs
    with open(file_name, 'r') as file:
        inputs = [line.strip() for line in file.readlines()]
    
    runtimes = []
    results = []
    
    # Run KMP on each input
    for idx, input_str in enumerate(inputs):
        # Split only on the first '|' to avoid too many values error
        if '|' in input_str:
            text, pattern = input_str.split('|', 1)  # split only at first '|'
        else:
            text = input_str
            pattern = input_str[-5:]  # fallback, last 5 chars
            
        begin = time.time()
        pos = kmp_search(text, pattern)
        end = time.time()
        
        runtimes.append(end - begin)
        results.append((idx + 1, len(text), pos, end - begin))
    
    # Print results
    print(f"\n=== Results for {file_name} ===")
    print("Index | Input Length | Position Found | Runtime (seconds)")
    print("------------------------------------------------------------")
    for idx, length, pos, runtime in results:
        print(f"{idx:5} | {length:12} | {pos:13} | {runtime:.8f}")
    
    # Plot runtime
    plt.figure(figsize=(10, 6))
    plt.plot([length for _, length, _, _ in results], runtimes, marker='o')
    plt.title(f'KMP Search Runtime vs Input Length ({file_name})')
    plt.xlabel('Input Length')
    plt.ylabel('Runtime (seconds)')
    plt.grid(True)
    plt.show()
