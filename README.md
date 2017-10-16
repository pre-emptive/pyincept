# pyincept

A simple framework for non-UI apps

# What's this all about?

Incept provides some of the 'boilerplate' code that most non-UI apps need.
For example, it loads config from a series of YAML files in a standard location,
it can daemonise if required, can drop a PID file, sets up logging, database
connections etc.

Looking around on the Internet, many people say "you don't need a framework, the
language is so expressive!" - all true, but even those people end up writing the
same 50 lines of code for every app they write.

# Why would I want to use it?

Incept is a simple way to ensure that all your apps follow some sort of 'standards'.
It means you don't need to do some of boring things that non-UI apps need, and
most of all that those boring things get done the same way every time you write
such an app.

# How do I use it?

Very simply, you can create a 'hello world' app by running:

`incept init`

That'll create some basic directories and put an "app" called 'app.py' in the app
directory. That's where your code will ultimately go, and of course you're welcome
to create modules, tests or whatever else you need. It's just the 'main' of your
application that goes in the 'app.py' file.

To run your application, you can simply run:

`incept`

There are a few options to have Incept change to a particular directory before
looking for config and the 'app.py' file (or indeed make it look for a different
file). You can also make the process daemonise into the background, whilst
leaving a PID file somewhere so you can find it again if you'd like to as well.
This hopefully makes it easy to run Incept apps from init.d or Systemd start units.

# Installation

To install, run something like this:

`pip install git+https://github.com/pre-emptive/pyincept.git`
