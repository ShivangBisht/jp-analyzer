from app.analyzer.kwja_variation import first_mismatch,line_diff,stable_lines
def test_comments_ignored(): assert stable_lines("# x\n* -1D\nEOS\n")==["* -1D","EOS"]
def test_diff_is_private():
 r=line_diff("* -1D\nEOS\n","+ -1D\nEOS\n");assert r["changedLineCount"]==1;assert "leftText" not in r["changed"][0]
def test_code_points():
 r=first_mismatch("a～","a~");assert r["leftCodePoint"]=="U+FF5E";assert r["rightCodePoint"]=="U+007E"
