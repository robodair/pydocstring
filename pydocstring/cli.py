"""
pydocstring CLI provides entrypoints for CLI commands

Currently only the ``pydocstring`` command is supported

To use pydocstring from the command line you call ``pydocstring`` with the source, and optionally
the position of the cursor within that source (defaults to the end).

Note that pydocstring doesn't insert docstrings in place (yet), as it's designed for editor
integration.
It prints out the generated docstring for the scope the given cursor position is in.

You may also want to provide the ``-f`` flag with the formatter you want to use.

.. code-block:: text

    usage: pydocstring [-h] [-f {google,numpy,reST}] [--version] source [position]

    positional arguments:
    source                Source code to process, or the path to a file
    position              Position of the cursor in the document, defaults to
                          the end. Row, then column

    optional arguments:
    -h, --help            show this help message and exit
    -f {google,numpy,reST}, --formatter {google,numpy,reST}
                            docstring formatter to use
    --version             show program's version number and exit

"""
import sys #pragma: no cover
import os #pragma: no cover
import argparse #pragma: no cover
import ast #pragma: no cover
import pydocstring #pragma: no cover
from pydocstring import exc #pragma: no cover


def main(): #pragma: no cover
    """
    CLI entrypoint
    """
    parser = argparse.ArgumentParser(prog="pydocstring")
    parser.add_argument("source",
                        type=str,
                        help="Source code to process, or the path to a file")
    parser.add_argument("position",
                        nargs="?",
                        type=ast.literal_eval,
                        help="Position of the cursor in the document, defaults to the end. \
                            Row, then column, presented as a string python tuple. E.g. '(10, 15)'")
    parser.add_argument("-f", "--formatter",
                        choices=['google', 'numpy', 'reST'],
                        default='google',
                        type=str,
                        help="docstring formatter to use")
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {0}'.format(pydocstring.__version__))
    parser.add_argument('--debug',
                        action="store_true",
                        help="Show stacktraces")
    args = parser.parse_args()
    source = args.source

    if os.path.exists(args.source):
        with open(args.source) as source_file:
            source = source_file.read()

    lines = source.splitlines()
    position = tuple(args.position) if args.position else (len(lines), len(lines[-1]))
    print(position)

    try:
        output = pydocstring.generate_docstring(source,
                                                position=position,
                                                formatter=args.formatter)
        print('"""\n' + output + '"""\n')
    except Exception as ex:
        if args.debug:
            raise ex
        sys.stderr.write("Could not generate a docstring for the given source:\n")
        sys.stderr.write(repr(ex))
        sys.exit(1)
