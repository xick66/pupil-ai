import argparse
import requests

url = 'http://localhost:5000/directory/'
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Co-pet server CLI.")

    # Add the directory argument
    parser.add_argument("--directory", help="Specify the directory path.")

    # Parse the arguments
    args = parser.parse_args()

    # Access the directory argument value
    directory_path = args.directory

    # Your script logic here
    if directory_path:
        print("Directory specified:", directory_path)
        response = requests.get(url + directory_path)
        print(response)
    else:
        print('cannot execute without dir')