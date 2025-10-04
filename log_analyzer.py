import time

# -------------------------------
# 1. Generator Function: read_logs
# -------------------------------
def read_logs(file_path):
    """Generator that yields one log line at a time"""
    with open(file_path, "r") as f:
        for line in f:
            yield line.strip()  # remove extra spaces/newline


# -------------------------------
# 2. Decorator: time_it
# -------------------------------
def time_it(func):
    """Decorator to measure execution time of functions"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Execution time of {func.__name__}: {end - start:.6f} seconds")
        return result
    return wrapper


# -------------------------------
# 3. Analysis Functions
# -------------------------------
@time_it
def analyze_logs(file_path):
    logs = list(read_logs(file_path))   # consume generator

    # Extract ERROR logs into a list (list comprehension)
    error_logs = [log for log in logs if "ERROR" in log]

    # Build set of unique log levels (set comprehension)
    log_levels = {log.split(",")[1] for log in logs}

    # Build dictionary mapping level → count (dict comprehension)
    log_count = {level: sum(1 for log in logs if level in log) for level in log_levels}

    return error_logs, log_levels, log_count


# -------------------------------
# 4. Bonus: filter_logs generator
# -------------------------------
def filter_logs(file_path, level):
    """Generator that yields only logs of given level"""
    for log in read_logs(file_path):
        if f",{level}," in log:
            yield log


@time_it
def error_code_count(file_path):
    """Dictionary comprehension to count ERROR codes"""
    # Extract only error logs
    error_logs = [log for log in read_logs(file_path) if "ERROR" in log]

    # Build dictionary {code: count}
    error_codes = {
        log.split("code=")[1]: sum(1 for l in error_logs if log.split("code=")[1] in l)
        for log in error_logs if "code=" in log
    }
    return error_codes


# -------------------------------
# 5. Main Driver
# -------------------------------
if __name__ == "__main__":
    file_path = "server.log"

    # Run analysis
    errors, levels, counts = analyze_logs(file_path)
    print("\n--- Log Analysis ---")
    print("Error Logs:", errors)
    print("Unique Levels:", levels)
    print("Log Counts:", counts)

    # Bonus: filter specific logs
    print("\n--- Filtered ERROR Logs ---")
    for log in filter_logs(file_path, "ERROR"):
        print(log)

    # Bonus: ERROR code counts
    print("\n--- Error Code Count ---")
    print(error_code_count(file_path))
