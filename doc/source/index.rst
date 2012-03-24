.. sanction documentation master file, created by
   sphinx-quickstart on Fri Mar 23 19:05:39 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

sanction
========

sanction [sangk-shuhn]: authoritative permission or approval, as for an action. 

.. contents::
   :depth: 2

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
