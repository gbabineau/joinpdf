import os
import tempfile
import unittest
from pypdf import PdfWriter, PdfReader
from joinpdf.joinpdf import (find_pdf_files, merge_pdfs)


class JoinPdfTests(unittest.TestCase):
    def create_pdf(self, path, pages=1):
        writer = PdfWriter()
        for _ in range(pages):
            writer.add_blank_page(width=72, height=72)
        writer.write(path)

    def test_find_pdf_files_pattern(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                self.create_pdf("file_01.pdf")
                self.create_pdf("file_02.pdf")
                self.create_pdf("other.pdf")
                found = find_pdf_files(["file_"])
                self.assertEqual(sorted(found), ["file_01.pdf", "file_02.pdf"])
            finally:
                os.chdir(old_cwd)

    def test_find_pdf_files_explicit(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path1 = os.path.join(tmpdir, "a.pdf")
            path2 = os.path.join(tmpdir, "b.pdf")
            self.create_pdf(path1)
            self.create_pdf(path2)
            found = find_pdf_files([path1, path2])
            self.assertEqual(found, [path1, path2])

    def test_merge_pdfs_creates_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path1 = os.path.join(tmpdir, "a.pdf")
            path2 = os.path.join(tmpdir, "b.pdf")
            output = os.path.join(tmpdir, "merged.pdf")
            self.create_pdf(path1, pages=1)
            self.create_pdf(path2, pages=2)
            merge_pdfs([path1, path2], output)
            reader = PdfReader(output)
            self.assertEqual(len(reader.pages), 3)

    def test_merge_pdfs_raises_on_empty_list(self):
        with self.assertRaises(ValueError):
            merge_pdfs([], "merged.pdf")
