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


def distance(a, b):
    sum_squares = 0

    for i in range(2, len(a)):
        sum_squares = sum_squares + ((a[i] - b[i]) ** 2)

    return sum_squares ** 0.5


def associate(dataset, centroids):
    labels = {}
    score = 0

    for row in dataset:
        min_distance = 1000000000
        closest_centroid = None

        for centroid in centroids:
            a_distance = distance(row, centroid)

            if a_distance < min_distance:
                min_distance = a_distance
                closest_centroid = centroid

        score += min_distance
        key = str(closest_centroid[0])

        if key in labels:
            labels[key].append(row)
        else:
            labels[key] = [row]

    return labels, score


def print_labels(labels):
    for data in labels.values():
        d = {}

        # for row in data:
        #     key = row[1]

        #     if key in d:
        #         d[key] += 1
        #     else:
        #         d[key] = 1

        # print(d)
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
medoids = get_random_centroids(dataset, k)
old_score = 100000000
labels, new_score = associate(dataset, medoids)
is_swapped = True

while is_swapped:
    is_swapped = False

    for i in range(len(medoids)):
        for row in dataset:
            if row[0] != medoids[i][0]:
                new_medoids = medoids[:]
                new_medoids[i] = row
                new_labels, a_score = associate(dataset, new_medoids)

                if a_score < new_score:
                    labels = new_labels
                    new_score = a_score
                    is_swapped = True

print_labels(labels)
print(new_score)
