import cv2
from bitarray import bitarray
import numpy as np

# getting information from user
window_size = input("Enter length of sliding window: ")
window_size = int(window_size)
lookahead_buffer_size = input("Enter look-ahead size: ")
lookahead_buffer_size = int(lookahead_buffer_size)
search_buffer_size = window_size - lookahead_buffer_size
path = input("Enter Image Path: ")
U16 = False
if lookahead_buffer_size > 256:
    U16 = True


def findLongestMatch(data, current_position):
    end_of_buffer = min(current_position + lookahead_buffer_size, len(data) + 1)
    best_match_distance = -1
    best_match_length = -1
    for j in range(current_position + 2, end_of_buffer):
        search_buffer_index = max(0, current_position - search_buffer_size)
        substring = data[current_position:j]
        for k in range(search_buffer_index, current_position):
            repetitions = int(len(substring) / (current_position - k))
            last = len(substring) % (current_position - k)
            matched_string = data[k:current_position] * repetitions + data[k:k + last]
            if matched_string == substring and len(substring) > best_match_length:
                best_match_distance = current_position - k
                best_match_length = len(substring)
    if best_match_distance > 0 and best_match_length > 0:
        return best_match_distance, best_match_length
    return None


i = 0
flag_buffer = bitarray()
jump_distance_buffer = []
colors_buffer = []

# read the input file
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
data = [val for sublist in img for val in sublist]


while i < len(data):
    match = findLongestMatch(data, i)
    if match:
        (bestMatchDistance, bestMatchLength) = match
        flag_buffer.append(True)
        jump_distance_buffer.append(bestMatchDistance)
        jump_distance_buffer.append(bestMatchLength)
        if i + bestMatchLength < len(data):
            if U16:
                colors_buffer.append(data[i + bestMatchLength])
            else:
                jump_distance_buffer.append(data[i + bestMatchLength])
        i += (bestMatchLength+1)
    else:
        flag_buffer.append(False)
        if U16:
            colors_buffer.append(data[i])
        else:
            jump_distance_buffer.append(data[i])
        i += 1
with open('flags.txt', 'wb') as output_file:
    output_file.write(flag_buffer.tobytes())
if U16:
    tags = np.array(jump_distance_buffer, dtype=np.uint16)
    colors = np.array(colors_buffer, dtype=np.uint8)
    colors.tofile('colors.npy')
else:
    tags = np.array(jump_distance_buffer, dtype=np.uint8)

tags.tofile('tags.npy')

print(data)


