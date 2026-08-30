package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
	"text/tabwriter"
)


type Process struct {
	ID         string
	Arrival    int
	Burst      int
	Remaining  int 
	Completion int
	TurnAround int
	Waiting    int
}


type GanttSegment struct {
	ID    string
	Start int
	End   int
}


func readString(reader *bufio.Reader, prompt string) string {
	fmt.Print(prompt)
	line, _ := reader.ReadString('\n')
	return strings.TrimSpace(line)
}

func readInt(reader *bufio.Reader, prompt string) int {
	for {
		fmt.Print(prompt)
		line, _ := reader.ReadString('\n')
		line = strings.TrimSpace(line)
		val, err := strconv.Atoi(line)
		if err != nil || val < 0 {
			fmt.Println("  -> Please enter a valid non-negative whole number.")
			continue
		}
		return val
	}
}

func readPositiveInt(reader *bufio.Reader, prompt string) int {
	for {
		val := readInt(reader, prompt)
		if val <= 0 {
			fmt.Println("  -> Value must be greater than 0.")
			continue
		}
		return val
	}
}


func scheduleFCFS(procs []Process) ([]Process, []GanttSegment) {
	ps := make([]Process, len(procs))
	copy(ps, procs)

	
	sort.SliceStable(ps, func(i, j int) bool {
		return ps[i].Arrival < ps[j].Arrival
	})

	currentTime := 0
	var gantt []GanttSegment

	for i := range ps {
		if currentTime < ps[i].Arrival {
			currentTime = ps[i].Arrival 
		}
		start := currentTime
		end := start + ps[i].Burst

		ps[i].Completion = end
		ps[i].TurnAround = end - ps[i].Arrival
		ps[i].Waiting = ps[i].TurnAround - ps[i].Burst

		gantt = append(gantt, GanttSegment{ID: ps[i].ID, Start: start, End: end})
		currentTime = end
	}

	return ps, gantt
}


func scheduleSJF(procs []Process) ([]Process, []GanttSegment) {
	ps := make([]Process, len(procs))
	copy(ps, procs)

	n := len(ps)
	done := make([]bool, n)
	currentTime := 0
	completed := 0
	var gantt []GanttSegment

	for completed < n {
		idx := -1
		for i := range ps {
			if done[i] || ps[i].Arrival > currentTime {
				continue
			}
			if idx == -1 ||
				ps[i].Burst < ps[idx].Burst ||
				(ps[i].Burst == ps[idx].Burst && ps[i].Arrival < ps[idx].Arrival) {
				idx = i
			}
		}

		if idx == -1 {
			
			next := -1
			for i := range ps {
				if !done[i] && (next == -1 || ps[i].Arrival < next) {
					next = ps[i].Arrival
				}
			}
			currentTime = next
			continue
		}

		start := currentTime
		end := start + ps[idx].Burst

		ps[idx].Completion = end
		ps[idx].TurnAround = end - ps[idx].Arrival
		ps[idx].Waiting = ps[idx].TurnAround - ps[idx].Burst

		gantt = append(gantt, GanttSegment{ID: ps[idx].ID, Start: start, End: end})

		currentTime = end
		done[idx] = true
		completed++
	}

	return ps, gantt
}


func scheduleRR(procs []Process, quantum int) ([]Process, []GanttSegment) {
	ps := make([]Process, len(procs))
	copy(ps, procs)
	for i := range ps {
		ps[i].Remaining = ps[i].Burst
	}

	
	sort.SliceStable(ps, func(i, j int) bool {
		return ps[i].Arrival < ps[j].Arrival
	})

	n := len(ps)
	added := make([]bool, n) 
	var queue []int
	currentTime := ps[0].Arrival
	completed := 0
	var gantt []GanttSegment

	
	addArrivals := func() {
		for i := 0; i < n; i++ {
			if !added[i] && ps[i].Arrival <= currentTime {
				queue = append(queue, i)
				added[i] = true
			}
		}
	}

	addArrivals()

	for completed < n {
		if len(queue) == 0 {
			
			next := -1
			for i := 0; i < n; i++ {
				if !added[i] && (next == -1 || ps[i].Arrival < next) {
					next = ps[i].Arrival
				}
			}
			currentTime = next
			addArrivals()
			continue
		}

		idx := queue[0]
		queue = queue[1:]

		start := currentTime
		runTime := quantum
		if ps[idx].Remaining < quantum {
			runTime = ps[idx].Remaining
		}
		currentTime += runTime
		ps[idx].Remaining -= runTime
		end := currentTime

		gantt = append(gantt, GanttSegment{ID: ps[idx].ID, Start: start, End: end})

		
		addArrivals()

		if ps[idx].Remaining > 0 {
			queue = append(queue, idx)
		} else {
			ps[idx].Completion = end
			ps[idx].TurnAround = end - ps[idx].Arrival
			ps[idx].Waiting = ps[idx].TurnAround - ps[idx].Burst
			completed++
		}
	}

	return ps, gantt
}


func centerText(s string, width int) string {
	if len(s) >= width {
		return s[:width]
	}
	left := (width - len(s)) / 2
	right := width - len(s) - left
	return strings.Repeat(" ", left) + s + strings.Repeat(" ", right)
}

func printGantt(gantt []GanttSegment) {
	if len(gantt) == 0 {
		fmt.Println("(no execution segments)")
		return
	}

	widths := make([]int, len(gantt))
	for i, seg := range gantt {
		w := len(seg.ID) + 2
		if w < 6 {
			w = 6
		}
		widths[i] = w
	}

	var top strings.Builder
	top.WriteString("|")
	for i, seg := range gantt {
		top.WriteString(centerText(seg.ID, widths[i]))
		top.WriteString("|")
	}

	border := strings.Repeat("-", len(top.String()))

	var bottom strings.Builder
	firstMark := fmt.Sprintf("%d", gantt[0].Start)
	bottom.WriteString(firstMark)
	bottom.WriteString(strings.Repeat(" ", widths[0]+1-len(firstMark)))
	for i, seg := range gantt {
		mark := fmt.Sprintf("%d", seg.End)
		if i < len(gantt)-1 {
			pad := widths[i+1] + 1 - len(mark)
			if pad < 1 {
				pad = 1
			}
			bottom.WriteString(mark)
			bottom.WriteString(strings.Repeat(" ", pad))
		} else {
			bottom.WriteString(mark)
		}
	}

	fmt.Println(border)
	fmt.Println(top.String())
	fmt.Println(border)
	fmt.Println(bottom.String())
}

func printTable(ps []Process) {
	sorted := make([]Process, len(ps))
	copy(sorted, ps)
	sort.Slice(sorted, func(i, j int) bool {
		return sorted[i].Arrival < sorted[j].Arrival
	})

	w := tabwriter.NewWriter(os.Stdout, 0, 4, 2, ' ', 0)
	fmt.Fprintln(w, "Crew (PID)\tArrival\tBurst\tCompletion\tTurnaround\tWaiting")

	var totalWT, totalTAT int
	for _, p := range sorted {
		fmt.Fprintf(w, "%s\t%d\t%d\t%d\t%d\t%d\n",
			p.ID, p.Arrival, p.Burst, p.Completion, p.TurnAround, p.Waiting)
		totalWT += p.Waiting
		totalTAT += p.TurnAround
	}
	w.Flush()

	n := float64(len(sorted))
	fmt.Printf("\nAverage Waiting Time    : %.2f\n", float64(totalWT)/n)
	fmt.Printf("Average Turnaround Time : %.2f\n", float64(totalTAT)/n)
}


func printBanner() {
	fmt.Println("=================================================")
	fmt.Println("   GRAND LINE CPU SCHEDULING SIMULATOR")
	fmt.Println("   (Each pirate crew = one process in the queue)")
	fmt.Println("=================================================")
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	printBanner()

	n := readPositiveInt(reader, "\nHow many pirate crews (processes) are arriving? ")

	procs := make([]Process, 0, n)
	usedIDs := make(map[string]bool)

	for i := 0; i < n; i++ {
		fmt.Printf("\n--- Crew #%d ---\n", i+1)
		id := readString(reader, "Crew name / Process ID (e.g. Luffy or P1): ")
		if id == "" || usedIDs[id] {
			id = fmt.Sprintf("P%d", i+1)
			fmt.Printf("  -> Using default ID: %s\n", id)
		}
		usedIDs[id] = true

		arrival := readInt(reader, "Arrival Time: ")
		burst := readPositiveInt(reader, "Burst Time (voyage duration on CPU): ")

		procs = append(procs, Process{ID: id, Arrival: arrival, Burst: burst})
	}

	for {
		fmt.Println("\n-------------------------------------------------")
		fmt.Println("Choose a Scheduling Algorithm:")
		fmt.Println("1. First Come First Serve (FCFS)")
		fmt.Println("2. Shortest Job First (SJF - Non-Preemptive)")
		fmt.Println("3. Round Robin (RR)")
		fmt.Println("4. Exit")

		choice := readInt(reader, "Enter choice: ")

		var result []Process
		var gantt []GanttSegment
		var title string

		switch choice {
		case 1:
			result, gantt = scheduleFCFS(procs)
			title = "First Come First Serve (FCFS)"
		case 2:
			result, gantt = scheduleSJF(procs)
			title = "Shortest Job First (SJF - Non-Preemptive)"
		case 3:
			tq := readPositiveInt(reader, "Enter Time Quantum: ")
			result, gantt = scheduleRR(procs, tq)
			title = fmt.Sprintf("Round Robin (Time Quantum = %d)", tq)
		case 4:
			fmt.Println("\nFair winds, Captain! Exiting simulator.")
			return
		default:
			fmt.Println("  -> Invalid choice, please try again.")
			continue
		}

		fmt.Printf("\n=== %s ===\n\n", title)
		fmt.Println("Gantt Chart / Execution Timeline:")
		printGantt(gantt)
		fmt.Println()
		printTable(result)
	}
}
