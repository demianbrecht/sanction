.. _glossary:

Glossary
========

.. glossary::
   :sorted:

   stateless requests
    A method of conducting OAuth2 requests such that the application is not
    responsible to store credentials. This means that for every request, the
    client application will request an access token from the OAuth2 provider.
    Not only will this slow down your application, but it increases the chance
    of hitting limits imposed by the providers.

   oauth2
    The protocol allowing for protected resource access that the sanction 
    library was built to support.
    Everything that you need to know about OAuth2 can be `found here`_.

.. _`found here`: http://oauth.net/2/
