.. sanction documentation master file, created by
   sphinx-quickstart on Tue Aug 20 07:22:31 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

sanction
========

.. image:: https://secure.travis-ci.org/demianbrecht/sanction.png?branch=master
   :target: http://travis-ci.org/#!/demianbrecht/sanction

.. raw:: html

   <iframe style="border: 0; margin: 0; padding: 0;" src="https://www.gittip.com/demianbrecht/widget.html" width="48pt" height="20pt"></iframe>

sanction [sangk-shuhn]: authoritative permission or approval, as for an action. 

.. contents::
   :depth: 3


Overview
--------
sanction is a lightweight, dead simple client implementation of the 
OAuth2 protocol. The major goals of the library are:

- Grok me 
  
  - Variations on OAuth2 client implementation range from a few hundred
    LOC to thousands. In a Pythonic world, there's absolutely no need for
    this when simply dealing with the client side of the spec. Currently,
    sanction sits at a whopping 65 LOC, one class. This makes the library
    tremendously easy to grok.

- Support multiple providers

  - Most providers have varying levels of diversion from the official
    spec. The goal with this library is to either handle these diversions
    natively, or expose a method to allow client code to deal with it 
    efficiently and effectively.
    
- Support all server-side OAuth2 flows

  - Three of the four OAuth2 flows should be supported by this library.
    Currently, only authorization code and client credential flows have
    been tested due to lack of other (known) implementations.

sanction has been tested with the following OAuth2 providers:

* Facebook_ (include the test API)
* Google_
* Foursquare_
* bitly_
* GitHub_
* StackExchange_
* Instagram_
* DeviantArt_

.. _Facebook: https://developers.facebook.com/docs/authentication/
.. _Google: https://developers.google.com/accounts/docs/OAuth2
.. _Foursquare: https://developer.foursquare.com/overview/auth
.. _GitHub: http://developer.github.com/v3/oauth/
.. _Instagram: http://instagram.com/developer/
.. _bitly: http://dev.bitly.com/api.html
.. _StackExchange: https://api.stackexchange.com/docs
.. _Instagram: http://instagram.com/developer/
.. _DeviantArt: http://www.deviantart.com/developers/oauth2

:note: The intention of the sanction library is to not only provide accessibility
       to the OAuth2 authorization code flow, but all server-side flows. However,
       due to lack of implementations, the only tested currently teseted flows
       are authorization code and client credentials.


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

    scope_req = 'scope1,scope2'
    my_redirect(c.auth_uri(scope_req))

:note: (New in 0.4) The scope is assumed to be consistent with the expectations
       of the provider. For example, scope being passed to Facebook should be
       a single string with comma-delimited entities while Google should be
       delimited by spaces (i.e. Facebook: ``scope_req = 'scope1,scope2'``).

You can also elect to use the optional ``state`` parameter to pass a CSRF token
that will be included if the provider's response::

    my_redirect(c.auth_uri(state=my_state))

:note: It is **strongly** encouraged that you use the ``state`` parameter to 
       offer CSRF protection. It is also up to you to process the ``state``
       parameter and handle redirection accordingly *before* calling 
       ``request_token``.


Access Token Request
````````````````````
When the user has granted or denied resource access to your application, they
will be redirected to the ``redirect_uri`` as specified by the value of the ``GET``
param. In order to request an access token from the provider, you must
request an access token from the provider::

    c.request_token(response_dict)


The default parser (``sanction._default_parser``) will attempt to decode JSON,
followed by an attempt to parse querystring-formatted data (i.e. access token
data returned by Facebook). If the provider you're working with has a different
requirement, you can use the ``parser`` parameter of ``request_token`` to pass
another callable that will be responsible for decoding the returned data.


Refreshing Access Tokens
````````````````````````
Some (not all) providers provide the ability to refresh a given access token,
giving an application to users' data even if they're offline (Google is one
of these providers). If your client previously received a refresh token
with the initial code/token exchange, then you can use the ``request_token``
API to request a refreshed token::

    c.request_token(grant_type='refresh_token',
        refresh_token=my_refresh_token)

An example of this is shown in the Google login handler in the sample app.


Resource Request
````````````````

If the user has granted access and your config settings are correct, you should
then be able to access protected resources through the adapter's API::

    c.request("/userinfo")

If the provider has deviated from the OAuth2 spec and the response isn't JSON
(i.e. Stack Exchange), you can pass a custom parser to ``request``::

    c.request("/userinfo", parser=lambda c: dosomething(c))


API
```

.. automodule:: sanction
   :members: 


Notes
-----

There are no implementations for individual OAuth2-exposed resources. This is not
the intention of the library and will not be added.


Thanks
------

* `Alec Taylor`_: Example code refactor.
* `Jake Basile`_: Pointing out the oversight of the ``refresh_token``.
* `Ricky Elrod`_: Python 2.6 string index fix.


.. _`Jake Basile`: https://github.com/jakebasile
.. _`Alec Taylor`: https://github.com/AlecTaylor
.. _`Ricky Elrod`: https://github.com/CodeBlock


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

