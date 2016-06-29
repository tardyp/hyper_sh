import argparse


def do_up(args):
    print "up"
    pass


def do_down(args):
    print "down"
    pass


def do_rm(args):
    print "rm"
    pass


def main():
    parser = argparse.ArgumentParser(description='deploy docker-compose files into hyper')
    parser.add_argument('--config', dest='config', action='store',
                        help='config file with creds to access hyper api (made through hyper config)')

    subparsers = parser.add_subparsers(help='sub-command help')

    parser_up = subparsers.add_parser('up', help='start a docker-compose file on the cloud')
    parser_up.set_defaults(func=do_up)

    parser_down = subparsers.add_parser('down', help='stop a docker-compose file on the cloud')
    parser_down.set_defaults(func=do_down)

    parser_rm = subparsers.add_parser('rm', help='remove contains created by a docker-compose file on')
    parser_rm.set_defaults(func=do_rm)

    args = parser.parse_args()
    return args.func(args)
