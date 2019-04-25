import csv
import random


max_iterations = 1000


def get_random_centroids(dataset, k, prev=[]):
    centroids = prev[:]

    for _ in range(k):
        is_unique = False

        while not is_unique:
            random_row = random.choice(dataset)
            match = list(filter(lambda x: x[0] == random_row[0], centroids))

            if len(match) == 0:
                is_unique = True
                centroids.append(random_row)

    return centroids


def should_stop(old_centroids, new_centroids, iterations):
    if iterations >= max_iterations:
        return True
    elif old_centroids == None:
        return False

    old = list(map(lambda x: x[0], old_centroids))
    new = list(map(lambda x: x[0], new_centroids))

    return sorted(old) == sorted(new)


def distance(a, b):
    sum_squares = 0

    for i in range(2, len(a)):
        sum_squares = sum_squares + ((a[i] - b[i]) ** 2)

    return sum_squares ** 0.5


def associate(dataset, centroids):
    labels = {}

    for row in dataset:
        min_distance = 1000000000
        closest_centroid = None

        for centroid in centroids:
            a_distance = distance(row, centroid)

            if a_distance < min_distance:
                min_distance = a_distance
                closest_centroid = centroid

        key = str(closest_centroid[0])

        if key in labels:
            labels[key].append(row)
        else:
            labels[key] = [row]

    return labels


def get_new_centroids(dataset, labels, k):
    new_centroids = []

    for data in labels.values():
        size = len(data)
        centroid = [sum(x) for x in zip(*data)]
        centroid = [x / size for x in centroid]
        new_centroids.append(centroid)

    if len(new_centroids) < k:
        random_centroids = get_random_centroids(dataset, k - len(new_centroids), new_centroids)
        new_centroids = random_centroids

    return new_centroids


def print_labels(labels):
    for data in labels.values():
        d = {}

        for row in data:
            key = row[1]

            if key in d:
                d[key] += 1
            else:
                d[key] = 1

        print(d)
        print(len(data))


dataset = []

with open('work.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    for row in csv_reader:
        if line_count != 0:
            a_row = []

            for elem in row:
                if ',' in elem:
                    a_row.append(int(elem.replace(',', '')))
                else:
                    a_row.append(int(elem))

            dataset.append(a_row)

        line_count += 1

k = 2

iterations = 0
centroids = get_random_centroids(dataset, k)
old_centroids = None
labels = None

while not should_stop(old_centroids, centroids, iterations):
    old_centroids = centroids
    # iterations += 1
    labels = associate(dataset, centroids)
    centroids = get_new_centroids(dataset, labels, k)

print_labels(labels)

print()
for x in centroids:
    print(x)

