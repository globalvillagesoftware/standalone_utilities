#!/usr/bin/env python3
# encoding: utf-8
"""
Utility to move files from one repository to another preserving Git history

:param str branch: The repository branch to be used - defaults to master
:param List[str] files: A list of the paths of the files to be moved
:param str url: The URL of the remote website that hosts the repositories
:return: The exit code of the program
:rtype: int
@author:     Jonathan Gossage

@copyright:  2020 Jonathan Gossage. All rights reserved.

@license:    Apache2

@contact:    jgossage@gmail.com
@deffield    updated: Updated
"""

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from lib.helpers import ActionRepo, ActionUrl

__all__ = []
__version__ = 0.1
__date__ = '2020-05-07'
__updated__ = '2020-05-07'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)'\
                               % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = """%s

  Created by Jonathan Gossage on %s.
  Copyright 2020 Jonathan Gossage. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
""" % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count",
                            help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version',
                            version=program_version_message)
        parser.add_argument('oldrepo', action=ActionRepo, nargs=1,
                            help='path to the old (from) repository')
        parser.add_argument('newrepo', action=ActionRepo, nargs=1,
                            help='path to the new (to) repository')
        parser.add_argument('-u', '--url', action=ActionUrl, nargs=1,
                            help='Url of the remote site that contains'
                                 ' remote copies of the repository')
        parser.add_argument('files', store='append',
                            help='list of paths to files that are to be moved')

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")

        return doit(args)
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as E:
        if DEBUG or TESTRUN:
            raise E
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(E) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        PROFILE_FILENAME = 'move_files_from_rep_profile.txt'
        cProfile.run('main()', PROFILE_FILENAME)
        STATSFILE = open("profile_stats.txt", "wb")
        P = pstats.Stats(PROFILE_FILENAME, stream=STATSFILE)
        STATS = P.strip_dirs().sort_stats('cumulative')
        STATS.print_stats()
        STATSFILE.close()
        sys.exit(0)
    sys.exit(main())

def doit(args):
    """Contains application specific logic"""
    return 0
