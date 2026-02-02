"""
Test language configuration loading and dynamic regex building.

Validates that language_config module correctly:
- Loads configuration from .spider-config.json
- Falls back to defaults when config missing
- Builds correct regex patterns for different comment styles
- Detects effective code lines vs comments
"""

import unittest
import sys
import json
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "spider" / "scripts"))

from spider.utils import (
    load_language_config,
    build_spider_begin_regex,
    build_spider_end_regex,
    build_no_spider_begin_regex,
    build_no_spider_end_regex,
    LanguageConfig,
    DEFAULT_FILE_EXTENSIONS,
)


class TestLanguageConfigLoading(unittest.TestCase):
    """Test language configuration loading from .spider-config.json."""

    def test_default_config_when_no_project_config(self):
        """Verify default config is used when no .spider-config.json exists."""
        with TemporaryDirectory() as tmpdir:
            config = load_language_config(Path(tmpdir))
            
            # Should have default extensions
            self.assertEqual(config.file_extensions, DEFAULT_FILE_EXTENSIONS)
            self.assertIn(".py", config.file_extensions)
            self.assertIn(".js", config.file_extensions)
            self.assertIn(".rs", config.file_extensions)
            
            # Should have default comment styles
            self.assertIn("#", config.single_line_comments)
            self.assertIn("//", config.single_line_comments)
            self.assertIn("--", config.single_line_comments)

    def test_custom_config_overrides_defaults(self):
        """Verify custom config from .spider-config.json overrides defaults."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Write custom config
            config_file = tmppath / ".spider-config.json"
            config_file.write_text(json.dumps({
                "spiderAdapterPath": "adapter",
                "codeScanning": {
                    "fileExtensions": [".php", ".rb"],
                    "singleLineComments": ["#", "//"],
                    "multiLineComments": [
                        {"start": "/*", "end": "*/"}
                    ],
                    "blockCommentPrefixes": ["*"]
                }
            }))
            
            config = load_language_config(tmppath)
            
            # Should use custom extensions
            self.assertEqual(config.file_extensions, {".php", ".rb"})
            self.assertNotIn(".py", config.file_extensions)
            
            # Should use custom comments
            self.assertEqual(config.single_line_comments, ["#", "//"])

    def test_partial_config_falls_back_to_defaults(self):
        """Verify partial config uses defaults for missing fields."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Write config with only fileExtensions
            config_file = tmppath / ".spider-config.json"
            config_file.write_text(json.dumps({
                "spiderAdapterPath": "adapter",
                "codeScanning": {
                    "fileExtensions": [".kt", ".swift"]
                }
            }))
            
            config = load_language_config(tmppath)
            
            # Should use custom extensions
            self.assertEqual(config.file_extensions, {".kt", ".swift"})
            
            # Should fall back to defaults for comments
            self.assertIn("#", config.single_line_comments)
            self.assertIn("//", config.single_line_comments)


class TestRegexPatternBuilding(unittest.TestCase):
    """Test dynamic regex pattern building from language config."""

    def test_spider_begin_regex_matches_python_style(self):
        """Verify spider-begin regex matches Python # comments."""
        config = LanguageConfig(
            file_extensions={".py"},
            single_line_comments=["#"],
            multi_line_comments=[],
            block_comment_prefixes=[]
        )
        
        regex = build_spider_begin_regex(config)
        
        # Should match Python comment
        self.assertIsNotNone(regex.match("# spider-begin spd-test-feature-x-flow-y:ph-1:inst-step"))
        self.assertIsNotNone(regex.match("  # spider-begin spd-test-feature-x-flow-y:ph-1:inst-step"))
        
        # Should extract tag
        match = regex.match("# spider-begin spd-test-feature-x-flow-y:ph-1:inst-step")
        self.assertEqual(match.group(1), "spd-test-feature-x-flow-y:ph-1:inst-step")

    def test_spider_begin_regex_matches_javascript_style(self):
        """Verify spider-begin regex matches JavaScript // comments."""
        config = LanguageConfig(
            file_extensions={".js"},
            single_line_comments=["//"],
            multi_line_comments=[],
            block_comment_prefixes=[]
        )
        
        regex = build_spider_begin_regex(config)
        
        # Should match JS comment
        self.assertIsNotNone(regex.match("// spider-begin spd-test-feature-x-flow-y:ph-1:inst-step"))
        self.assertIsNotNone(regex.match("  // spider-begin spd-test-feature-x-flow-y:ph-1:inst-step"))

    def test_spider_begin_regex_matches_sql_style(self):
        """Verify spider-begin regex matches SQL -- comments."""
        config = LanguageConfig(
            file_extensions={".sql"},
            single_line_comments=["--"],
            multi_line_comments=[],
            block_comment_prefixes=[]
        )
        
        regex = build_spider_begin_regex(config)
        
        # Should match SQL comment
        self.assertIsNotNone(regex.match("-- spider-begin spd-test-feature-x-flow-y:ph-1:inst-step"))

    def test_spider_begin_regex_matches_html_comment(self):
        """Verify spider-begin regex matches HTML <!-- comments."""
        config = LanguageConfig(
            file_extensions={".html"},
            single_line_comments=[],
            multi_line_comments=[{"start": "<!--", "end": "-->"}],
            block_comment_prefixes=[]
        )
        
        regex = build_spider_begin_regex(config)
        
        # Should match HTML comment
        self.assertIsNotNone(regex.match("<!-- spider-begin spd-test-feature-x-flow-y:ph-1:inst-step"))

    def test_spider_begin_regex_matches_multiple_styles(self):
        """Verify spider-begin regex matches multiple comment styles."""
        config = LanguageConfig(
            file_extensions={".py", ".js", ".sql"},
            single_line_comments=["#", "//", "--"],
            multi_line_comments=[{"start": "/*", "end": "*/"}],
            block_comment_prefixes=["*"]
        )
        
        regex = build_spider_begin_regex(config)
        
        # Should match all styles
        self.assertIsNotNone(regex.match("# spider-begin spd-test-feature-x-flow-y:ph-1:inst-step"))
        self.assertIsNotNone(regex.match("// spider-begin spd-test-feature-x-flow-y:ph-1:inst-step"))
        self.assertIsNotNone(regex.match("-- spider-begin spd-test-feature-x-flow-y:ph-1:inst-step"))
        self.assertIsNotNone(regex.match("/* spider-begin spd-test-feature-x-flow-y:ph-1:inst-step"))
        self.assertIsNotNone(regex.match("* spider-begin spd-test-feature-x-flow-y:ph-1:inst-step"))

    def test_spider_end_regex_matches_same_styles_as_begin(self):
        """Verify spider-end regex matches same styles as spider-begin."""
        config = LanguageConfig(
            file_extensions={".py", ".js"},
            single_line_comments=["#", "//"],
            multi_line_comments=[],
            block_comment_prefixes=[]
        )
        
        end_regex = build_spider_end_regex(config)
        
        # Should match both styles
        self.assertIsNotNone(end_regex.match("# spider-end spd-test-feature-x-flow-y:ph-1:inst-step"))
        self.assertIsNotNone(end_regex.match("// spider-end spd-test-feature-x-flow-y:ph-1:inst-step"))

    def test_no_spider_begin_regex_matches_exclusion_marker(self):
        """Verify !no-spider-begin regex matches exclusion markers."""
        config = LanguageConfig(
            file_extensions={".py"},
            single_line_comments=["#"],
            multi_line_comments=[{"start": "<!--", "end": "-->"}],
            block_comment_prefixes=[]
        )
        
        regex = build_no_spider_begin_regex(config)
        
        # Should match exclusion markers
        self.assertIsNotNone(regex.match("# !no-spider-begin"))
        self.assertIsNotNone(regex.match("# Some text !no-spider-begin"))
        self.assertIsNotNone(regex.match("<!-- !no-spider-begin -->"))

    def test_no_spider_end_regex_matches_exclusion_marker(self):
        """Verify !no-spider-end regex matches exclusion end markers."""
        config = LanguageConfig(
            file_extensions={".py"},
            single_line_comments=["#"],
            multi_line_comments=[{"start": "<!--", "end": "-->"}],
            block_comment_prefixes=[]
        )
        
        regex = build_no_spider_end_regex(config)
        
        # Should match exclusion end markers
        self.assertIsNotNone(regex.match("# !no-spider-end"))
        self.assertIsNotNone(regex.match("<!-- !no-spider-end -->"))


class TestEffectiveCodeLineDetection(unittest.TestCase):
    """Test detection of effective code lines vs comments."""

    def test_empty_line_is_not_effective_code(self):
        """Verify empty lines are not considered effective code."""
        config = LanguageConfig(
            file_extensions={".py"},
            single_line_comments=["#"],
            multi_line_comments=[],
            block_comment_prefixes=[]
        )
        
        self.assertFalse(config.is_effective_code_line(""))
        self.assertFalse(config.is_effective_code_line("   "))
        self.assertFalse(config.is_effective_code_line("\t\t"))

    def test_python_comment_is_not_effective_code(self):
        """Verify Python comments are not considered effective code."""
        config = LanguageConfig(
            file_extensions={".py"},
            single_line_comments=["#"],
            multi_line_comments=[],
            block_comment_prefixes=[]
        )
        
        self.assertFalse(config.is_effective_code_line("# This is a comment"))
        self.assertFalse(config.is_effective_code_line("  # Indented comment"))

    def test_javascript_comment_is_not_effective_code(self):
        """Verify JavaScript comments are not considered effective code."""
        config = LanguageConfig(
            file_extensions={".js"},
            single_line_comments=["//"],
            multi_line_comments=[{"start": "/*", "end": "*/"}],
            block_comment_prefixes=[]
        )
        
        self.assertFalse(config.is_effective_code_line("// This is a comment"))
        self.assertFalse(config.is_effective_code_line("/* Start of block comment"))
        self.assertFalse(config.is_effective_code_line("*/  End of block comment"))

    def test_actual_code_is_effective_code(self):
        """Verify actual code lines are considered effective code."""
        config = LanguageConfig(
            file_extensions={".py"},
            single_line_comments=["#"],
            multi_line_comments=[],
            block_comment_prefixes=[]
        )
        
        self.assertTrue(config.is_effective_code_line("x = 5"))
        self.assertTrue(config.is_effective_code_line("def my_function():"))
        self.assertTrue(config.is_effective_code_line("    return True"))

    def test_markdown_bold_is_effective_code(self):
        """Verify markdown bold (**) is not treated as block comment prefix."""
        config = LanguageConfig(
            file_extensions={".md"},
            single_line_comments=["#"],
            multi_line_comments=[{"start": "<!--", "end": "-->"}],
            block_comment_prefixes=["*"]
        )
        
        # ** should be treated as effective content (markdown bold)
        self.assertTrue(config.is_effective_code_line("**Bold text**"))
        
        # Single * at start should be treated as comment prefix
        self.assertFalse(config.is_effective_code_line("* Block comment line"))

    def test_sql_comment_is_not_effective_code(self):
        """Verify SQL -- comments are not considered effective code."""
        config = LanguageConfig(
            file_extensions={".sql"},
            single_line_comments=["--"],
            multi_line_comments=[],
            block_comment_prefixes=[]
        )
        
        self.assertFalse(config.is_effective_code_line("-- SQL comment"))
        self.assertTrue(config.is_effective_code_line("SELECT * FROM users;"))


class TestCommentPatternBuilding(unittest.TestCase):
    """Test comment pattern building for regex."""

    def test_build_comment_pattern_escapes_special_chars(self):
        """Verify special regex characters are properly escaped."""
        config = LanguageConfig(
            file_extensions={".py"},
            single_line_comments=["#", "//"],
            multi_line_comments=[{"start": "/*", "end": "*/"}],
            block_comment_prefixes=["*"]
        )
        
        pattern = config.build_comment_pattern()
        
        # Should contain escaped versions
        self.assertIn(r"\#", pattern)
        self.assertIn(r"//", pattern)
        self.assertIn(r"/\*", pattern)
        self.assertIn(r"\*", pattern)
        
        # Should be wrapped in non-capturing group
        self.assertTrue(pattern.startswith("(?:"))
        self.assertTrue(pattern.endswith(")"))

    def test_build_comment_pattern_includes_all_prefixes(self):
        """Verify all comment prefixes are included in pattern."""
        config = LanguageConfig(
            file_extensions={".py"},
            single_line_comments=["#", "//", "--"],
            multi_line_comments=[{"start": "<!--", "end": "-->"}],
            block_comment_prefixes=["*"]
        )
        
        pattern = config.build_comment_pattern()
        
        # Should include all single-line styles (some escaped)
        self.assertIn("#", pattern)
        self.assertIn("//", pattern)
        self.assertIn("\\-\\-", pattern)  # -- gets escaped to \-\-
        
        # Should include multi-line start markers (escaped)
        self.assertIn("<!\\-\\-", pattern)  # <!-- gets escaped
        
        # Should include block prefixes
        self.assertIn("*", pattern)


if __name__ == "__main__":
    unittest.main()
