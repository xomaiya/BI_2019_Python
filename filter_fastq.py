#!/usr/bin/env python
import argparse


def symbols2values(symbols):
    return [ord(el) - ord('!') for el in symbols]


def calculate_gc_content(read):
    if len(read) == 0:
        return 0
    return len([i for i in read if i in "GC"]) * 100 / len(read)


def filter(read, min_length, gc_min, gc_max):
    if len(read) < min_length:
        return 'bad'
    gc_content = calculate_gc_content(read)
    if gc_min <= gc_content <= gc_max:
        return 'good'
    else:
        return 'bad'


def sliding_window(read, quality, threshold, window):
    quality = symbols2values(quality)
    for i in range(len(quality) - window + 1):
        if sum(quality[i:i + window]) < threshold * window:
            return read[:i]
    return read


def leading(read, quality, threshold):
    quality = symbols2values(quality)
    thresh_index = -1
    for i in range(len(quality)):
        if quality[i] < threshold:
            thresh_index = i
        else:
            break
    return read[thresh_index + 1:]


def trailing(read, quality, threshold):
    return leading(read[::-1], quality[::-1], threshold)[::-1]


def crop(read, length):
    return headcrop(read[::-1], length)[::-1]


def headcrop(read, length):
    return read[length:]


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser.add_argument('fastq', type=str)

    filter_parser = subparsers.add_parser('filter')
    filter_parser.add_argument('--min_length', type=int, required=True)
    filter_parser.add_argument('--keep_filtered', action="store_true")
    filter_parser.add_argument('--gc_bounds', type=int, nargs='+', required=True)
    filter_parser.add_argument('--output_base_name', type=str, required=False)
    filter_parser.add_argument('fastq', type=str)

    trimmomatic_parser = subparsers.add_parser('trimmomatic')
    trimmomatic_subparser = trimmomatic_parser.add_subparsers()

    sliding_window_parser = trimmomatic_subparser.add_parser('SLIDINGWINDOW')
    sliding_window_parser.add_argument('--threshhold', type=int, required=True)
    sliding_window_parser.add_argument('--window', type=int, required=True)

    leading_parser = trimmomatic_subparser.add_parser('LEADING')
    leading_parser.add_argument('--threshhold', type=int, required=True)

    trailing_parser = trimmomatic_subparser.add_parser('TRAILING')
    trailing_parser.add_argument('--threshhold', type=int, required=True)

    crop_parser = trimmomatic_subparser.add_parser('CROP')
    crop_parser.add_argument('--length', type=int, required=True)

    headcrop_parser = trimmomatic_subparser.add_parser('HEADCROP')
    headcrop_parser.add_argument('--length', type=int, required=True)

    args = parser.parse_args()

    with open(args.fastq, 'r') as file:
        fastq = file.readlines()

    if args.trimmonatic:

        if args.SLIDINGWINDOW:
            with open('output', 'w') as file:
                for i in range(0, len(fastq), 4):
                    file.write(f'{fastq[i]}\n')
                    file.write(f'{sliding_window(fastq[i + 1], fastq[i + 2], args.threshold, args.window)}\n')
                    file.write(f'{fastq[i + 2]}\n')
                    file.write(f'{fastq[i + 3]}\n')

        if args.LEADING:
            with open('output', 'w') as file:
                for i in range(0, len(fastq), 4):
                    file.write(f'{fastq[i]}\n')
                    file.write(f'{leading(fastq[i + 1], fastq[i + 2], args.threshold)}\n')
                    file.write(f'{fastq[i + 2]}\n')
                    file.write(f'{fastq[i + 3]}\n')

        if args.TRAILING:
            with open('output', 'w') as file:
                for i in range(0, len(fastq), 4):
                    file.write(f'{fastq[i]}\n')
                    file.write(f'{trailing(fastq[i + 1], fastq[i + 2], args.threshold)}\n')
                    file.write(f'{fastq[i + 2]}\n')
                    file.write(f'{fastq[i + 3]}\n')

        if args.CROP:
            with open('output', 'w') as file:
                for i in range(0, len(fastq), 4):
                    file.write(f'{fastq[i]}\n')
                    file.write(f'{crop(fastq[i + 1], args.length)}\n')
                    file.write(f'{fastq[i + 2]}\n')
                    file.write(f'{fastq[i + 3]}\n')

        if args.HEADCROP:
            with open('output', 'w') as file:
                for i in range(0, len(fastq), 4):
                    file.write(f'{fastq[i]}\n')
                    file.write(f'{headcrop(fastq[i + 1], args.length)}\n')
                    file.write(f'{fastq[i + 2]}\n')
                    file.write(f'{fastq[i + 3]}\n')

    if args.filter:
        assert args.min_length > 0, "min_length < 0. Так дела не делаются."
        assert 1 <= len(args.gc_bounds) <= 2, "Неверное количество границ"

        gc_min = args.gc_bounds[0]
        if len(args.gc_bounds) == 2:
            gc_max = args.gc_bounds[1]
        else:
            gc_max = 100

        if args.output_base_name is None:
            output_path = args.fastq[:args.fastq.rindex('.')]
        else:
            output_path = args.output_base_name

        pass_path = output_path + '__passed.fastq'
        fail_path = output_path + '__failed.fastq'

        with open(pass_path, 'w') as passed, open(fail_path, 'w') as failed:
            for i in range(0, len(fastq), 4):
                if filter(fastq[i + 1], args.min_length, gc_min, gc_max) == 'good':
                    passed.writelines(fastq[i: i + 4])
                elif args.keep_filtered is not None:
                    failed.writelines(fastq[i: i + 4])
