py-sanction
===========



.. contents:: Table of Contents 
    :depth: 3


:warning: This module is in WIP state and should not be used until this message
          has been removed.

Overview
--------
py-sanction a fully tested, extensible client implementation of the OAuth2 
protocol [#]_. The goal of this project that sets it apart from other 
implementations is that it aims to provide a core implementation that adheres
to the OAuth2 protocol, while exposing an interface that allows for trivial 
addition of new adapter implementations that must obey their respective
provider idiosyncrasies and/or extensions. 


Quickstart
----------
For the quickstart, `authorization code grant`_ flow is assumed, as is the
Bearer_ token type. If you're unfamiliar with these terms, chances are that 
they're what you're looking for as it's the default in most public OAuth2
provider implementations (Google, Facebook, Foursquare, etc.).

Introducing this library should be rather trivial (in the usual basic case).
There are three steps required in the most common use case (Google is assumed
to be the provider throughout sample code):

Instantiation
`````````````

To access protected resources via the OAuth2 protocol, you must instantiate a 
``Client`` and pass it an adapter implementation to use, as well as a ``dict``
containing configuration information::

    from sanction.client import Client
    from sanction.adapters.google import Google

    client = Client(Google, {
        "google.client_id": "myclientid",
        "google.client_secret": "myclientsecret",
        "google.redirect_uri": "myredirecturi",
        "google.scope": "myscope",
        "google.access_type": "online" # google-specific
    })

Of course, you may create the config ``dict`` in your preferred method, the
above is simply for demonstration using the required config settings (the
example project uses ``ConfigParser`` against an ``.ini`` file for settings.

Authorization Request
`````````````````````
The next step is to redirect the user agent to the provider's authentication/
authorization uri (continuation from previous code block)::

    my_redirect(client.flow.authorization_uri())

You can also elect to use the optional ``state`` parameter to pass a CSRF token
that will be included if the provider's response::

    my_redirect(client.flow.authorization_uri(state=my_state))

:note: It is **strongly** encouraged that you use the ``state`` parameter to 
       offer CSRF protection.


Access Token Request
````````````````````
When the user has granted or denied resource access to your application, they
will be redirected to the ``redirect_uri`` as specified in your config 
settings. In order to request an access token from the provider, you must
tell the ``Client`` that authorization has been received::

    client.flow.authorization_received(server_response_dict)

If the user has granted access and your config settings are correct, you should
then be able to access protected resources through the adapter's API::

    client.request("/userinfo")

Out of the box, the adapters do *not* supply an wrapper for each provider's
API, but if people want to add it, it will definitely be added.


.. _`authorization code grant`: http://tools.ietf.org/html/draft-ietf-oauth-v2-23#section-4.1
.. _Bearer: http://tools.ietf.org/html/draft-ietf-oauth-v2-bearer-08

.. [#] Reference: http://tools.ietf.org/html/draft-ietf-oauth-v2
