#!/usr/bin/env python3
"""
Script to check if svdep (SystemVerilog dependency manager) is loaded/installed.

This script checks multiple locations:
1. System-wide Python installation
2. IVPM virtual environment (./packages/python/)
3. Attempts to import and display version information

Usage:
    python check_svdep.py
    # Or with the ivpm environment:
    ./packages/python/bin/python check_svdep.py
"""

import sys
import os
import subprocess
from pathlib import Path


def print_header(title):
    """Print a formatted header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print('=' * 70)


def check_import():
    """Try to import svdep directly."""
    print_header("Checking svdep Import")
    try:
        import svdep
        print("✓ svdep is importable")
        
        # Try to get version
        if hasattr(svdep, '__version__'):
            print(f"  Version: {svdep.__version__}")
        else:
            print("  Version: (version attribute not found)")
        
        # Try to get module location
        if hasattr(svdep, '__file__'):
            print(f"  Location: {svdep.__file__}")
        
        # Try to list available functions/classes
        public_attrs = [attr for attr in dir(svdep) if not attr.startswith('_')]
        if public_attrs:
            print(f"  Public API: {', '.join(public_attrs[:10])}")
            if len(public_attrs) > 10:
                print(f"              ... and {len(public_attrs) - 10} more")
        
        return True
    except ImportError as e:
        print(f"✗ svdep is NOT importable")
        print(f"  Error: {e}")
        return False


def check_pip_show(python_path=None):
    """Check if svdep is installed using pip show."""
    if python_path:
        pip_cmd = [str(Path(python_path).parent / 'pip'), 'show', 'svdep']
        env_name = f"IVPM environment ({python_path})"
    else:
        pip_cmd = [sys.executable, '-m', 'pip', 'show', 'svdep']
        env_name = "Current Python environment"
    
    print_header(f"Checking with 'pip show' in {env_name}")
    
    try:
        result = subprocess.run(
            pip_cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✓ svdep is installed")
            print(result.stdout)
            return True
        else:
            print(f"✗ svdep is NOT installed in {env_name}")
            if result.stderr:
                print(f"  Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"✗ Command timed out")
        return False
    except FileNotFoundError:
        print(f"✗ pip not found at expected location")
        return False
    except Exception as e:
        print(f"✗ Error checking pip: {e}")
        return False


def check_pip_list(python_path=None):
    """Check if svdep appears in pip list."""
    if python_path:
        pip_cmd = [str(Path(python_path).parent / 'pip'), 'list']
        env_name = "IVPM environment"
    else:
        pip_cmd = [sys.executable, '-m', 'pip', 'list']
        env_name = "Current environment"
    
    print_header(f"Checking 'pip list' in {env_name}")
    
    try:
        result = subprocess.run(
            pip_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Search for svdep in the output
            lines = result.stdout.lower().split('\n')
            svdep_lines = [line for line in lines if 'svdep' in line]
            
            if svdep_lines:
                print("✓ svdep found in package list:")
                for line in svdep_lines:
                    print(f"  {line}")
                return True
            else:
                print(f"✗ svdep NOT found in package list")
                return False
        else:
            print(f"✗ Failed to get package list")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def check_ivpm_packages():
    """Check the IVPM packages directory."""
    print_header("Checking IVPM Packages Directory")
    
    packages_dir = Path('packages/python')
    
    if not packages_dir.exists():
        print(f"✗ IVPM packages directory not found: {packages_dir}")
        print("  Run 'ivpm update' to create the environment")
        return False
    
    print(f"✓ IVPM packages directory exists: {packages_dir.absolute()}")
    
    # Check for Python executable
    python_exe = packages_dir / 'bin' / 'python'
    if not python_exe.exists():
        python_exe = packages_dir / 'Scripts' / 'python.exe'  # Windows
    
    if python_exe.exists():
        print(f"✓ Python executable found: {python_exe}")
        return python_exe
    else:
        print(f"✗ Python executable not found in {packages_dir}")
        return None


def get_installation_instructions():
    """Return instructions for installing svdep."""
    return """
To install svdep:

1. In your system Python:
   pip install svdep

2. In the IVPM virtual environment:
   ./packages/python/bin/pip install svdep
   
   Or on Windows:
   .\\packages\\python\\Scripts\\pip install svdep

3. Verify installation:
   python check_svdep.py
"""


def main():
    """Main function to run all checks."""
    print_header("svdep Installation Checker")
    print("Checking if svdep (SystemVerilog dependency manager) is installed...")
    
    found_anywhere = False
    
    # Check 1: Try direct import
    if check_import():
        found_anywhere = True
    
    # Check 2: Check current environment with pip
    if check_pip_show():
        found_anywhere = True
    
    # Check 3: Check IVPM environment
    ivpm_python = check_ivpm_packages()
    if ivpm_python:
        if check_pip_show(str(ivpm_python)):
            found_anywhere = True
        check_pip_list(str(ivpm_python))
    
    # Check 4: List in current environment
    check_pip_list()
    
    # Summary
    print_header("Summary")
    if found_anywhere:
        print("✓ svdep IS installed in at least one location")
        print("\nsvdep is a SystemVerilog dependency management tool.")
        print("It can be used to track dependencies of SV files generated by zuspec.")
    else:
        print("✗ svdep is NOT installed")
        print("\nsvdep is an optional dependency for SystemVerilog dependency tracking.")
        print("It is not required for the zuspec-example-dma project to function,")
        print("but can be useful if you're managing SystemVerilog file dependencies.")
        print(get_installation_instructions())
    
    return 0 if found_anywhere else 1


if __name__ == '__main__':
    sys.exit(main())
