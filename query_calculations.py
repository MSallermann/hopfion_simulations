import os, calculation_folder

from sympy import arg

def check(path):
    return calculation_folder.calculation_folder(path).locked()

def check(path):
    return os.path.exists(os.path.join(path, "gneb_preconverge", "chain.ovf"))

def main(path):
    if check(path):
        print(path)
        return 1
    return 0

if __name__ == "__main__":
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, nargs="+")
    args = parser.parse_args()

    count = 0
    for f in args.paths:
        count += main(f)

    result_string = f"=====\n{count} / {len(args.paths)} ( {count/len(args.paths) * 100:.2f} % )"
    print(result_string)