from collections import defaultdict, deque

x, t = map(int, input("Enter X and T: ").split())
n = int(input("Enter number of logs: "))

failed = defaultdict(deque)
suspicious = {}

for _ in range(n):
    time, user, ip, status = input().split()
    hour, minute = map(int, time.split(":"))
    current_time = hour * 60 + minute

    queue = failed[user]

    while queue and current_time - queue[0][0] > t:
        queue.popleft()

    if status == "FAIL":
        queue.append((current_time, ip))

    elif status == "SUCCESS":
        different_ip = any(old_ip != ip for _, old_ip in queue)

        if len(queue) >= x and different_ip:
            if user not in suspicious:
                suspicious[user] = time

for user in sorted(suspicious):
    print(user, suspicious[user])