"""
Show a requirement
"""
import argparse


def parse_args(args):
    """
    Parse args
    """
    argparser = argparse.ArgumentParser(prog='req show')
    argparser.add_argument('req', help='Requirement to show')
    return argparser.parse_args(args)


def show(reqfile):
    """
    Show requirement
    """
    with open(reqfile) as file_:
        print(file_.read())


def main(args):
    """
    Main
    """
    args = parse_args(args)
    show(args.req)


if __name__ == '__main__':
    import sys
    main(sys.argv)

