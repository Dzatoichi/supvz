import subprocess
import sys


def run_tests():
    subprocess.run(["docker", "compose", "up", "-d", "postgres_test"], check=True)

    exit_code = 0
    try:
        result = subprocess.run(["poetry", "run", "pytest"], shell=True)
        exit_code = result.returncode
    except Exception:
        exit_code = 1
    finally:
        subprocess.run(["docker", "compose", "stop", "postgres_test"], shell=True)

    sys.exit(exit_code)


if __name__ == "__main__":
    run_tests()
