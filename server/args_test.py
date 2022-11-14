import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--param', nargs="+", default=[])
    parser_command = parser.add_subparsers(title="Command", metavar="", dest="command")
    parser_install = parser_command.add_parser("install", help="install role")
    parser_install.add_argument('--param', nargs="+", default=[])
    parser_install.add_argument('--file', type=str)
    parser_command.add_parser("delete", help="delete role")

    args = parser.parse_args()

    print(args)
