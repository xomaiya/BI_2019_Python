#!/usr/bin/env python
import argparse


def read_bed(file_name):
    bed_list = []
    with open(file_name, 'r') as file:
        for line in file:
            bed_list.append((line.split()[0], int(line.split()[1]), int(line.split()[2])))
    return bed_list


def write_bed(bed, file_name):
    with open(file_name, 'w') as file:
        # file.write('chr\tstart\tend')
        file.writelines(f'{name}\t{start}\t{end}\n' for name, start, end in bed)


def read_fasta(file_name):
    fasta = {}
    with open(file_name, 'r') as file:
        for line in file:
            if line[0] == '>':
                chr = line[1:].strip()
                fasta[chr] = ''
            else:
                fasta[chr] += line.strip()
    return fasta


def sort(bed, output_name):
    return write_bed(sorted(bed), output_name)


def subtract_interval(bed1, interval):
    subtracted = []
    for interval1 in sorted(bed1):
        if interval[0] != interval1[0] or interval[2] < interval1[1] or interval[1] > interval1[2]:
            subtracted.append(interval1)
            continue
        if interval[1] <= interval1[1] and interval[2] >= interval1[2]:
            continue
        if interval[1] <= interval1[1] and interval[2] < interval1[2]:
            subtracted.append((interval1[0], interval[2] + 1, interval1[2]))
            continue
        if interval[1] <= interval1[2] and interval[2] >= interval1[2]:
            subtracted.append((interval1[0], interval1[1], interval[1] - 1))
            continue
        subtracted.append((interval1[0], interval1[1], interval[1] - 1))
        subtracted.append((interval1[0], interval[2] + 1, interval1[2]))
    return subtracted


def subtract(bed1, bed2, output_name):
    for interval in bed2:
        bed1 = subtract_interval(bed1, interval)
    return write_bed(bed1, output_name)


def merge(bed, output_name):
    bed = sorted(bed)
    merged = []
    i = 0
    while i < len(bed):
        mergering = bed[i]
        while True:
            if i + 1 == len(bed) or bed[i][0] != bed[i + 1][0] or bed[i + 1][1] - bed[i][2] > 10:
                i += 1
                break
            else:
                mergering = (mergering[0], mergering[1], bed[i + 1][2])
                i += 1
        merged.append(mergering)
    return write_bed(merged, output_name)


def getfasta(fasta, bed, output_name):
    with open(output_name, 'w') as file:
        for interval in bed:
            print(fasta[interval[0]][interval[1]:interval[2] + 1])
            try:
                file.write(f'>{interval[0]}:{interval[1]}{interval[2]}\n')
                file.write(f'{fasta[interval[0]][interval[1]:interval[2] + 1]}\n')
            except (IndexError, KeyError):
                pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('merge', type='store_true')
    parser.add_argument('sort', type='store_true')
    parser.add_argument('substract', type='store_true')
    parser.add_argument('getfasta', type='store_true')
    parser.add_argument('intersect', type='store_true')

    parser.add_argument('--input', type=str, nargs='+', required=True)
    parser.add_argument('--output', type=str, required=False)

    args = parser.parse_args()

    if args.output == None:
        args.output = 'output'

    if args.sort:
        sort(read_bed(args.input[0]), args.output)
    if args.subtrack:
        subtract(read_bed(args.input[0]), read_bed(args.input[1]), args.output)
    if args.merge:
        merge(read_bed(args.input[0]), args.output)
    if args.intersect:
        pass
    if args.getfasta:
        getfasta(read_bed(args.input[0]), read_fasta(args.input[1]), args.output)

