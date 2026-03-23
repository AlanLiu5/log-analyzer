# 📊 Log Analyzer (Python)

A simple but practical command-line tool to analyze log files.  
Supports both **custom simple logs** and **Nginx access logs**.

---

## 🚀 Features

- Count total requests
- Count errors (404 / 500)
- Top visited pages
- Top error pages
- Most active users (IP)
- Peak traffic hours
- Support multiple log formats

---

## 📂 Supported Formats

### 1. Simple Format

```
2026-03-17 10:00:03 GET /home 200 ip=1.1.1.1
```

---

### 2. Nginx Format

```
1.2.3.4 - - [18/Mar/2026:10:00:01 +1100] "GET /home HTTP/1.1" 200 123 "-" "UA"
```

---

## 🛠 Usage

### Basic Command

```
python log_tool.py --input access.log --k 5 --format simple
```

---

### Nginx Log

```
python log_tool.py --input nginx_access.log --k 5 --format nginx
```

---

### Save Output

```
python log_tool.py --input nginx_access.log --k 5 --format nginx --output report.txt
```

---

## 📊 Example Output

```
total_requests = 6
count_404 = 2
count_500 = 1

Top Pages:
1) /api -> 2
2) /home -> 2
3) /missing -> 2

Errors:
error_total = 3
count_404 = 2
count_500 = 1

Top Error Pages:
1) /missing -> 2
2) /api -> 1

Top Users (IP):
1) 1.2.3.4 -> 2
2) 2.2.2.2 -> 2
3) 3.3.3.3 -> 1

Top Hours:
1) 10 -> 3
2) 11 -> 2
3) 12 -> 1
```

---

## 🧪 Run Tests

```
python test_log.py
```

---

## 🧠 Project Structure

- log_lib.py → core logic (parsing + analysis)
- log_tool.py → CLI entry
- test_log.py → tests
- sample logs included

---

## 💡 Future Improvements

- Web UI (upload log files)
- Visualization (charts)
- Real-time monitoring
- More log formats (JSON, CSV)

---

## 👤 Author

Alan (University of Melbourne)