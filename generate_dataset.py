import random
import csv


with open("data.csv", 'w', newline='') as fopen:
    csv_writer = csv.writer(fopen)
    for i in range(15000):
        csv_writer.writerow([str(random.randint(1, 9)) + str(random.randint(0, 999999999))])

