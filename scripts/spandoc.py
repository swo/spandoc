#!/usr/bin/env python3
#
# author: scott olesen <swo@alum.mit.edu>

import smart_pandoc.base as sd
import smart_pandoc.watch
import argparse, subprocess

if __name__ == '__main__':
    p = argparse.ArgumentParser(description="'smart' pandoc: a wrapper with some intelligent defaults")
    p.add_argument('input', nargs='?', help='markdown file (leave blank and spandoc will use the only markdown file in this directory; use "-" for stdin)')
    p.add_argument('--to', '-t', default='pdf', choices=['beamer', 'pdf', 'html', 'docx'], help='output format')
    p.add_argument('--force', '-f', action='store_true', help='overwrite existing file?')
    p.add_argument('--verbose', '-v', action='store_true', help='verbose output')
    p.add_argument('--filters', nargs='*', default=['pandoc-citeproc'], help='pandoc filters (default: only citeproc)')
    p.add_argument('--variables', nargs='*')
    p.add_argument('--watch', '-w', action='store_true', help='continually run pandoc?')
    p.add_argument('--output', '-o', help='specify output file (otherwise, let spandoc guess)')
    args = p.parse_args()

    # figure out pandoc "to" type based on the extension
    pandoc_to, output_ext = sd.interpret_to(args.to)

    # guess the input file if none was provided
    if args.input is None:
        input_fn = sd.find_markdown_file()
    else:
        input_fn = args.input

    # guess the output file if none was provided
    if args.output is None:
        output_fn = sd.name_output(input_fn, output_ext)
    else:
        output_fn = args.output

    # check that output file destination is blank
    if not (args.force or sd.ok_write_file(output_fn)):
        print('not overwriting; use -f to force overwrite')
        sys.exit(0)

    # build the system command to run pandoc
    command = sd.pandoc_command(input_fn, output_fn, pandoc_to, args.filters, args.variables)
    callback = lambda: subprocess.call(command)

    # run pandoc
    callback()

    # if watching, continue to call pandoc as the file changes
    if args.watch:
        smart_pandoc.watch.watch(input_fn, callback, args.verbose)
