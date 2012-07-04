https://secure.travis-ci.org/demianbrecht/py-sanction.png!":http://travis-ci.org/demianbrecht/py-sanction

sanction [sangk-shuhn]: authoritative permission or approval, as for an action. 

.. contents::
   :depth: 3


:note: sanction has undergone a major overhaul!

       After spending some time with Python in a professional capacity, I decided
       that what I had originally written was quite horribly over-engineered and 
       would take *far* too much effort in maintenance.

       So, the current implementation assumes that you have at least a *basic* 
       understanding of the OAuth2 protocol.


Overview
--------
sanction is an implementation of the OAuth2 protocol that provides the
following features:

* Support for multiple providers
* Simple implementation
    * The simpler the implementation, the easier to understand. At time of writing,
      the entire library is comprised of 71 LOC. This shouldn't be difficult to
      grok, even for the absolute newbie.


sanction has been tested with the following OAuth2 providers:

* Facebook
* Google
* Foursquare


Quickstart
----------

For the quickstart, authorization code grant flow is assumed, as is the
Bearer token type. If you're unfamiliar with these terms, chances are that 
they're what you're looking for as it's the default in most public OAuth2
provider implementations (Google, Facebook, Foursquare, etc.).

Introducing this library should be rather trivial (in the usual basic case).
There are three steps required in the most common use case (Google is assumed
to be the provider throughout sample code):

You can also take a look at the example code in ``/example``.

Instantiation
`````````````

To access protected resources via the OAuth2 protocol, you must instantiate a 
``Client`` and pass it relevant endpoints for your current operation::

    from sanction.client import Client

    # instantiating a client to get the auth URI
    c = Client(auth_endpoint="https://accounts.google.com/o/oauth2/auth",
        client_id=config["google.client_id"],
        redirect_uri="http://localhost:8080/login/google")
    
    # instantiating a client to process OAuth2 response
    c = Client(token_endpoint="https://accounts.google.com/o/oauth2/token",
        resource_endpoint="https://www.googleapis.com/oauth2/v1",
        redirect_uri="http://localhost:8080/login/google",
        client_id=config["google.client_id"],
        client_secret=config["google.client_secret"])


Of course, you may create the config ``dict`` in your preferred method, the
above is simply for demonstration using the required config settings (the
example project uses ``ConfigParser`` against an ``.ini`` file for settings.

Authorization Request
`````````````````````
The next step is to redirect the user agent to the provider's authentication/
authorization uri (continuation from previous code block)::

    scope_req = ("scope1","scope2",)
    my_redirect(c.get_auth_uri(scope_req))

You can also elect to use the optional ``state`` parameter to pass a CSRF token
that will be included if the provider's response::

    my_redirect(client.flow.authorization_uri(state=my_state))

:note: It is **strongly** encouraged that you use the ``state`` parameter to 
       offer CSRF protection. It is also up to you to process the ``state``
       parameter and handle redirection accordingly *before* calling 
       ``auth_received``.


Access Token Request
````````````````````
When the user has granted or denied resource access to your application, they
will be redirected to the ``redirect_uri`` as specified by the value of the ``GET``
param. In order to request an access token from the provider, you must
tell the ``Client`` that authorization has been received::

    c.auth_recieved(response_dict)

If the user has granted access and your config settings are correct, you should
then be able to access protected resources through the adapter's API::

    c.request("/userinfo")

There are no implementations for individual OAuth2-exposed resources. This is not
the intention of the library and will not be added.


TODO's
``````
* Graceful error handling.
