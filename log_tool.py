import argparse
from log_lib import analyze_basic, top_paths, error_counts, top_error_paths, top_ips, top_hours


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="log file name")
    parser.add_argument("--k", type=int, default=10, help="top k (default=10)")
    parser.add_argument("--format", choices=["simple", "nginx"] , help="file format(default=simple)")
    parser.add_argument("--output", default="", help="output report file (optional)")

    args = parser.parse_args()

    if args.k <= 0:
        print("k must be a positive integer")
        return

    lines = []

    try:
        total, c404, c500 = analyze_basic(args.input,fmt=args.format)
    except FileNotFoundError:
        print(f"file not found: {args.input}")
        return

    # --- Overview ---
    lines.append(f"total_requests = {total}")
    lines.append(f"count_404 = {c404}")
    lines.append(f"count_500 = {c500}")

    # --- Top Pages ---
    lines.append("")
    lines.append("Top Pages:")
    for i, (path, cnt) in enumerate(top_paths(args.input, k=args.k,fmt=args.format), start=1):
        lines.append(f"{i}) {path} -> {cnt}")

    # --- Errors ---
    c404, c500, cerr = error_counts(args.input,fmt=args.format)
    lines.append("")
    lines.append("Errors:")
    lines.append(f"error_total = {cerr}")
    lines.append(f"count_404 = {c404}")
    lines.append(f"count_500 = {c500}")

    # --- Top Error Pages ---
    lines.append("")
    lines.append("Top Error Pages:")
    for i, (path, cnt) in enumerate(top_error_paths(args.input, k=args.k,fmt=args.format), start=1):
        lines.append(f"{i}) {path} -> {cnt}")

    # --- Top Users (IP) ---
    lines.append("")
    lines.append("Top Users (IP):")
    for i, (ip, cnt) in enumerate(top_ips(args.input, k=args.k,fmt=args.format), start=1):
        lines.append(f"{i}) {ip} -> {cnt}")

    # --- Top Hours ---
    lines.append("")
    lines.append("Top Hours:")
    for i, (hour, cnt) in enumerate(top_hours(args.input, k=args.k,fmt=args.format), start=1):
        lines.append(f"{i}) {hour} -> {cnt}")

    report = "\n".join(lines)

    # 1) 打印到终端
    print(report)

    # 2) 如果传了 --output，就写入文件
    if args.output != "":
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report + "\n")
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()