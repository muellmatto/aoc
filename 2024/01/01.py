left_list = []
right_list = []

with open("input.txt", "r") as f:
    while True:
        line = f.readline()
        if not line:
            break
        left, right = line.split("   ")
        left_list.append(int(left))
        right_list.append(int(right))


left_list.sort()
right_list.sort()

distances = []
similarities = []

for i in range(len(left_list)):
    distances.append(left_list[i] - right_list[i])
    similarities.append(left_list[i] * right_list.count(left_list[i]))

distances_abs = map(abs, distances)
total_distance = sum(distances_abs)
print(total_distance)

similarity_score = sum(similarities)
print(similarity_score)
