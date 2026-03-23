from log_lib import parse_line, analyze_basic, top_paths, error_counts, top_error_paths, top_ips, top_hours

def test_error_counts():
    filename = "access_err_test.log"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("2026-03-17 10:00:01 GET /home 200 ip=1.1.1.1\n")
        f.write("2026-03-17 10:00:03 GET /missing 404 ip=2.2.2.2\n")
        f.write("2026-03-17 10:00:04 POST /api 500 ip=3.3.3.3\n")
        f.write("2026-03-17 10:00:05 GET /missing 404 ip=2.2.2.2\n")

    c404, c500, total = error_counts(filename)
    assert c404 == 2
    assert c500 == 1
    assert total == 3


def test_top_error_paths():
    filename = "access_err_test2.log"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("2026-03-17 10:00:01 GET /home 200 ip=1.1.1.1\n")
        f.write("2026-03-17 10:00:03 GET /missing 404 ip=2.2.2.2\n")
        f.write("2026-03-17 10:00:04 POST /api 500 ip=3.3.3.3\n")
        f.write("2026-03-17 10:00:05 GET /missing 404 ip=2.2.2.2\n")

    top = top_error_paths(filename, k=2)
    assert top == [("/missing", 2), ("/api", 1)]
def test_parse_line():
    line = "2026-03-17 10:00:03 GET /missing 404 ip=2.2.2.2"
    d = parse_line(line)
    assert d["path"] == "/missing"
    assert d["status"] == 404
    assert d["ip"] == "2.2.2.2"


def test_analyze_basic():
    # 用一个小测试文件
    filename = "access_test.log"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("2026-03-17 10:00:01 GET /home 200 ip=1.1.1.1\n")
        f.write("2026-03-17 10:00:03 GET /missing 404 ip=2.2.2.2\n")
        f.write("2026-03-17 10:00:04 POST /api 500 ip=3.3.3.3\n")

    total, c404, c500 = analyze_basic(filename)
    assert total == 3
    assert c404 == 1
    assert c500 == 1
def test_top_paths():
    filename = "access_test2.log"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("2026-03-17 10:00:01 GET /home 200 ip=1.1.1.1\n")
        f.write("2026-03-17 10:00:02 GET /home 200 ip=1.1.1.1\n")
        f.write("2026-03-17 10:00:03 GET /login 200 ip=2.2.2.2\n")

    top = top_paths(filename, k=2)
    assert top == [("/home", 2), ("/login", 1)]
def test_top_hours():
    filename = "access_hour_test.log"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("2026-03-17 10:00:01 GET /home 200 ip=1.1.1.1\n")
        f.write("2026-03-17 10:10:02 GET /home 200 ip=1.1.1.1\n")
        f.write("2026-03-17 11:00:03 GET /login 200 ip=2.2.2.2\n")
        f.write("2026-03-17 11:20:04 GET /login 200 ip=2.2.2.2\n")
        f.write("2026-03-17 11:40:05 GET /missing 404 ip=3.3.3.3\n")

    top = top_hours(filename, k=2)
    assert top == [("11", 3), ("10", 2)]


if __name__ == "__main__":
    test_parse_line()
    test_analyze_basic()
    test_top_paths()
    test_error_counts()
    test_top_error_paths()
    test_top_hours()
    print("all log tests passed")