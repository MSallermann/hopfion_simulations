from spirit_extras import gneb_workflow
import calculation_folder

def main(path):
    folder = calculation_folder.calculation_folder( path )
    if not folder.lock():
        return

    print(folder.descriptor["J"])

    folder.unlock()

if __name__ == "__main__":
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest="input_folder", type=str, nargs='?', help='The input folder')

    import glob
    files = glob.glob(args.input_folder)
    for f in files:
        main(f)