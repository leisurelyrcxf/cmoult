#A Simple Server

This application manages a set of sites, each of them having multiple
pages. Users can register then login to the application to handle
pages.

Users communicate with the application through a socket server
listening on port 8080.

Here are the available commands :

- register _username_ : creates a new account if _username_ is not
  already used.
- login _username_ : logs in as _username_ if such an username exists.
- logout : logs out the user currently logged in
- create site _name_ : creates a new site with the given _name_ if no
  site already has this name.
- create page _sname_ _name_ : creates a page with the given _name_ in
  the site named _sname_ if the site exists and no page has this
  _name_ in the site.
- delete site _name_ : deletes the site named _name_ if it exists
- delete page _sname_ _name_ : deletes the page named _name_ from site named _sname_ if both exist.
- show all : shows all the pages of all the sites
- show site _name_ : shows the pages of the site of the given _name_ if it exists.
- show page _sname_ _name_ : shows the page named _name_ of the site named _sname_ if both exist.

The file `server.py` contains the code of the application.

##The update

We want to add right managements to the application. We want users to
be able to access only sites they created or that were created by
their friends. We also want to enable users to declare their friends
in the application.

After update, the following command will be available :

- register _username_ : creates a new account if _username_ is not
  already used.
- login _username_ : logs in as _username_ if such an username exists.
- logout : logs out the user currently logged in
- create site _name_ : creates a new site with the given _name_ if no
  site already has this name. The created site will belong to the logged user. 
- create page _sname_ _name_ : creates a page with the given _name_ in
  the site named _sname_ if the site exists and no page has this
  _name_ in the site. Does nothing if the logged user does not have access to the site.
- delete site _name_ : deletes the site named _name_ if it exists and
  the logged user has access to it.
- delete page _sname_ _name_ : deletes the page named _name_ from site
  named _sname_ if both exist. Does nothing if the logged user does
  not have access to the site.
- show all : shows all the pages of all the sites the logger user can
  access.
- show site _name_ : shows the pages of the site of the given _name_
  if it exists and the logged user can access it.
- show page _sname_ _name_ : shows the page named _name_ of the site
  named _sname_ if both exist. Does nothing if the logged user does
  not have access to the site.

Commands supplied while no user is logged will be ignored (unless the commands are __register__ or __login__)

All sites created before the update will be considered public and
therefore be accessible by everyone.

The file `update.py` contains the code of the update. Keepin mind that
it is not yet ready to be applied.


## Implementing the update

The update has been implemented as if the application were using the
following platforms : Kitsune or K42. Each implentation is in a
seperate folder (kitsune for Kitsune, k42 for K42).

For emulating Kitsune, we use a `ThreadRebootManager`, a
`HeapTraversalManager` and use a `DSU_Thread` for static detection of
alterability. Managers are set up and started in the application.

For emulating K42, we use a `SafeRedefineManager` and a
`LazyConversionManager`. Managers are started in the update.












