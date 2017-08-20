# author: scott olesen <swo@alum.mit.edu>

import select, argparse, os.path, os, sys, glob, re

def find_markdown_file():
    # if there is no input, then see if there is one .md in the path
    possible_mds = glob.glob(os.path.join(os.getcwd(), '*.md')) + glob.glob(os.path.join(os.getcwd(), '*.markdown'))
    if len(possible_mds) == 1:
        return possible_mds[0]
    elif len(possible_mds) == 0:
        print("no markdown file found in this directory; specify one")
        sys.exit(1)
    elif len(possible_mds) > 1:
        print("multiple markdown files in this directory; specify one")
        sys.exit(1)

def name_output(input_fn, output_ext):
    # check that this is a markdown file
    root, ext = os.path.splitext(input_fn)
    assert ext in ['.md', '.markdown']
    return root + '.' + output_ext

def interpret_to(to):
    '''
    Figure otu the pandoc "to" argument and the output file extension based on
    spandoc's "to" input

    to: str
      "to" argument from the command line
    returns: (str, str)
      pandoc's "to" argument, output file extension
    '''

    if to == 'pdf':
        return ('latex', 'pdf')
    elif to == 'beamer':
        return ('beamer', 'pdf')
    else:
        return (to, to)

def pandoc_command(input_fn, output_fn, pandoc_to, filters=None, variables=None):
    command = ['pandoc', '--to', pandoc_to, '--output', output_fn]

    if filters is not None:
        command += ['--filter'] + filters

    if variables is not None:
        command += ['-V'] + variables

    command += ['--', input_fn]

    return command

def ok_write_file(fn):
    '''
    Check if the file already exists. If it does, prompt user about whether
    it's OK to overwrite an existing file. Otherwise just say it's OK.
    '''

    if os.path.isfile(fn):
        resp = input("file '{}' already exists. overwite? [y/N] ".format(fn))
        return resp.lower() in ['y', 'yes']
    else:
        return True
