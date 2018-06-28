# ------------------------------------------------------------------------
#
#  This file is part of the Chirp Connect Python SDK.
#  For full information on usage and licensing, see https://chirp.io/
#
#  Copyright (c) 2011-2018, Asio Ltd.
#  All rights reserved.
#
# ------------------------------------------------------------------------
import requests

from .exceptions import ConnectNetworkError


def get_licence_data(key, secret, name=None):
    """
    Retrieve a licence for an application.
    If name is specified then this licence is returned, otherwise
    the default is used.

    Args:
        name (str): Licence name, default is used if not set

    Returns: (str) licence string

    Raises:
        ConnectNetworkError: If licence request fails
        ValueError: If an invalid licence name is requested
    """
    try:
        url = 'https://licence.chirp.io/v3/connect'
        r = requests.get(url, auth=(key, secret))
        if r.status_code != 200:
            err = r.json()
            raise ConnectNetworkError(err.get('message', 'Failed to retrieve licence'))
        data = r.json()
        licences = [l['name'] for l in data['data']]
        if name and name not in licences:
            raise ValueError('Invalid licence name')
        return data['data'][licences.index(name)] if name else data['data'][0]['licence']
    except requests.exceptions.ConnectionError:
        raise ConnectNetworkError('No internet connection')
    except requests.exceptions.Timeout:
        raise ConnectNetworkError('Timeout')
    except requests.exceptions.RequestException as err:
        raise ConnectNetworkError(str(err))
