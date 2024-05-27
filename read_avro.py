import sys

import fastavro


def read_avro(file_path):
    with open(file_path, "rb") as f:
        reader = fastavro.reader(f)
        for record in reader:
            print(record)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python read_avro.py <path_to_avro_file>")
    else:
        avro_file_path = sys.argv[1]
        read_avro(avro_file_path)
