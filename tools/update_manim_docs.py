#!/usr/bin/env python3
"""Update Manim documentation by building Sphinx docs and organizing them into reference sections."""
import os
import sys
import subprocess
import re
import shutil
from pathlib import Path


def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the result."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Command failed: {cmd}", file=sys.stderr)
        print(f"stdout: {result.stdout}", file=sys.stderr)
        print(f"stderr: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result


def find_python():
    """Find a suitable Python binary."""
    for python_bin in ["python3.12", "python3"]:
        result = run_command(f"which {python_bin}", check=False)
        if result.returncode == 0:
            return python_bin
    return "python3"


def main():
    # Setup paths
    root_dir = Path(__file__).parent.parent
    repo_dir = Path(os.getenv("REPO_DIR", root_dir / ".manim-docs"))
    out_dir = Path(os.getenv("OUT_DIR", root_dir / "manim-skill" / "references" / "manim-docs"))
    venv_dir = Path(os.getenv("VENV_DIR", repo_dir / ".venv-docs"))
    python_bin = os.getenv("PYTHON_BIN", find_python())

    build_dir = repo_dir / "docs" / "_build" / "markdown"

    # Git operations
    if (repo_dir / ".git").exists():
        print("Updating manim repo...")
        run_command(f"git fetch --all --prune", cwd=repo_dir)
        run_command(f"git pull --ff-only", cwd=repo_dir)
    else:
        print("Cloning manim repo...")
        run_command(f"git clone https://github.com/ManimCommunity/manim.git {repo_dir}")

    # Check for venv
    sphinx_build = venv_dir / "bin" / "sphinx-build"
    if not sphinx_build.exists():
        print(f"Error: venv or sphinx-build missing. Install docs deps manually first.", file=sys.stderr)
        print(f"Hint: create venv at {venv_dir} and install docs requirements + manim.", file=sys.stderr)
        sys.exit(1)

    # Build docs with sphinx
    print("Building markdown docs with Sphinx...")
    log_file = repo_dir / "docs" / "_build" / "markdown-build.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    cmd = f"{sphinx_build} -q -b markdown -t skip-manim -c {repo_dir}/docs/source {repo_dir}/docs/source {build_dir}"
    result = run_command(cmd, check=False)

    with open(log_file, "w") as f:
        f.write(result.stdout)
        f.write(result.stderr)

    if result.returncode != 0:
        print("Sphinx build failed. Last 50 lines:", file=sys.stderr)
        with open(log_file) as f:
            lines = f.readlines()
            for line in lines[-50:]:
                print(line, end="", file=sys.stderr)
        sys.exit(1)

    # Check for warnings
    with open(log_file) as f:
        content = f.read()
        if "WARNING" in content or "ERROR" in content:
            print("Sphinx warnings/errors (last 50 lines):", file=sys.stderr)
            for line in content.split("\n"):
                if "WARNING" in line or "ERROR" in line:
                    print(line, file=sys.stderr)

    # Clean and create output directory
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Copy individual markdown files
    files_to_copy = [
        # "tutorials/index.md",
        "tutorials/quickstart.md",
        "tutorials/building_blocks.md",
        "tutorials/output_and_config.md",
        # "guides/index.md",
        "guides/using_text.md",
        "guides/configuration.md",
        "guides/deep_dive.md",
        "examples.md",
        "tutorials_guides.md",
        "faq/general.md",
        "faq/help.md",
        "faq/installation.md",
        "faq/opengl.md",
    ]

    for rel_path in files_to_copy:
        src = build_dir / rel_path
        dst = out_dir / rel_path
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        else:
            print(f"Warning: missing {rel_path}", file=sys.stderr)

    # Copy reference directory
    ref_src = build_dir / "reference"
    ref_dst = out_dir / "reference"
    if ref_src.exists():
        if ref_dst.exists():
            shutil.rmtree(ref_dst)
        shutil.copytree(ref_src, ref_dst)

    # Generate reference sections
    if ref_dst.exists():
        sections_dir = out_dir / "reference_sections"
        sections_dir.mkdir(parents=True, exist_ok=True)

        for section in ["animations", "cameras", "configuration", "mobjects", "scenes", "utilities_misc"]:
            section_rst = repo_dir / "docs" / "source" / "reference_index" / f"{section}.rst"

            if not section_rst.exists():
                print(f"Warning: missing {section_rst}", file=sys.stderr)
                continue

            # Read the .rst file and extract module names
            with open(section_rst) as f:
                content = f.read()

            # Find all lines with module references like "~manim.scene.scene_file_writer"
            modules = re.findall(r'^\s*~([a-zA-Z0-9_.]+)', content, re.MULTILINE)

            # Group modules by their first two levels (e.g., scene.scene_file_writer)
            grouped = {}
            for mod in modules:
                ref_file = ref_dst / f"manim.{mod}.md"
                if ref_file.exists():
                    # Extract first two parts after "manim."
                    # e.g., "scene.scene_file_writer" -> "scene.scene_file_writer"
                    parts = mod.split(".")
                    if len(parts) >= 2:
                        # Use first two parts as the grouping key
                        group_key = ".".join(parts[:2])
                        if group_key not in grouped:
                            grouped[group_key] = []
                        grouped[group_key].append((mod, ref_file))

            # Create one file per group
            for group_key in sorted(grouped.keys()):
                section_out = sections_dir / f"{group_key}.md"
                section_content = []

                for mod, ref_file in grouped[group_key]:
                    section_content.append(f"## {mod}\n")
                    with open(ref_file) as f:
                        section_content.append(f.read())
                    section_content.append("\n")

                # Write the group file
                with open(section_out, "w") as f:
                    f.write("".join(section_content))

        # Remove the reference directory
        shutil.rmtree(ref_dst)

    print(f"Updated references in {out_dir}")


if __name__ == "__main__":
    main()
