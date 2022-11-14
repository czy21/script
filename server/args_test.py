import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--p1')
    parser.add_argument('-h', '--help', help="hahaha")

    parser_1 = argparse.ArgumentParser(parents=[parser], usage="haha")
    parser_1.add_argument('--a1')
    print(parser_1.parse_args())
    # args = parser.parse_args()
    # print(args)
