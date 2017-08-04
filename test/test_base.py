# author: scott olesen <swo@alum.mit.edu>

from smart_pandoc.base import *
import pytest

class TestInterpetTo:
    def test_pdf(self):
        assert interpret_to('pdf') == ('latex', 'pdf')

    def test_beamer(self):
        assert interpret_to('beamer') == ('beamer', 'pdf')

    def test_other(self):
        assert interpret_to('docx') == ('docx', 'docx')


class TestNameOutput:
    def test_correct(self):
        assert name_output('foo.md', 'pdf') == 'foo.pdf'
        assert name_output('foo.markdown', 'pdf') == 'foo.pdf'

    def test_bad(self):
        with pytest.raises(AssertionError):
            name_output('foo.txt', 'pdf')


class TestOKWriteFile:
    @pytest.mark.skip(reason="Can't interact with user")
    def test_correct(self, monkeypatch):
        monkeypatch.setattr(__builtins__, 'input', lambda x: 'y')
        assert input('foo') == 'y'
        # I don't know a way to have a test that requires user interaction
        # Test three conditions:
        #  - True if the file doesn't exist
        #  - True if the file exists and the user enters 'Y' or 'y'
        #  - False if the file exists and the user enters something else


class TestPandocCommand:
    def test_bare(self):
        assert pandoc_command('in.md', 'docx') == ['pandoc', '--to', 'docx', 'in.md']

    def test_output(self):
        assert pandoc_command('in.md', 'docx', output_fn='out.docx') == ['pandoc', '--to', 'docx', '--output', 'out.docx', 'in.md']

    def test_filters(self):
        assert pandoc_command('in.md', 'docx', filters=['filter1.hs', 'filter2.hs']) == ['pandoc', '--to', 'docx', '--filter', 'filter1.hs', 'filter2.hs', '--', 'in.md']

    def test_variables(self):
        assert pandoc_command('in.md', 'docx', variables=['papersize=A4', 'toc']) == ['pandoc', '--to', 'docx', '-V', 'papersize=A4', 'toc', '--', 'in.md']

    def test_multiple(self):
        assert pandoc_command('in.md', 'docx', output_fn='out.docx', filters=['filter1.hs', 'filter2.hs'], variables=['papersize=A4', 'toc']) == ['pandoc', '--to', 'docx', '--output', 'out.docx', '--filter', 'filter1.hs', 'filter2.hs', '-V', 'papersize=A4', 'toc', '--', 'in.md']

# def tablify(lines):
#     fields = [l.split('\t') for l in lines]
#     col_widths = [max([len(x) for x in col_fields]) for col_fields in zip(*fields)]
#     padded_fields = [[str.ljust(x, cw) for x, cw in zip(xs, col_widths)] for xs in fields]
#     separators = ['-' * cw for cw in col_widths]
#     padded_fields.insert(1, separators)
#     out_lines = [' '.join(pfs) for pfs in padded_fields]

#     return out_lines

# def interpolate_tables(lines):
#     # look for a line that matches
#     match_pattern = '!table\[(.+)\]\s*$'
#     for line in lines:
#         if re.match(match_pattern, line):
#             table_fn = re.match(match_pattern, line).group(1)

#             with open(table_fn) as f:
#                 table_lines = [l.rstrip() for l in f]

#             for line in tablify(table_lines):
#                 yield line
#         else:
#             yield line

# def find_input(fn=None):
#     if fn is None:
#         # check if reading from stdin
#         if select.select([sys.stdin,],[],[],0.0)[0]:
#             return (sys.stdin.readlines(), None)
#         else:
#             # if there is no input, then see if there is one .md in the path
#             possible_mds = glob.glob(os.path.join(os.getcwd(), '*.md')) + glob.glob(os.path.join(os.getcwd(), '*.markdown'))
#             if len(possible_mds) == 1:
#                 with open(possible_mds[0]) as f:
#                     return (f.readlines(), possible_mds[0])
#             elif len(possible_mds) == 0:
#                 print("no markdown file found in this directory; specify one")
#                 sys.exit(1)
#             elif len(possible_mds) > 1:
#                 print("multiple markdown files in this directory; specify one")
#                 sys.exit(1)
#     else:
#         with open(fn) as f:
#             return (f.readlines(), fn)

