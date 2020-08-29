"""Functions for interfacing with Glances webservers"""
import requests


def request_data(address, endpoint, port=61208, api_version=3, timeout=0.5):
    """Perform the GET request to the specified server and endpoint

    Args:
        address (str): the address of the server to query
        endpoint (str): the desired endpoint
            See: https://github.com/nicolargo/glances/wiki/The-Glances-RESTFULL-JSON-API
        port (int, optional): the port on which the server is running
            Default is 61208
        api_version (int, optional): The server's Glances API version.
            Default is 3
        timeout (float, optional): Timeout time (in seconds) for the request.
            Default is 0.5

    Returns:
        dict: the server's response

    Raises:
        requests.ConnectionError
            If the server cannot be reached
        ValueError
            If the response cannot be translated to JSON
    """
    if api_version != 3:
        raise NotImplementedError('ataglances only supports the Glances v3 API')
    return requests.get(f'http://{address}:{port}/api/{api_version}/{endpoint}',
                        timeout=timeout).json()


def convert_list_response_to_dict(list_response):
    """Converts the raw Glances API JSON response from lists of dicts to dicts of dicts,
    which will be a lot easier to work with.

    Args:
        list_response (list of dict): the raw API list-of-dict response

    Returns:
        dict of str to dicts: the reshaped response data
    """
