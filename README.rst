flaskext-search
===============

This script provides a simple command line interface which allows you to
list, search and filter existing flask extensions.

Usage
-----
These are the options provided by the script::

    -l, --list                  Lists every available extension
    -a, --approved-only         Filters the result by approved extensions.
    -s name, --search[=] name   Search for an extension whose name contains the
                                string.
    --search-desc desc          Search for an extension whose description
                                contains the given string.

License
-------
flaskext-search was written and is maintained by Daniel Neuhäuser and is
licensed under the BSD license.
