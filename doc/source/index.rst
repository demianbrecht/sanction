.. sanction documentation master file, created by
   sphinx-quickstart on Fri Mar 23 19:05:39 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

sanction
========

sanction [sangk-shuhn]: authoritative permission or approval, as for an action. 

.. contents::
   :depth: 3

Why sanction?
-------------
sanction was written to cover issues missed by other implementations:

* Support for multiple providers (protocol deviations). This didn't seem to
  be supported by **any** library.
* Actually an :term:`OAuth2` implementation (python-oauth2 is a 2nd version of 
  python-oauth, not an actual OAuth2 implementation)
* Support for the *entire* OAuth2 spec. Most provide support for the 
  authorization request flow (employed by all web server providers) with
  Bearer token credentials, but lacked support or extensibility for any other
  flows, credentials or other provider extensions)
* 100% unit test coverage. Some employed TDD, others didn't.

Overview
--------
sanction is an implementation of the :term:`OAuth2` protocol that provides the
following features:

* `Fully protocol-compliant`_
* `An extensible framework`_
* `Typed exceptions`_ 
* `100% unit test coverage`_

Fully protocol-compliant
````````````````````````
In the design of this package, the :term:`OAuth2` protocol was analyzed and
used. This differs from other implementations that simply use specific provider
documentation as a base design. In doing this, making the library cross-
provider compatable can become difficult.

For example, even though both Facebook and Google provide access to protected
resources through :term:`OAuth2`, both implementations differ and require
specialized handling at almost every level. For details, see the documentation
for :py:class:`~sanction.adapters.facebook.Facebook` and
:py:class:`~sanction.adapters.google.Google`.

An extensible framework
```````````````````````
There are two parts to the extensibility of the OAuth2 framework:

Firstly, care was taken to ensure that if an implementation for a portion of
the :term:`OAuth2` spec was not designed in up front, that adding it in future
commits would be trivial. For the most part, anywhere that implementations
can be swapped in and out (i.e. providers, flows, credentials, etc.), an
adapter pattern was used.

In some cases where data issued by servers dictate types (rather than 
specifying this at authoring time), factory methods are used to instantiate
types. An example of this in practice is 
:py:meth:`~sanction.exceptions.exception_factory`, which is responsible for
instantiating an exception based on server return data.

Secondly, sanction offers support for provider-specific protocol deviations
and protocol extensions. For example, when access credentials are returned
to the your application, Facebook returns URL-formatted data rather than
JSON. Polymorphic behavior can be used in order to support this by a 
specialized :py:meth:`~sanction.adapters.facebook.Facebook.parse_access_token`
implementation, which parses the URL-formatted data as only required by
Facebook.

Other methods are exposed in order to support deviations as required (most can
be seen by reading through the individual adapter implementations).

Typed exceptions 
````````````````
Exceptions that occur when requests are made (authorization, resource requests,
etc) are typed. This was done to allow for typed exception handling in client
code::

    try:
        client.request("/invalid")
    except AccessDeniedError:
        log.error("Something bad happened")

100% unit test coverage
```````````````````````
If it's not tested, chances are it won't work. Sanction has 100% code coverage.
Of course, this doesn't mean by any stretch that it's problem-free. It simply
means that errors (newly introduced or knock-ons) can be caught in an automated
fashion. TDD is just a Good Thing.


Quickstart
----------

For the quickstart, authorization code grant flow is assumed, as is the
Bearer token type. If you're unfamiliar with these terms, chances are that 
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

Adapters implementations do *not* supply an wrapper for each provider's
API. This isn't the intent of the sanction library.


Other documentation
-------------------

.. toctree::
   :maxdepth: 1

   api.rst


Indices and Glossary 
--------------------

* :ref:`glossary`
* :ref:`genindex`
* :ref:`search`

.. toctree::
   :hidden:

   glossary
