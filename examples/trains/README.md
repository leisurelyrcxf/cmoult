#I like trains!


This application handle a fleet of trains circling through Paris.
This application model is the following

A train has color, speed and an initial position.
A Lane element is either a Rail or a Station.
A Lane has a starting Station followed by any number of Lane element.

Each Station has a maximum capacity and each Rail as a length.

Before leaving a station, a train has to check if all along its journey, 
it will stay alone on any rail it circulates on and if there will be enough 
room for it at the next Station. 


##How the update works


The application only uses the Listener of Pymoult. No manager is
started whith the application.

The update is composed of two steps :

1. update the trains
2. update the lane elements

###Updating the trains

We first provide the new methods that will be added to the Train
class : the `__init__` method will be redefined and a
`switch_direction` method will be added.

After defining the `getTrainThreads` that will get all the train
objects (which are also threads) we use it in the custom TrainManager
that will add the `direction` attribute to each train before handling
the method redefinition and addition.

In this step, the manager is user-defined, added on-the-fly and
specific to this update. Since it is very specific and already
configured, we don't define to use an Update class with it.

###Updating the line elements

Here, we want to use safe redefinition (redefining a function when it
is not in the stack) for the methods we need to redefine. Since the
SafeRedefinitionManager provided by Pymoult does not handle
redefinition of methods, we extend it in a new manager:
`SafeRedefMethod` with its associated `SafeRedefMethodUpdate` class.

Then, we use this manager to update the methods. We have to update the
`can_enter` method of the Rail class before updating the other methods
in order to keep the execution safe (__i.e.__ not allowing two train
in oposite direction entering in a same line).

When this first substep is complete, we can proceed with the update of
the other methods. 


##Running the example


To start the text based example, simply run `./test.sh` script.
To launch the graphical example, launch the script with the gui argument :
`./test.sh gui`



