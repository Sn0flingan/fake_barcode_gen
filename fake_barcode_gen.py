# Fake Barcode generator
#
# Runs on Python 3
#
# Created by Alice (Sn0flingan) on 2018-11-14
#

import argparse
from statistics import median
from random import choice
import csv

from Levenshtein import distance


def main():
    args = get_arguments()
    barcodes = load_barcodes(args.input)
    num_true_bc = len(barcodes)
    
    #Calculate min distance in true barcodes
    if args.verbosity:
        print("Calculating distance between true barcodes...")
    distances = []
    for i in range(0, len(barcodes)):
        k = 1
        while i+k<=(len(barcodes)-1):
            dist = distance(barcodes[i], barcodes[i+k])
            distances.append(dist)
            k += 1
    min_distance = min(distances)
    if args.verbosity:
        print("Min distance within barcodes: {}".format(min_distance))

    #Generate fake barcodes
    if args.verbosity:
        print("Generating fake barcodes...")
    bc_length = median([len(bc) for bc in barcodes])
    for i in range(args.num_fake_bc):
        barcode = generate_barcode(bc_length, "")
        while min(distance(barcode, prev_bc) for prev_bc in barcodes) != min_distance:
            barcode = generate_barcode(bc_length, "")
        barcodes.append(barcode)
    fake_barcodes = barcodes[num_true_bc:]

    #Append to file
    filehandle = open(args.input, 'a')
    formated_barcodes = ['bc_fake_{};{}\n'.format(idx+1, barcode) for idx, barcode in enumerate(fake_barcodes)]
    filehandle.writelines(formated_barcodes)
    filehandle.close()
    if args.verbosity:
        print("Appended fake barcodes to: {}".format(args.input))

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Barcode file in csv format")
    parser.add_argument("-a", "--append", help="Store false barcodes in original file",
                        action='store_false')
    parser.add_argument("-v", "--verbosity", help="Verbosity of output",
                        action='store_true')
    parser.add_argument("-n", "--num_fake_bc", help="The number of fake barcodes to generate",
                        default=1, type=int)
    args = parser.parse_args()
    return args

def load_barcodes(barcode_file):
    barcodes = []
    with open(barcode_file, newline='') as f:
        reader = csv.reader(f, delimiter=';')
        try:
            for sequence in reader:
                non_sequence_letters = 'bdefhijklmnopqrsuvwxyz'
                #Assume header row if it contains other items than 'a', 'c', 'g', 't'
                if any(i in sequence[1] for i in non_sequence_letters):
                    continue
                barcodes.append(sequence[1])
                if len(sequence)>2:
                    barcodes.append(sequence[2])
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    return barcodes

def generate_barcode(bc_len, bc):
    if bc_len == 0:
        return bc
    next_base = choice("atgc")
    '''
    if not len(bc) == 0:
        while next_base == bc[-1]:
            next_base = choice("atgc")
    '''
    bc += next_base
    return generate_barcode(bc_len-1, bc)

main()
