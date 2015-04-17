#Webserver example

This examples shows a simple webserver handling sessions using
cookies. It serves simple dynamic pages defined in the application.

Sessions are a dictionnary binding keys to string values, they use
cookies to comunicate with the web browser.

Pages are instances of the `Page` class. They use the `__str__` method
to return their html code. The `call` method of page instances is
called when the page is asked. It generate the content of the page.

##The initial version

The initial version serves three different pages : banana, coconut and
hello. Each of these pages displays a small message and the number of
time it has been requested by the user.

The latter part is achieved by storing the number of requests for each
page in the current session.

##The update

Now we want to add authentication handling to the server. For this
purpose, we need to do some modifications :

1. Add a `User` class holding logins and password. 
2. Add a login attribute to the `Session` class
3. Add a login page to the webserver
4. Modify the `Page` to make it display the login of the current session

To update the `Session` instances, we will use Lazy update because
there may be many of them to update. Lazy update will permit to update
sessions when theyr are needed.

To update the `Page` instances, we will use Eager update because we
want all pages to be updated immediately.

In order to update the web server and the handler, we will need a
custom made manager since accessing these elements may be
complicated. This custom manager will update the instance of
`Webserver` when no method of `Handler` instances are in the stack.





