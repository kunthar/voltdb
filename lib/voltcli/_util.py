# This file is part of VoltDB.

# Copyright (C) 2008-2011 VoltDB Inc.
#
# This file contains original code and/or modifications of original code.
# Any modifications made by VoltDB Inc. are licensed under the following
# terms and conditions:
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# Completely independent simple utility functions. Can be safely imported
# before full initialization complets. This namespace gets absorbed into util,
# so most places should import vcli_util rather than _util.

__author__ = 'scooper'

import sys
import os

def display_messages(msgs, f = sys.stdout, tag = None, level = 0):
    """
    Low level message display.
    """
    if tag:
        stag = '%8s: ' % tag
    else:
        stag = ''
    # Special case to allow a string instead of an iterable.
    try:
        # Raises TypeError if not string
        var = msgs + ' '
        msgs = [msgs]
    except TypeError:
        pass
    sindent = level * '  '
    # Recursively process message list and sub-lists.
    for msg in msgs:
        if msg is not None:
            # Handle exceptions
            if issubclass(msg.__class__, Exception):
                f.write('%s%s%s Exception: %s\n' % (stag, sindent, msg.__class__.__name__, str(msg)))
            else:
                # Handle multi-line strings
                try:
                    # Raises TypeError if not string
                    var = msg + ' '
                    # If it is a string slice and dice it by linefeeds.
                    for msg2 in msg.split('\n'):
                        f.write('%s%s%s\n' % (stag, sindent, msg2))
                except TypeError:
                    # Recursively display an iterable with indentation added.
                    if hasattr(msg, '__iter__'):
                        display_messages(msg, f = f, tag = tag, level = level + 1)
                    else:
                        f.write('%s%s%s\n' % (stag, sindent, str(msg)))

def info(*msgs):
    """
    Display INFO level messages.
    """
    display_messages(msgs, tag = 'INFO')

def warning(*msgs):
    """
    Display WARNING level messages.
    """
    display_messages(msgs, tag = 'WARNING')

def error(*msgs):
    """
    Display ERROR level messages.
    """
    display_messages(msgs, tag = 'ERROR')

def abort(*msgs):
    """
    Display ERROR messages and then abort.
    """
    error(*msgs)
    display_messages('Errors are fatal, aborting execution', f = sys.stderr, tag = 'FATAL')
    sys.exit(1)

def find_in_path(name):
    """
    Find program in the system path.
    """
    # NB: non-portable
    for dir in os.environ['PATH'].split(':'):
        if os.path.exists(os.path.join(dir, name)):
            return os.path.join(dir, name)
    return None