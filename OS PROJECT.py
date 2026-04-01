import tkinter as tk
from tkinter import ttk, messagebox

BOX_WIDTH = 8

# ------------------ Scheduling Algorithms ------------------

def fcfs(processes):
    processes = sorted(processes, key=lambda x: x[2])
    time = 0
    result = []
    gantt = []

    for pid, bt, at in processes:
        if time < at:
            gantt.append(("IDLE", time, at))
            time = at

        start = time
        time += bt
        ct = time
        tat = ct - at
        wt = tat - bt

        gantt.append((pid, start, ct))
        result.append((pid, at, bt, ct, wt, tat))

    return result, gantt


def sjf(processes):
    time = 0
    gantt = []
    completed = []
    processes = processes.copy()

    while processes:
        ready = [p for p in processes if p[2] <= time]

        if not ready:
            next_at = min(p[2] for p in processes)
            gantt.append(("IDLE", time, next_at))
            time = next_at
            continue

        pid, bt, at = min(ready, key=lambda x: x[1])
        start = time
        time += bt
        ct = time
        tat = ct - at
        wt = tat - bt

        gantt.append((pid, start, ct))
        completed.append((pid, at, bt, ct, wt, tat))
        processes.remove((pid, bt, at))

    return completed, gantt


def round_robin(processes, tq):
    time = 0
    gantt = []
    queue = []
    remaining = {}
    completed = {}

    processes = sorted(processes, key=lambda x: x[2])

    for pid, bt, at in processes:
        remaining[pid] = bt

    i = 0
    n = len(processes)

    while len(completed) < n:
        while i < n and processes[i][2] <= time:
            queue.append(processes[i][0])
            i += 1

        if not queue:
            next_at = processes[i][2]
            gantt.append(("IDLE", time, next_at))
            time = next_at
            continue

        pid = queue.pop(0)

        exec_time = min(tq, remaining[pid])
        start = time
        time += exec_time
        remaining[pid] -= exec_time

        gantt.append((pid, start, time))

        while i < n and processes[i][2] <= time:
            queue.append(processes[i][0])
            i += 1

        if remaining[pid] > 0:
            queue.append(pid)
        else:
            completed[pid] = time

    result = []
    for pid, bt, at in processes:
        ct = completed[pid]
        tat = ct - at
        wt = tat - bt
        result.append((pid, at, bt, ct, wt, tat))

    return result, gantt


# ------------------ GUI Functions ------------------

def create_table():
    for w in table_frame.winfo_children():
        w.destroy()

    global entries
    entries = []

    try:
        n = int(proc_entry.get())
    except:
        messagebox.showerror("Error", "Enter valid number")
        return

    headers = ["Process ID", "Arrival Time", "Burst Time"]
    for c, h in enumerate(headers):
        ttk.Label(table_frame, text=h,
                  font=("Arial", 10, "bold")).grid(row=0, column=c, padx=14, pady=4)

    for i in range(n):
        pid = ttk.Entry(table_frame, width=14)
        at = ttk.Entry(table_frame, width=14)
        bt = ttk.Entry(table_frame, width=14)

        pid.grid(row=i+1, column=0, pady=4)
        at.grid(row=i+1, column=1, pady=4)
        bt.grid(row=i+1, column=2, pady=4)

        entries.append((pid, at, bt))


def simulate():
    algo = algo_var.get()

    tq = None
    if algo == "Round Robin":
        try:
            tq = int(tq_entry.get())
        except:
            messagebox.showerror("Error", "Invalid Time Quantum")
            return

    processes = []
    for pid_e, at_e, bt_e in entries:
        processes.append((pid_e.get(), int(bt_e.get()), int(at_e.get())))

    if algo == "FCFS":
        result, gantt = fcfs(processes)
    elif algo == "SJF":
        result, gantt = sjf(processes)
    else:
        result, gantt = round_robin(processes, tq)

    output.delete("1.0", tk.END)

    # ----------------- Text Decorations -----------------
    output.tag_configure("header", foreground="blue", font=("Consolas", 10, "bold"))
    output.tag_configure("avg", foreground="green", font=("Consolas", 10, "bold"))
    output.tag_configure("gantt", foreground="purple", font=("Consolas", 10, "bold"))
    output.tag_configure("row1", background="#f0f8ff")  # light blue
    output.tag_configure("row2", background="#ffffff")  # white

    # --- Table header ---
    output.insert(tk.END,
        "Process".ljust(10) + "AT".ljust(8) + "BT".ljust(8) +
        "CT".ljust(8) + "WT".ljust(8) + "TAT".ljust(8) + "\n",
        "header")
    output.insert(tk.END, "-" * 60 + "\n", "header")

    # --- Table rows ---
    awt = atat = 0
    for idx, (pid, at, bt, ct, wt, tat) in enumerate(result):
        tag = "row1" if idx % 2 == 0 else "row2"
        output.insert(tk.END,
            f"{pid:<10}{at:<8}{bt:<8}{ct:<8}{wt:<8}{tat:<8}\n",
            tag)
        awt += wt
        atat += tat

    n = len(result)
    # --- Averages ---
    output.insert(tk.END, f"\nAverage WT  = {awt/n:.2f}\n", "avg")
    output.insert(tk.END, f"Average TAT = {atat/n:.2f}\n\n", "avg")

    # --- Gantt chart heading ---
    output.insert(tk.END, "Gantt Chart:\n", "gantt")
    for pid, s, e in gantt:
        output.insert(tk.END, f"|{pid.center(BOX_WIDTH)}")
    output.insert(tk.END, "|\n")

    for pid, s, e in gantt:
        output.insert(tk.END, f"{str(s).ljust(BOX_WIDTH+1)}")
    output.insert(tk.END, str(gantt[-1][2]))


# ------------------ Main Window ------------------

root = tk.Tk()
root.title("CPU Scheduling Algorithm Simulator")
root.geometry("980x620")
root.resizable(False, False)

BG = "#e6f2ff"
root.configure(bg=BG)

tk.Label(root, text="CPU Scheduling Algorithm Simulator",
         font=("Arial", 22, "bold"), bg=BG).pack(pady=10)

frame_algo = tk.Frame(root, bg=BG)
frame_algo.pack(pady=6)

tk.Label(frame_algo, text="Algorithm:", bg=BG,
         font=("Arial", 12)).grid(row=0, column=0)

algo_var = tk.StringVar(value="FCFS")
ttk.Combobox(frame_algo, textvariable=algo_var,
             values=["FCFS", "SJF", "Round Robin"],
             state="readonly", width=22).grid(row=0, column=1)

tk.Label(frame_algo, text="Time Quantum:",
         bg=BG, font=("Arial", 12)).grid(row=1, column=0)
tq_entry = ttk.Entry(frame_algo, width=22)
tq_entry.grid(row=1, column=1)

frame_proc = tk.Frame(root, bg=BG)
frame_proc.pack(pady=6)

tk.Label(frame_proc, text="No. of Processes:", bg=BG,
         font=("Arial", 12)).grid(row=0, column=0)
proc_entry = ttk.Entry(frame_proc, width=18)
proc_entry.grid(row=0, column=1)

ttk.Button(frame_proc, text="Create Table",
           command=create_table).grid(row=0, column=2, padx=8)

table_frame = tk.Frame(root, bg=BG)
table_frame.pack(pady=6)

ttk.Button(root, text="Simulate",
           command=simulate).pack(pady=8)

output = tk.Text(root, height=20, width=105, font=("Consolas", 10))
output.pack(pady=8)

root.mainloop()
