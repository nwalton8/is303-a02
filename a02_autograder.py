"""
IS 303 Autograder - A02: Decisions

This autograder checks student Python files against a rubric JSON file.
Students can run this locally before submitting to verify their work meets
the basic requirements.

Usage:
    python a02_autograder.py

    By default, the autograder looks for .py files in the current directory
    and uses a02_rubric.json for grading instructions. You can also pass
    a folder path as an argument to grade a specific folder.

    python a02_autograder.py /path/to/student/folder

Checks performed:
    1. File identification: matches file names to known problem contexts
    2. Content checks: verifies the I/P/O comment block exists
    3. Branch tests: runs the program with different inputs and verifies
       that different inputs produce different outputs (conditional logic)
    4. Validation tests: sends invalid input and checks for error messages
    5. Branch diversity: warns if all branch tests produce identical output
"""

import json
import os
import re
import subprocess
import sys


def load_rubric(rubric_path):
    """Load and return the rubric from a JSON file."""
    with open(rubric_path, "r", encoding="utf-8") as f:
        return json.load(f)


def identify_problem(file_name, rubric):
    """
    Match a file name to a problem context using the rubric's naming dictionary.
    Returns the problem name if matched, or None if no match is found.
    """
    file_lower = file_name.lower()
    for problem_name, possible_names in rubric["problem_naming"].items():
        for name in possible_names:
            if name.lower() == file_lower:
                return problem_name
    return None


def check_file_contents(file_path, problem_rubric):
    """
    Check the file contents against the rubric's content checks.
    Returns a tuple of (points_earned, list_of_notes).
    """
    points = 0
    notes = []

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    for check in problem_rubric["content_checks"]:
        field = check["field"]
        regexes = check["regexes"]
        check_points = check["points"]
        found = False

        for regex in regexes:
            if re.search(regex, content, re.IGNORECASE | re.DOTALL):
                found = True
                break

        if found:
            points += check_points
        else:
            notes.append(f"  MISSING: {field}")

    return points, notes


def run_single_test(file_path, sim_input, timeout=15):
    """
    Run a student file with the given simulated input.
    Returns (exit_code, stdout, stderr) or raises on timeout.
    """
    result = subprocess.run(
        [sys.executable, os.path.abspath(file_path)],
        input=sim_input,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def run_test_cases(file_path, problem_rubric, timeout=15):
    """
    Run all test cases (branch tests and validation tests) for a problem.
    Returns (points_earned, list_of_notes).

    Branch tests check that the program runs and produces output.
    Validation tests check that invalid input produces an error message.
    After all branch tests, checks that at least two produced different
    output (confirming conditional logic is working).
    """
    points = 0
    notes = []
    test_cases = problem_rubric["test_cases"]
    branch_outputs = []

    for tc in test_cases:
        label = tc["label"]
        sim_input = tc["inputs"]
        expected = tc["expected_output"]
        tc_points = tc["points"]
        tc_type = tc.get("type", "branch")

        try:
            exit_code, stdout, stderr = run_single_test(
                file_path, sim_input, timeout
            )

            # Handle program crashes
            if exit_code != 0:
                # For validation tests, a crash with output may still count
                # (some students use sys.exit() after printing an error)
                if tc_type == "validation" and stdout:
                    output = stdout
                else:
                    notes.append(f"  ERROR [{label}]: Program crashed")
                    if stderr:
                        error_lines = stderr.strip().split("\n")
                        last_line = error_lines[-1]
                        if "EOFError" in last_line:
                            notes.append(
                                f"    Program asked for more input than expected."
                            )
                            notes.append(
                                f"    Check that your input() calls match "
                                f"the context description."
                            )
                        else:
                            notes.append(f"    {last_line}")
                    continue
            else:
                output = stdout

            # Check output against expected pattern
            if re.search(expected, output, re.DOTALL | re.IGNORECASE):
                points += tc_points
                if tc_type == "branch":
                    branch_outputs.append(output.strip())
            else:
                if tc_type == "validation":
                    notes.append(f"  VALIDATION [{label}]:")
                    notes.append(
                        f"    Expected an error message (e.g., 'Error: ...' "
                        f"or 'Invalid ...')"
                    )
                    notes.append(
                        f"    Got: {output.strip()[:200]}"
                    )
                    notes.append(
                        f"    Note: If your program validates a different "
                        f"input than what was tested,"
                    )
                    notes.append(
                        f"    this may be a false negative. Your instructor "
                        f"will check manually."
                    )
                else:
                    notes.append(f"  OUTPUT MISMATCH [{label}]:")
                    notes.append(f"    Expected pattern: {expected}")
                    notes.append(f"    Got: {output.strip()[:200]}")

                if tc_type == "branch":
                    branch_outputs.append(output.strip())

        except subprocess.TimeoutExpired:
            notes.append(
                f"  TIMEOUT [{label}]: Program took more than {timeout} "
                f"seconds. Check for infinite loops."
            )
        except Exception as e:
            notes.append(f"  ERROR [{label}]: {str(e)}")

    # Branch diversity check: different inputs should produce different outputs
    if len(branch_outputs) >= 2:
        unique_outputs = set(branch_outputs)
        if len(unique_outputs) == 1:
            notes.append("")
            notes.append(
                f"  WARNING: All {len(branch_outputs)} branch tests "
                f"produced identical output."
            )
            notes.append(
                f"    This suggests your conditional logic may not be "
                f"working correctly."
            )
            notes.append(
                f"    Different inputs should produce different results."
            )

    return points, notes


def grade_file(file_path, problem_name, problem_rubric):
    """
    Grade a single file. Returns (points_earned, list_of_notes).
    """
    total_points = 0
    all_notes = []

    # Check file contents (I/P/O block)
    pts, notes = check_file_contents(file_path, problem_rubric)
    total_points += pts
    all_notes.extend(notes)

    # Run test cases (branch + validation)
    pts, notes = run_test_cases(file_path, problem_rubric)
    total_points += pts
    all_notes.extend(notes)

    return total_points, all_notes


def find_student_files(folder_path, rubric):
    """
    Scan a folder for .py files that match known problem contexts.
    Returns a list of (file_path, problem_name) tuples.
    Ignores the autograder file itself.
    """
    matches = []
    autograder_name = os.path.basename(__file__).lower()

    for file_name in sorted(os.listdir(folder_path)):
        if not file_name.endswith(".py"):
            continue
        if file_name.lower() == autograder_name:
            continue

        problem_name = identify_problem(file_name, rubric)
        if problem_name:
            matches.append((os.path.join(folder_path, file_name), problem_name))
        else:
            print(f"  [?] {file_name}: not recognized as a known context (skipped)")

    return matches


def print_separator():
    """Print a visual separator line."""
    print("-" * 60)


def main():
    # Determine folder and rubric paths
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = os.path.dirname(os.path.abspath(__file__))

    rubric_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "a02_rubric.json"
    )

    if not os.path.exists(rubric_path):
        print(f"Error: Cannot find a02_rubric.json at {rubric_path}")
        print("Make sure the rubric file is in the same folder as this autograder.")
        sys.exit(1)

    rubric = load_rubric(rubric_path)

    print()
    print("=" * 60)
    print("  IS 303 Autograder: A02 - Decisions")
    print("=" * 60)
    print(f"  Scanning: {folder_path}")
    print()

    # Find matching files
    matches = find_student_files(folder_path, rubric)

    if not matches:
        print("  No recognized Python files found.")
        print()
        print("  Make sure your file names match one of these patterns:")
        for problem, names in rubric["problem_naming"].items():
            print(f"    {problem}: {', '.join(names[:3])}")
        print()
        sys.exit(1)

    # Grade each file
    total_score = 0
    problems_found = []

    for file_path, problem_name in matches:
        file_name = os.path.basename(file_path)
        problem_rubric = rubric["problem_rubrics"][problem_name]

        print_separator()
        print(f"  File: {file_name}")
        print(f"  Context: {problem_name}")
        print()

        pts, notes = grade_file(file_path, problem_name, problem_rubric)
        total_score += pts
        problems_found.append(problem_name)

        # Calculate max possible for this problem
        max_content = sum(c["points"] for c in problem_rubric["content_checks"])
        max_tests = sum(tc["points"] for tc in problem_rubric["test_cases"])
        max_possible = max_content + max_tests

        print(f"  Score: {pts}/{max_possible}")

        if notes:
            print()
            print("  Issues found:")
            for note in notes:
                print(f"    {note}")
        else:
            print("  All checks passed!")

        print()

    # Summary
    print_separator()
    print()
    print("  SUMMARY")
    print()
    print(f"  Programs found: {len(matches)}")
    for pname in problems_found:
        print(f"    - {pname}")
    print()

    if len(matches) < 2:
        print("  WARNING: This assignment requires TWO programs from")
        print("  different contexts. Only one was found.")
        print()

    if len(matches) >= 2 and len(set(problems_found)) < 2:
        print("  WARNING: Both files matched the same context.")
        print("  You need two DIFFERENT contexts.")
        print()

    print(f"  Autograder score: {total_score} (content + output checks only)")
    print()
    print("  Note: This score does NOT include points for code organization,")
    print("  boolean operator usage, f-string quality, condition order,")
    print("  commit messages, or GitHub submission. Those are graded by")
    print("  your instructor.")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
