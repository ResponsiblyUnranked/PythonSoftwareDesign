# Python Software Design

A collection of examples of how to apply various software design patterns in Python.

It is primarily focused around Object-Oriented Programming (OOP).

## Introduction

### TL;DR

There are too many beginner tutorials for Python, but few tutorials teaching design
patterns and best-practices in Python. This repository is a resource for Python
developers looking to enhance their skills, and ultimately write better software.

### Inspiration

This project is hugely inspired by [ArjanCodes](https://www.youtube.com/@ArjanCodes)
and [Dive into Design Patterns](https://refactoring.guru/design-patterns/book) by
Alexander Shvets.

Please check out their work and support them, because this project wouldn't exist if it
wasn't for their amazing content (not sponsored).

### What?

This is a collection of various best-practices, design patterns, anti-patterns, and
other useful code examples in Python. Its main goal is to make design patterns in
Python approachable and easy to understand. It's here to turn Python "scripters" into
Python "developers".

If you find yourself wanting to not just write code that works, but code that:

- works _well_
- is easy for other people to understand
- is easy to update and modify
- stays clean, even as your project grows

then this project should be able to help.

### Why?

Python is a great language. Because of how easy it is to learn, there are tons of
beginner-level tutorials on the language. This is great because it makes programming
more accessible for people who are interested.

The downside of this, is that there are a lot of people who learn programming in Python,
but miss key aspects that can really improve your code. Even if you are someone who will
only ever write Python scripts for your own personal use, there are things that you can
do that will improve your code, even just for yourself!

The most obvious example of this is the omission of type hints in beginner tutorials.
While not using type hints makes it easier to get started in Python, it makes your code
much, _much_ more difficult to understand, and I believe beginner tutorials should be
using type hints. They are also the backbone of good interface design.

This is also my playground as a developer to learn more about the design patterns myself
and add more examples as I learn about them.

## Project Layout

The project follows a simple Python packaging layout with each new design pattern, 
principle, or best-practice having its own package (folder with `__init__.py`) under 
`src/`.

Some ideas can be grouped as a collection, like the 
[SOLID](https://en.wikipedia.org/wiki/SOLID) principles, and will therefore be 
grouped under `src/solid/`.

Each principle will have an accompanying `README.md` file with some explanation of 
the principle, and the following code. Where possible, I will provide anti-patterns too.

Please consult the wiki for a guide on navigating all these principles, especially 
if you are a beginner looking for a structured approach to learning all the concepts.

## Contributing

All contributions, criticisms, and comments are welcome. I am just a single developer
working on this project in my free time, and I will probably make mistakes!
So I'm happy for you to contribute corrections too.

Please read
[CONTRIBUTING.md](https://github.com/Jamie-McKernan/PythonSoftwareDesign/blob/master/CONTRIBUTING.md)
for more information.