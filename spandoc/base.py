# author: scott olesen <swo@alum.mit.edu>

import select, argparse, os.path, os, sys, glob, subprocess, re, tempfile

def tablify(lines):
    fields = [l.split('\t') for l in lines]
    col_widths = [max([len(x) for x in col_fields]) for col_fields in zip(*fields)]
    padded_fields = [[str.ljust(x, cw) for x, cw in zip(xs, col_widths)] for xs in fields]
    separators = ['-' * cw for cw in col_widths]
    padded_fields.insert(1, separators)
    out_lines = [' '.join(pfs) for pfs in padded_fields]

    return out_lines

def interpolate_tables(lines):
    # look for a line that matches
    match_pattern = '!table\[(.+)\]\s*$'
    for line in lines:
        if re.match(match_pattern, line):
            table_fn = re.match(match_pattern, line).group(1)

            with open(table_fn) as f:
                table_lines = [l.rstrip() for l in f]

            for line in tablify(table_lines):
                yield line
        else:
            yield line

def find_input(fn=None):
    if fn is None:
        # check if reading from stdin
        if select.select([sys.stdin,],[],[],0.0)[0]:
            return (sys.stdin.readlines(), None)
        else:
            # if there is no input, then see if there is one .md in the path
            possible_mds = glob.glob(os.path.join(os.getcwd(), '*.md')) + glob.glob(os.path.join(os.getcwd(), '*.markdown'))
            if len(possible_mds) == 1:
                with open(possible_mds[0]) as f:
                    return (f.readlines(), possible_mds[0])
            elif len(possible_mds) == 0:
                print("no markdown file found in this directory; specify one")
                sys.exit(1)
            elif len(possible_mds) > 1:
                print("multiple markdown files in this directory; specify one")
                sys.exit(1)
    else:
        with open(fn) as f:
            return (f.readlines(), fn)

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

def pandoc_command(input_fn, pandoc_to, output_fn=None, filters=None, variables=None):
    command = ['pandoc', '--to', pandoc_to]

    if output_fn is not None:
        command += ['--output', output_fn]

    if filters is not None:
        command += ['--filter'] + filters

    if variables is not None:
        command += ['-V'] + variables

    command += [input_fn]

    return command

def ok_write_file(fn):
    '''
    Check if the file already exists. If it does, prompt user about whether
    it's OK to overwrite an existing file. Otherwise just say it's OK.
    '''

    if os.path.isfile(fn):
        resp = input("file '{}' already exists. overwite? [y/N] ".format(output_fn))
        return resp.lower() in ['y', 'yes']
    else:
        return True
