"""Source parsing must reject service pages and distinguish exact shelfmarks."""
import csv
import importlib.util
import io
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location("ncl_probe",Path(__file__).resolve().parents[1]/"scripts/probe-tianwen-13gi-ncl-catalog.py")
probe=importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

class TestCatalogParsing(unittest.TestCase):
 def source(self,rows,encoding="cp950",delimiter=","):
  text=io.StringIO(newline="")
  writer=csv.writer(text,delimiter=delimiter)
  writer.writerow(["正題名","書號","索書號","作者","版本"])
  writer.writerows(rows)
  return text.getvalue().encode(encoding)

 def test_cp950_exact_row_and_date_verbatim(self):
  version="清初葉舊鈔光緒間(1644-1735)錢塘丁氏補鈔本"
  data=self.source([["高麗史","03130","208 03130","鄭麟趾",version]])
  parsed=probe.parse_csv(data)
  self.assertEqual(parsed["decoding"],"cp950")
  self.assertEqual(parsed["exact_book_number_rows"][0]["bibliographic_fields"]["版本"],version)
  self.assertEqual(parsed["exact_book_number_rows"][0]["csv_row_1based"],2)

 def test_title_number_is_only_fuzzy_and_prefix_does_not_match(self):
  parsed=probe.parse_csv(self.source([
   ["03130參照","99999","999 99999","某","某版"],
   ["其他書","103130","208 103130","某","某版"],
   ["高麗史","03130","208 03130","鄭麟趾","舊鈔本"],
  ]))
  self.assertEqual(len(parsed["candidate_rows"]),2)
  self.assertEqual(len(parsed["exact_book_number_rows"]),1)
  self.assertEqual(parsed["exact_book_number_rows"][0]["csv_row_1based"],4)

 def test_quoted_multiline_field_and_utf8_tab_export(self):
  parsed=probe.parse_csv(self.source([["高麗史","03130","208 03130","鄭麟趾","舊鈔,補鈔\n未定"]],"utf-8-sig","\t"))
  self.assertEqual(parsed["rows_checked"],1)
  self.assertEqual(parsed["exact_book_number_rows"][0]["bibliographic_fields"]["版本"],"舊鈔,補鈔\n未定")

 def test_no_match_is_report_only(self):
  parsed=probe.parse_csv(self.source([["其他書","00100","208 00100","某","某版"]]))
  self.assertEqual(parsed["rows_checked"],1)
  self.assertEqual(parsed["exact_book_number_rows"],[])

 def test_html_and_wrong_schema_rejected(self):
  for data in (b"<!doctype html><html>503,service unavailable</html>",b"title,number\nbook,03130\n"):
   with self.subTest(data=data),self.assertRaises(ValueError):probe.parse_csv(data)

 def test_truncated_record_and_match_overflow_rejected(self):
  for rows in ([["高麗史","03130"]],[["高麗史","03130","208 03130","鄭麟趾","舊鈔"]]*21):
   with self.subTest(count=len(rows)),self.assertRaises(ValueError):probe.parse_csv(self.source(rows))

if __name__=="__main__":unittest.main()
