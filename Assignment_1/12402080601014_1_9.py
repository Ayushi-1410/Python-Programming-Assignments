import heapq

print("THREADED JOB SCHEDULER")

w = int(input("Enter number of workers: "))
n = int(input("Enter number of jobs: "))

jobs = []

for i in range(n):

    print("\nEnter details for job", i + 1)

    arrival = int(input("Arrival time: "))
    job_id = input("Job ID: ")
    priority = int(input("Priority: "))
    duration = int(input("Duration: "))
    resources = int(input("Resources: "))

    jobs.append(
        (
            arrival,
            -priority,
            job_id,
            duration,
            resources
        )
    )

jobs.sort()

worker_time = [0] * w

result = []

total_wait = 0

for job in jobs:

    arrival = job[0]
    priority = -job[1]
    job_id = job[2]
    duration = job[3]
    resources = job[4]

    worker = min(
        range(w),
        key=lambda x: worker_time[x]
    )

    start_time = max(
        arrival,
        worker_time[worker]
    )

    finish_time = start_time + duration

    wait_time = start_time - arrival

    worker_time[worker] = finish_time

    total_wait += wait_time

    result.append(
        (
            start_time,
            job_id,
            worker + 1,
            wait_time
        )
    )

result.sort()

print("\nRESULT")

for start_time, job_id, worker, wait in result:

    print(
        job_id,
        "W" + str(worker),
        start_time,
        wait
    )

average_wait = total_wait / n

print("AVG_WAIT", round(average_wait, 2))