"""
Unit tests for CLI helper functions.

Tests utility functions from spaider.utils.document that perform parsing, filtering, and formatting.
"""

import unittest
import sys
import json
import io
import contextlib
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "spaider" / "scripts"))

from spaider.utils.document import (
    file_has_spaider_markers,
    get_content_scoped_without_markers,
    iter_text_files,
    read_text_safe,
    scan_sdsl_instructions_without_markers,
    scan_spd_ids_without_markers,
    to_relative_posix,
)

from spaider.utils import document as doc

from spaider import cli as spaider_cli


class TestRelativePosix(unittest.TestCase):
    """Test to_relative_posix function."""

    def test_relative_path_within_root(self):
        """Test relative path within root."""
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            subpath = root / "subdir" / "file.txt"

            rel = to_relative_posix(subpath, root)

            self.assertEqual(rel, "subdir/file.txt")

    def test_absolute_path_outside_root(self):
        """Test absolute path when outside root."""
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "root"
            outside = Path(tmpdir) / "outside" / "file.txt"

            rel = to_relative_posix(outside, root)

            # Should return absolute path when outside root
            self.assertIn("outside", rel)


class TestIterTextFiles(unittest.TestCase):
    def test_iter_text_files_include_exclude_and_max_bytes(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "a").mkdir()
            (root / "a" / "small.md").write_text("x\n", encoding="utf-8")
            (root / "a" / "big.md").write_text("x" * 200, encoding="utf-8")
            (root / "a" / "skip.md").write_text("x\n", encoding="utf-8")

            hits = iter_text_files(
                root,
                includes=["**/*.md"],
                excludes=["**/skip.md"],
                max_bytes=100,
            )
            rels = sorted([p.resolve().relative_to(root.resolve()).as_posix() for p in hits])
            self.assertEqual(rels, ["a/small.md"])

    def test_iter_text_files_relative_to_value_error_is_ignored(self):
        import os
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)

            orig_walk = os.walk

            def fake_walk(_root):
                yield ("/", [], ["outside.md"])

            os.walk = fake_walk
            try:
                hits = iter_text_files(root)
                self.assertEqual(hits, [])
            finally:
                os.walk = orig_walk


class TestReadTextSafe(unittest.TestCase):
    def test_read_text_safe_nonexistent_returns_none(self):
        with TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "missing.txt"
            self.assertIsNone(read_text_safe(p))

    def test_read_text_safe_null_bytes_returns_none(self):
        with TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "bin.txt"
            p.write_bytes(b"a\x00b")
            self.assertIsNone(read_text_safe(p))

    def test_read_text_safe_invalid_utf8_ignores(self):
        with TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "bad.txt"
            p.write_bytes(b"hi\xff\xfe")
            lines = read_text_safe(p)
            self.assertIsNotNone(lines)
            self.assertTrue(any("hi" in x for x in lines or []))

    def test_read_text_safe_normalizes_crlf_when_linesep_differs(self):
        import os

        with TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "crlf.txt"
            p.write_bytes(b"a\r\nb\r\n")

            orig = os.linesep
            try:
                os.linesep = "\r\n"
                lines = read_text_safe(p)
                self.assertEqual(lines, ["a", "b"])
            finally:
                os.linesep = orig


class TestCliInternalHelpers(unittest.TestCase):
    def test_load_json_file_invalid_json_returns_none(self):
        with TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "bad.json"
            p.write_text("{bad}", encoding="utf-8")
            self.assertIsNone(spaider_cli._load_json_file(p))

    def test_load_json_file_non_dict_returns_none(self):
        with TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "list.json"
            p.write_text(json.dumps([1, 2, 3]), encoding="utf-8")
            self.assertIsNone(spaider_cli._load_json_file(p))

    def test_safe_relpath_from_dir_fallbacks_to_absolute_on_error(self):
        with TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            target = base / "x" / "y"
            with patch("os.path.relpath", side_effect=Exception("boom")):
                rel = spaider_cli._safe_relpath_from_dir(target, base)
            self.assertEqual(rel, target.as_posix())

    def test_prompt_path_eof_returns_default(self):
        with patch("builtins.input", side_effect=EOFError()):
            out = spaider_cli._prompt_path("Q?", "default")
        self.assertEqual(out, "default")

    def test_safe_relpath_outside_base_returns_absolute(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "root"
            other = Path(tmpdir) / "other" / "x.txt"
            out = spaider_cli._safe_relpath(other, root)
            self.assertEqual(out, other.as_posix())

    def test_write_json_file_writes_trailing_newline(self):
        with TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "out.json"
            spaider_cli._write_json_file(p, {"a": 1})
            raw = p.read_text(encoding="utf-8")
            self.assertTrue(raw.endswith("\n"))
            self.assertEqual(json.loads(raw), {"a": 1})


class TestCliCommandCoverage(unittest.TestCase):
    def test_self_check_project_root_not_found(self):
        with TemporaryDirectory() as td:
            with patch.object(spaider_cli, "find_project_root", return_value=None):
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    code = spaider_cli._cmd_self_check(["--root", td])
        self.assertEqual(code, 1)

    def test_self_check_adapter_dir_not_found(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / ".git").mkdir()
            with patch.object(spaider_cli, "find_project_root", return_value=root):
                with patch.object(spaider_cli, "find_adapter_directory", return_value=None):
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        code = spaider_cli._cmd_self_check(["--root", td])
        self.assertEqual(code, 1)

    def test_self_check_registry_no_rules(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / ".git").mkdir()
            adapter = root / ".spaider-adapter"
            adapter.mkdir()
            with patch.object(spaider_cli, "find_project_root", return_value=root):
                with patch.object(spaider_cli, "find_adapter_directory", return_value=adapter):
                    with patch.object(spaider_cli, "load_artifacts_registry", return_value=({"version": "1.0"}, None)):
                        buf = io.StringIO()
                        with contextlib.redirect_stdout(buf):
                            code = spaider_cli._cmd_self_check(["--root", td])
        self.assertEqual(code, 1)

    def test_self_check_with_rules_structure(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / ".git").mkdir()
            adapter = root / ".spaider-adapter"
            adapter.mkdir()
            # Create rules structure
            weavers_dir = root / "weavers" / "test" / "artifacts" / "PRD"
            weavers_dir.mkdir(parents=True)
            (weavers_dir / "template.md").write_text(
                "---\n"
                "spaider-template:\n  version:\n    major: 1\n    minor: 0\n  kind: PRD\n"
                "---\n\n# PRD\n",
                encoding="utf-8",
            )
            # No example - should warn but pass (no examples = no failures)
            registry = {
                "version": "1.0",
                "weavers": {
                    "test-rules": {"format": "Spaider", "path": "weavers/test"}
                },
            }
            with patch.object(spaider_cli, "find_project_root", return_value=root):
                with patch.object(spaider_cli, "find_adapter_directory", return_value=adapter):
                    with patch.object(spaider_cli, "load_artifacts_registry", return_value=(registry, None)):
                        buf = io.StringIO()
                        with contextlib.redirect_stdout(buf):
                            code = spaider_cli._cmd_self_check(["--root", td])
        # PASS when no examples exist (warnings only)
        self.assertEqual(code, 0)

    def test_init_yes_dry_run(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = spaider_cli.main(["init", "--project-root", str(root), "--yes", "--dry-run"])
        self.assertEqual(rc, 0)

    def test_main_missing_subcommand_returns_error(self):
        rc = spaider_cli.main([])
        self.assertEqual(rc, 1)

    def test_main_unknown_command_returns_error(self):
        rc = spaider_cli.main(["does-not-exist"])
        self.assertEqual(rc, 1)


class TestNormalizeSpdIdFromLine(unittest.TestCase):
    def test_normalize_empty_returns_none(self):
        self.assertIsNone(doc._normalize_spd_id_from_line(""))

    def test_normalize_id_label_line(self):
        self.assertEqual(doc._normalize_spd_id_from_line("**ID**: `spd-test-1`"), "spd-test-1")

    def test_normalize_backticked_exact(self):
        self.assertEqual(doc._normalize_spd_id_from_line("`spd-test-2`"), "spd-test-2")

    def test_normalize_fullmatch_and_fallback_findall(self):
        self.assertEqual(doc._normalize_spd_id_from_line("spd-test-3"), "spd-test-3")
        self.assertEqual(doc._normalize_spd_id_from_line("prefix spd-test-4 suffix"), "spd-test-4")


class TestMarkerlessScanners(unittest.TestCase):
    def test_file_has_spaider_markers_false_on_read_error(self):
        with TemporaryDirectory() as td:
            p = Path(td) / "missing.md"
            self.assertFalse(file_has_spaider_markers(p))

    def test_scan_spd_ids_without_markers_skips_when_markers_present(self):
        with TemporaryDirectory() as td:
            p = Path(td) / "a.md"
            p.write_text("<!-- spd:id:item -->\n- [ ] **ID**: `spd-test-1`\n<!-- spd:id:item -->\n", encoding="utf-8")
            self.assertEqual(scan_spd_ids_without_markers(p), [])

    def test_scan_spd_ids_without_markers_def_ref_inline_and_fences(self):
        with TemporaryDirectory() as td:
            p = Path(td) / "a.md"
            p.write_text(
                "- [x] `p1` - **ID**: `spd-test-1`\n"
                "- `spd-test-1`\n"
                "* `spd-test-2`\n"
                "Inline `spd-test-3` here\n"
                "```\n"
                "- [x] `p1` - **ID**: `spd-in-fence`\n"
                "- `spd-in-fence`\n"
                "```\n",
                encoding="utf-8",
            )
            hits = scan_spd_ids_without_markers(p)
            types_by_id = {(h.get("type"), h.get("id")) for h in hits}
            self.assertIn(("definition", "spd-test-1"), types_by_id)
            self.assertIn(("reference", "spd-test-1"), types_by_id)
            self.assertIn(("reference", "spd-test-2"), types_by_id)
            self.assertIn(("reference", "spd-test-3"), types_by_id)
            self.assertNotIn(("definition", "spd-in-fence"), types_by_id)
            self.assertNotIn(("reference", "spd-in-fence"), types_by_id)

    def test_scan_sdsl_instructions_without_markers_basic_and_parent_binding(self):
        with TemporaryDirectory() as td:
            p = Path(td) / "a.md"
            p.write_text(
                "- [x] `p1` - **ID**: `spd-test-1`\n"
                "\n"
                "1. [x] - `p1` - Step - `inst-a`\n",
                encoding="utf-8",
            )
            hits = scan_sdsl_instructions_without_markers(p)
            self.assertEqual(len(hits), 1)
            self.assertEqual(hits[0].get("parent_id"), "spd-test-1")
            self.assertEqual(hits[0].get("phase"), 1)
            self.assertEqual(hits[0].get("inst"), "a")

    def test_scan_sdsl_instructions_without_markers_skips_marked_files_and_fences_and_bad_phase(self):
        with TemporaryDirectory() as td:
            p_marked = Path(td) / "marked.md"
            p_marked.write_text("<!-- spd:sdsl:x -->\n1. [x] - `p1` - Step - `inst-a`\n<!-- spd:sdsl:x -->\n", encoding="utf-8")
            self.assertEqual(scan_sdsl_instructions_without_markers(p_marked), [])

            p = Path(td) / "a.md"
            p.write_text(
                "- [x] **ID**: `spd-test-1`\n"
                "```\n"
                "1. [x] - `p1` - Step - `inst-in-fence`\n"
                "```\n"
                "1. [x] - `pX` - Step - `inst-bad-phase`\n"
                "1. [x] - `ph-2` - Step - `inst-ok`\n",
                encoding="utf-8",
            )
            hits = scan_sdsl_instructions_without_markers(p)
            self.assertEqual(len(hits), 1)
            self.assertEqual(hits[0].get("phase"), 2)
            self.assertEqual(hits[0].get("inst"), "ok")


class TestMarkerlessContentScopes(unittest.TestCase):
    def test_get_content_scoped_without_markers_none_on_read_error(self):
        with TemporaryDirectory() as td:
            p = Path(td) / "missing.md"
            self.assertIsNone(get_content_scoped_without_markers(p, id_value="spd-x"))

    def test_get_content_scoped_without_markers_hash_fence_segments_and_edge_cases(self):
        with TemporaryDirectory() as td:
            p = Path(td) / "a.md"
            p.write_text(
                "##\n##\n"
                "##\nnot an id\nline\n##\n"
                "##\nspd-aa\nline-a\nspd-bb\nline-b\n##\n",
                encoding="utf-8",
            )
            out = get_content_scoped_without_markers(p, id_value="spd-aa")
            self.assertIsNotNone(out)
            text, _start, _end = out or ("", 0, 0)
            self.assertIn("line-a", text)

            p2 = Path(td) / "b.md"
            p2.write_text("##\nspd-aa\nspd-bb\n##\n", encoding="utf-8")
            self.assertIsNone(get_content_scoped_without_markers(p2, id_value="spd-aa"))

    def test_get_content_scoped_without_markers_heading_scope_and_empty_scope(self):
        with TemporaryDirectory() as td:
            p = Path(td) / "a.md"
            p.write_text(
                "### spd-aa\n"
                "content-a\n"
                "### other\n"
                "x\n",
                encoding="utf-8",
            )
            out = get_content_scoped_without_markers(p, id_value="spd-aa")
            self.assertIsNotNone(out)
            self.assertIn("content-a", (out or ("", 0, 0))[0])

            p2 = Path(td) / "b.md"
            p2.write_text("### spd-aa\n\n### next\n", encoding="utf-8")
            self.assertIsNone(get_content_scoped_without_markers(p2, id_value="spd-aa"))

            p3 = Path(td) / "c.md"
            p3.write_text("### spd-aa\n", encoding="utf-8")
            self.assertIsNone(get_content_scoped_without_markers(p3, id_value="spd-aa"))

    def test_get_content_scoped_without_markers_id_definition_heading_nearest_and_fences(self):
        with TemporaryDirectory() as td:
            p = Path(td) / "a.md"
            p.write_text(
                "#### Title\n"
                "**ID**: `spd-aa`\n"
                "```\n"
                "#### Not a heading (in fence)\n"
                "```\n"
                "line-a\n"
                "**ID**: `spd-bb`\n"
                "line-b\n",
                encoding="utf-8",
            )
            out = get_content_scoped_without_markers(p, id_value="spd-aa")
            self.assertIsNotNone(out)
            self.assertIn("line-a", (out or ("", 0, 0))[0])

            p2 = Path(td) / "b.md"
            p2.write_text("#### Title\n**ID**: `spd-aa`\n", encoding="utf-8")
            self.assertIsNone(get_content_scoped_without_markers(p2, id_value="spd-aa"))

            self.assertIsNone(get_content_scoped_without_markers(p, id_value="spd-x"))


class TestIterTextFilesMoreCoverage(unittest.TestCase):
    def test_iter_text_files_includes_filter_nonmatch(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / "a").mkdir()
            (root / "a" / "x.md").write_text("x\n", encoding="utf-8")
            hits = iter_text_files(root, includes=["**/*.py"])
            self.assertEqual(hits, [])

    def test_iter_text_files_stat_oserror_is_ignored(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / "a").mkdir()
            p = root / "a" / "x.md"
            p.write_text("x\n", encoding="utf-8")

            orig_stat = Path.stat

            def fake_stat(self):
                if self.name == "x.md":
                    raise OSError("boom")
                return orig_stat(self)

            with patch.object(Path, "stat", new=fake_stat):
                hits = iter_text_files(root, includes=["**/*.md"], max_bytes=10)
            self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()