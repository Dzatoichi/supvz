import subprocess
import sys


def run_tests():
    """
    Запускает тестовую БД и выполняет pytest.
    После завершения тестов останавливает контейнер с тестовой БД.
    """
    # Запуск тестовой БД с профилем test
    subprocess.run(
        ["docker", "compose", "--profile", "test", "up", "-d", "postgres_test"],
        check=True,
    )

    exit_code = 0
    try:
        # Запуск тестов
        result = subprocess.run(["poetry", "run", "pytest", "-v"])
        exit_code = result.returncode
    except Exception:
        exit_code = 1
    finally:
        # Остановка тестовой БД
        subprocess.run(["docker", "compose", "--profile", "test", "stop", "postgres_test"])

    sys.exit(exit_code)


if __name__ == "__main__":
    run_tests()
