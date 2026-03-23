import re
_NGINX_RE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d{3})'
)

def parse_nginx_line(line: str):
    m = _NGINX_RE.match(line.strip())
    if not m:
        return None

    ip = m.group("ip")
    raw_time = m.group("time")  # 18/Mar/2026:10:00:01 +1100
    method = m.group("method")
    path = m.group("path")
    status = int(m.group("status"))

    # time -> date/time（简化处理）
    date_part = raw_time.split(":")[0]  # 18/Mar/2026
    hh = raw_time.split(":")[1]
    mm = raw_time.split(":")[2]
    ss = raw_time.split(":")[3].split()[0]
    time_str = f"{hh}:{mm}:{ss}"

    day, mon, year = date_part.split("/")
    mon_map = {
        "Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06",
        "Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"
    }
    date_str = f"{year}-{mon_map.get(mon,'01')}-{day.zfill(2)}"

    return {"date": date_str, "time": time_str, "method": method, "path": path, "status": status, "ip": ip}
def parse_line(line: str,fmt: str = "simple"):
    if fmt == "nginx":
        return parse_nginx_line(line)
    """
    A格式：
    2026-03-17 10:00:03 GET /missing 404 ip=2.2.2.2
    返回 dict：{"date":..., "time":..., "method":..., "path":..., "status":..., "ip":...}
    """
    parts = line.strip().split()
    if len(parts) < 6:
        return None

    try:
        status = int(parts[4])
    except ValueError:
        return None

    ip_part = parts[5]
    if not ip_part.startswith("ip="):
        return None

    return {
        "date": parts[0],
        "time": parts[1],
        "method": parts[2],
        "path": parts[3],
        "status": status,
        "ip": ip_part[3:],
    }


def analyze_basic(filename: str,fmt: str = "simple"):
    """
    返回：total, count_404, count_500
    """
    total = 0
    count_404 = 0
    count_500 = 0

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue

            d = parse_line(line,fmt)
            if d is None:
                continue

            total += 1
            if d["status"] == 404:
                count_404 += 1
            if d["status"] == 500:
                count_500 += 1

    return total, count_404, count_500


def top_paths(filename: str, k: int ,fmt: str = "simple"):
    counts = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            d = parse_line(line, fmt)
            if d is None:
                continue

            path = d["path"]
            counts[path] = counts.get(path, 0) + 1

    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))  [:k]
def error_counts(filename: str,fmt: str = "simple"):
    """
    返回：count_404, count_500, count_error_total
    """
    c404 = 0
    c500 = 0

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            d = parse_line(line, fmt)
            if d is None:
                continue

            if d["status"] == 404:
                c404 += 1
            if d["status"] == 500:
                c500 += 1

    return c404, c500, (c404 + c500)


def top_error_paths(filename: str, k: int,fmt: str = "simple" ):
    """
    只统计错误(404/500)的页面，返回 Top k: [("/missing", 2), ...]
    """
    counts = {}

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            d = parse_line(line, fmt)
            if d is None:
                continue

            status = d["status"]
            if status not in (404, 500):
                continue

            path = d["path"]
            counts[path] = counts.get(path, 0) + 1

    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:k]
def top_ips(filename: str, k: int,fmt: str = "simple" ):
    """
    返回 Top k IP: [("1.1.1.1", 12), ...]
    """
    counts = {}

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue

            d = parse_line(line, fmt)
            if d is None:
                continue

            ip = d["ip"]
            counts[ip] = counts.get(ip, 0) + 1

    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:k]
def top_hours(filename: str, k: int,fmt: str = "simple"):
    """
    按小时统计访问次数（hour = time[:2]）。
    返回 Top k: [("10", 15), ("11", 8), ...]
    """
    counts = {}

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue

            d = parse_line(line, fmt)
            if d is None:
                continue

            # d["time"] 形如 "10:00:03"
            t = d["time"]
            if len(t) < 2:
                continue
            hour = t[:2]   # "10"

            counts[hour] = counts.get(hour, 0) + 1

    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:k]
if __name__ == "__main__":
    s = '1.2.3.4 - - [18/Mar/2026:10:00:01 +1100] "GET /home HTTP/1.1" 200 123 "-" "UA"'
    print(parse_line(s, fmt="nginx"))