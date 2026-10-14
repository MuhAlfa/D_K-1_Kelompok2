class Process:
    def __init__(self, pid, arrival, burst, priority):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.remaining = burst
        self.start_time = -1
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1

def reset_procs():
    return [
        Process("P1", 0, 5, 2),
        Process("P2", 2, 3, 1),
        Process("P3", 3, 10, 4),
        Process("P4", 4, 4, 2),
        Process("P5", 7, 6, 3)
    ]

def cetak_hasil(nama, procs):
    total_wt = sum(p.waiting_time for p in procs)
    total_tat = sum(p.turnaround_time for p in procs)
    total_rt = sum(p.response_time for p in procs)
    n = len(procs)
    
    print(f"\n=== HASIL SIMULASI {nama} ===")
    print(f"{'PID':<6}{'Arrival':<9}{'Burst':<8}{'Priority':<10}{'Completion':<12}{'TAT':<8}{'WT':<8}{'RT':<8}")
    for p in procs:
        print(f"{p.pid:<6}{p.arrival:<9}{p.burst:<8}{p.priority:<10}{p.completion_time:<12}{p.turnaround_time:<8}{p.waiting_time:<8}{p.response_time:<8}")
    print(f"Rata-rata WT: {total_wt/n:.2f} | Rata-rata TAT: {total_tat/n:.2f} | Rata-rata RT: {total_rt/n:.2f}")

procs = reset_procs()
time = 0
for p in procs:
    if time < p.arrival: time = p.arrival
    p.start_time = time
    p.response_time = p.start_time - p.arrival
    time += p.burst
    p.completion_time = time
    p.turnaround_time = p.completion_time - p.arrival
    p.waiting_time = p.turnaround_time - p.burst
cetak_hasil("FCFS", procs)

procs = reset_procs()
time = 0; completed = 0; n = len(procs)
while completed < n:
    ready = [p for p in procs if p.arrival <= time and p.completion_time == 0]
    if ready:
        p = min(ready, key=lambda x: x.burst)
        if p.start_time == -1: p.start_time = time
        p.response_time = p.start_time - p.arrival
        time += p.burst
        p.completion_time = time
        p.turnaround_time = p.completion_time - p.arrival
        p.waiting_time = p.turnaround_time - p.burst
        completed += 1
    else:
        time += 1
cetak_hasil("SJF", procs)

procs = reset_procs()
time = 0; completed = 0
while completed < n:
    ready = [p for p in procs if p.arrival <= time and p.completion_time == 0]
    if ready:
        p = min(ready, key=lambda x: x.priority)
        if p.start_time == -1: p.start_time = time
        p.response_time = p.start_time - p.arrival
        time += p.burst
        p.completion_time = time
        p.turnaround_time = p.completion_time - p.arrival
        p.waiting_time = p.turnaround_time - p.burst
        completed += 1
    else:
        time += 1
cetak_hasil("Priority", procs)

def run_rr(quantum):
    procs = reset_procs()
    time = 0; queue = []
    def update_queue():
        for p in procs:
            if p.arrival <= time and p not in queue and p.remaining > 0 and p.start_time == -2:
                queue.append(p)
                p.start_time = -1
    
    for p in procs: p.start_time = -2
    while any(p.remaining > 0 for p in procs):
        update_queue()
        if not queue:
            time += 1
            continue
        p = queue.pop(0)
        if p.response_time == -1:
            p.response_time = time - p.arrival
        
        exec_time = min(quantum, p.remaining)
        p.remaining -= exec_time
        time += exec_time
        update_queue()
        
        if p.remaining > 0:
            queue.append(p)
        else:
            p.completion_time = time
            p.turnaround_time = p.completion_time - p.arrival
            p.waiting_time = p.turnaround_time - p.burst
    return procs

cetak_hasil("Round Robin (q=4)", run_rr(4))
cetak_hasil("Round Robin (q=6)", run_rr(6))