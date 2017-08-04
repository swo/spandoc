#!/usr/bin/env python3
#
# author: scott olesen <swo@alum.mit.edu>

#from spandoc.base import *
import smart_pandoc.base as sd
import argparse, tempfile, subprocess, os, sys

if __name__ == '__main__':
    p = argparse.ArgumentParser(description="'smart' pandoc: a wrapper with some intelligent defaults")
    p.add_argument('input', nargs='?', help='markdown file (leave blank and spandoc will use the only markdown file in this directory)')
    p.add_argument('--to', '-t', default='pdf', choices=['beamer', 'pdf', 'html', 'docx'], help='output format')
    p.add_argument('--force', '-f', action='store_true', help='overwrite existing file?')
    p.add_argument('--verbose', '-v', action='store_true', help='print pandoc command?')
    p.add_argument('--filters', nargs='*', default=['pandoc-citeproc'], help='pandoc filters (default: only citeproc)')
    p.add_argument('--variables', nargs='*')
    args = p.parse_args()

    # figure out pandoc "to" type based on the extension
    pandoc_to, output_ext = sd.interpret_to(args.to)

    # figure out the input/output mode: stream or file
    # input_fn = None implies streaming mode
    input_lines, input_fn = sd.find_input(args.input)

    # write interpolated lines to a temporary file
    tempf = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False)
    for line in sd.interpolate_tables(input_lines):
        print(line.rstrip(), file=tempf)

    tempf.close()

    # find the output file
    # if streaming mode, None; if file mode, a filename
    if input_fn is None:
        # streaming mode
        output_fn = None
    else:
        # guess the output name
        output_fn = sd.name_output(input_fn, output_ext)

        # check that this is not used
        if not (args.force or sd.ok_write_file(output_fn)):
            print('not overwriting')
            sys.exit(0)

    # build the system command to run pandoc
    # (we always read from the temporary file)
    command = sd.pandoc_command(tempf.name, pandoc_to, output_fn, args.filters, args.variables)

    if args.verbose:
        print('tempfile:', tempf.name)
        print('command:', *command)

    subprocess.run(command)

    os.remove(tempf.name)
