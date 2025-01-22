from argparse import ArgumentParser
from src.biomark import retrieveData


def main():
    # Main arguments included in command line execution of program,
    # useful for running program from a systemd service file.
    parser = ArgumentParser(description='Program to retrieve PIT data from IS1001s')
    parser.add_argument('client_file', type=str, help='/path/to/client/file.txt')
    args = parser.parse_args()

    retrieve = retrieveData(args.client_file)

    raw_data = retrieve.pitTags('10.30.8.6')
    formatted_data = retrieve.formatTagData(raw_data)
    print(formatted_data)


if __name__ == '__main__':
    main()

