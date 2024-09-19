import argparse
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def replace_all_parameters(url, canary_1):
    # Parse the URL into components
    parsed_url = urlparse(url)
    
    # Parse the query string into a dictionary
    query_params = parse_qs(parsed_url.query)
    
    # Replace all parameter values
    for key in query_params:
        query_params[key] = [canary_1]
    
    # Encode the query string back into a URL-encoded format
    new_query_string = urlencode(query_params, doseq=True)
    
    # Construct the new URL with the updated query string
    new_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        new_query_string,
        parsed_url.fragment
    ))
    
    return new_url

def check_word_in_response(url, canary_1):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Raise an exception if the request was not successful
        response.raise_for_status()
        
        # Check if the specified word is in the response content
        if canary_1 in response.text:
            print(f"{url} reflects!")
        else:
            print(f"{url} does not reflect. :(")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def process_urls(urls, canary_1):
    for url in urls:
        new_url = replace_all_parameters(url, canary_1)
        check_word_in_response(new_url, canary_1)

def main():
    parser = argparse.ArgumentParser(description='Replace all parameters in a URL with a given value.')
    parser.add_argument('-i', '--input', help='Input URL')
    parser.add_argument('-f', '--file', help='File containing list of URLs')
    
    args = parser.parse_args()
    canary_1 = 'SKJDfklj'
    
    if args.input:
        process_urls([args.input], canary_1)
    elif args.file:
        try:
            with open(args.file, 'r') as file:
                urls = [line.strip() for line in file if line.strip()]
            process_urls(urls, canary_1)
        except FileNotFoundError:
            print(f"The file {args.file} does not exist.")
    else:
        print("You must provide either an input URL with -i or a file with URLs using -f.")

if __name__ == '__main__':
    main()
