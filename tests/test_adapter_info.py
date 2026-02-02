"""
Test adapter-info command.

Tests adapter discovery, config loading, and error handling.
"""
import unittest
import json
import tempfile
import shutil
import io
import sys
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr

# Add spider.py to path
sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "spider" / "scripts"))

from spider.cli import main
from spider.utils.files import (
    find_project_root,
    load_project_config,
    find_adapter_directory,
    load_adapter_config,
)


class TestAdapterInfoCommand(unittest.TestCase):
    """Test suite for adapter-info CLI command."""
    
    def test_adapter_info_found_with_config(self):
        """Test adapter-info when adapter exists and is configured."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Setup: Create project structure with config
            project_root = Path(tmp_dir) / "project"
            project_root.mkdir()
            
            adapter_dir = project_root / ".spider-adapter"
            adapter_dir.mkdir()
            specs_dir = adapter_dir / "specs"
            specs_dir.mkdir()
            
            # Create .spider-config.json
            config_file = project_root / ".spider-config.json"
            config_file.write_text(json.dumps({
                "spiderAdapterPath": ".spider-adapter"
            }))
            
            # Create AGENTS.md
            agents_file = adapter_dir / "AGENTS.md"
            agents_file.write_text("""# Spider Adapter: TestProject

**Extends**: `../Spider/AGENTS.md`

**Version**: 1.0
""")
            
            # Create some spec files
            (specs_dir / "tech-stack.md").write_text("# Tech Stack\n")
            (specs_dir / "domain-model.md").write_text("# Domain Model\n")

            # Create artifacts.json in adapter
            (adapter_dir / "artifacts.json").write_text(
                json.dumps({"version": "1.0", "artifacts": [{"kind": "PRD", "path": "architecture/PRD.md"}]}, indent=2) + "\n",
                encoding="utf-8",
            )
            
            # Run command
            stdout_capture = io.StringIO()
            with redirect_stdout(stdout_capture):
                exit_code = main(["adapter-info", "--root", str(project_root)])
            
            # Verify output
            output = json.loads(stdout_capture.getvalue())
            
            self.assertEqual(exit_code, 0)
            self.assertEqual(output["status"], "FOUND")
            self.assertEqual(output["project_name"], "TestProject")
            self.assertIn("domain-model", output["specs"])
            self.assertIn("tech-stack", output["specs"])
            self.assertTrue(output["has_config"])
            self.assertIn(".spider-adapter", output["adapter_dir"])
            self.assertIn("artifacts_registry_path", output)
            self.assertIn("artifacts_registry", output)
            self.assertIsNone(output.get("artifacts_registry_error"))
            self.assertEqual(output["artifacts_registry"]["version"], "1.0")
    
    def test_adapter_info_found_without_config(self):
        """Test adapter-info finds adapter via recursive search when no config."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Setup: Create project structure WITHOUT config
            project_root = Path(tmp_dir) / "project"
            project_root.mkdir()
            
            # Add .git to mark as project root
            (project_root / ".git").mkdir()
            
            adapter_dir = project_root / ".spider-adapter"
            adapter_dir.mkdir()
            
            # Create AGENTS.md with Extends
            agents_file = adapter_dir / "AGENTS.md"
            agents_file.write_text("""# Spider Adapter: MyProject

**Extends**: `../../Spider/AGENTS.md`
""")
            
            # Run command
            stdout_capture = io.StringIO()
            with redirect_stdout(stdout_capture):
                exit_code = main(["adapter-info", "--root", str(project_root)])
            
            # Verify output
            output = json.loads(stdout_capture.getvalue())
            
            self.assertEqual(exit_code, 0)
            self.assertEqual(output["status"], "FOUND")
            self.assertEqual(output["project_name"], "MyProject")
            self.assertFalse(output["has_config"])
            self.assertIn("config_hint", output)
            self.assertIn("artifacts_registry_path", output)
            self.assertIn("artifacts_registry", output)
    
    def test_adapter_info_not_found(self):
        """Test adapter-info when no adapter exists."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Setup: Create project without adapter
            project_root = Path(tmp_dir) / "project"
            project_root.mkdir()
            (project_root / ".git").mkdir()
            
            # Run command
            stdout_capture = io.StringIO()
            with redirect_stdout(stdout_capture):
                exit_code = main(["adapter-info", "--root", str(project_root)])
            
            # Verify output
            output = json.loads(stdout_capture.getvalue())
            
            self.assertEqual(exit_code, 1)
            self.assertEqual(output["status"], "NOT_FOUND")
            self.assertIn("hint", output)
            self.assertIn("adapter-bootstrap", output["hint"])
    
    def test_adapter_info_config_error(self):
        """Test adapter-info when config exists but path is invalid."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Setup: Create project with invalid config
            project_root = Path(tmp_dir) / "project"
            project_root.mkdir()
            
            # Create config pointing to non-existent adapter
            config_file = project_root / ".spider-config.json"
            config_file.write_text(json.dumps({
                "spiderAdapterPath": "invalid-path"
            }))
            
            # Run command
            stdout_capture = io.StringIO()
            with redirect_stdout(stdout_capture):
                exit_code = main(["adapter-info", "--root", str(project_root)])
            
            # Verify output
            output = json.loads(stdout_capture.getvalue())
            
            self.assertEqual(exit_code, 1)
            self.assertEqual(output["status"], "CONFIG_ERROR")
            self.assertIn("config_path", output)
            self.assertEqual(output["config_path"], "invalid-path")
    
    def test_adapter_info_no_project_root(self):
        """Test adapter-info when not in a project (no .git or config)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Setup: Create empty directory (not a project)
            empty_dir = Path(tmp_dir) / "not-a-project"
            empty_dir.mkdir()
            
            # Run command
            stdout_capture = io.StringIO()
            with redirect_stdout(stdout_capture):
                exit_code = main(["adapter-info", "--root", str(empty_dir)])
            
            # Verify output
            output = json.loads(stdout_capture.getvalue())
            
            self.assertEqual(exit_code, 1)
            self.assertEqual(output["status"], "NOT_FOUND")
            self.assertIn("No project root found", output["message"])
    
    def test_adapter_info_with_spider_root_exclusion(self):
        """Test adapter-info excludes Spider core directory when spider-root provided."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Setup: Create nested structure with both Spider and adapter
            project_root = Path(tmp_dir) / "project"
            project_root.mkdir()
            (project_root / ".git").mkdir()
            
            # Create Spider core directory (should be excluded)
            spider_core = project_root / "Spider"
            spider_core.mkdir()
            (spider_core / "AGENTS.md").write_text("# Spider Core\n")
            (spider_core / "requirements").mkdir()
            (spider_core / "workflows").mkdir()
            
            # Create real adapter
            adapter_dir = project_root / ".spider-adapter"
            adapter_dir.mkdir()
            agents_file = adapter_dir / "AGENTS.md"
            agents_file.write_text("""# Spider Adapter: RealProject

**Extends**: `../Spider/AGENTS.md`
""")
            
            # Run command with spider-root
            stdout_capture = io.StringIO()
            with redirect_stdout(stdout_capture):
                exit_code = main([
                    "adapter-info",
                    "--root", str(project_root),
                    "--spider-root", str(spider_core)
                ])
            
            # Verify it found the adapter, not Spider core
            output = json.loads(stdout_capture.getvalue())
            
            self.assertEqual(exit_code, 0)
            self.assertEqual(output["status"], "FOUND")
            self.assertEqual(output["project_name"], "RealProject")
            self.assertIn(".spider-adapter", output["adapter_dir"])
            self.assertNotIn("Spider", output["adapter_dir"])


class TestAdapterHelperFunctions(unittest.TestCase):
    """Test suite for adapter discovery helper functions."""
    
    def test_find_project_root_with_config(self):
        """Test find_project_root locates .spider-config.json."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "project"
            project_root.mkdir()
            (project_root / ".spider-config.json").write_text("{}")
            
            subdir = project_root / "src" / "lib"
            subdir.mkdir(parents=True)
            
            found = find_project_root(subdir)
            self.assertEqual(found.resolve() if found else None, project_root.resolve())
    
    def test_find_project_root_with_git(self):
        """Test find_project_root locates .git directory."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "project"
            project_root.mkdir()
            (project_root / ".git").mkdir()
            
            subdir = project_root / "src"
            subdir.mkdir()
            
            found = find_project_root(subdir)
            self.assertEqual(found.resolve() if found else None, project_root.resolve())
    
    def test_find_project_root_not_found(self):
        """Test find_project_root returns None when no markers found."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            empty_dir = Path(tmp_dir) / "empty"
            empty_dir.mkdir()
            
            found = find_project_root(empty_dir)
            self.assertIsNone(found)
    
    def test_load_project_config_valid(self):
        """Test load_project_config with valid JSON."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "project"
            project_root.mkdir()
            
            config_file = project_root / ".spider-config.json"
            config_file.write_text(json.dumps({
                "spiderAdapterPath": ".spider-adapter",
                "other": "value"
            }))
            
            config = load_project_config(project_root)
            self.assertIsNotNone(config)
            self.assertEqual(config["spiderAdapterPath"], ".spider-adapter")
            self.assertEqual(config["other"], "value")
    
    def test_load_project_config_missing(self):
        """Test load_project_config returns None when file missing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "project"
            project_root.mkdir()
            
            config = load_project_config(project_root)
            self.assertIsNone(config)
    
    def test_load_project_config_invalid_json(self):
        """Test load_project_config handles invalid JSON."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "project"
            project_root.mkdir()
            
            config_file = project_root / ".spider-config.json"
            config_file.write_text("{ invalid json }")
            
            config = load_project_config(project_root)
            self.assertIsNone(config)
    
    def test_find_adapter_directory_with_config(self):
        """Test find_adapter_directory uses config path first."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "project"
            project_root.mkdir()
            
            # Create config
            config_file = project_root / ".spider-config.json"
            config_file.write_text(json.dumps({"spiderAdapterPath": "custom-adapter"}))
            
            # Create adapter at configured path
            adapter_dir = project_root / "custom-adapter"
            adapter_dir.mkdir()
            agents_file = adapter_dir / "AGENTS.md"
            agents_file.write_text("**Extends**: Spider")
            
            found = find_adapter_directory(project_root)
            self.assertEqual(found.resolve() if found else None, adapter_dir.resolve())
    
    def test_find_adapter_directory_recursive_search(self):
        """Test find_adapter_directory uses recursive search without config."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "project"
            project_root.mkdir()
            (project_root / ".git").mkdir()
            
            # Create adapter in nested location
            adapter_dir = project_root / "docs" / ".spider-adapter"
            adapter_dir.mkdir(parents=True)
            (adapter_dir / "specs").mkdir()
            agents_file = adapter_dir / "AGENTS.md"
            agents_file.write_text("""# Spider Adapter: Test

**Extends**: `../../Spider/AGENTS.md`
""")
            
            found = find_adapter_directory(project_root)
            self.assertEqual(found.resolve() if found else None, adapter_dir.resolve())
    
    def test_load_adapter_config_complete(self):
        """Test load_adapter_config extracts all metadata."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            adapter_dir = Path(tmp_dir) / "adapter"
            adapter_dir.mkdir()
            
            # Create AGENTS.md
            agents_file = adapter_dir / "AGENTS.md"
            agents_file.write_text("""# Spider Adapter: MyProject

**Extends**: `../Spider/AGENTS.md`
**Version**: 2.0
""")
            
            # Create specs
            specs_dir = adapter_dir / "specs"
            specs_dir.mkdir()
            (specs_dir / "tech-stack.md").write_text("# Tech Stack")
            (specs_dir / "api-contracts.md").write_text("# API Contracts")
            
            config = load_adapter_config(adapter_dir)
            
            self.assertEqual(config["project_name"], "MyProject")
            self.assertIn("tech-stack", config["specs"])
            self.assertIn("api-contracts", config["specs"])
            self.assertEqual(len(config["specs"]), 2)


if __name__ == "__main__":
    unittest.main()
