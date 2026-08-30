# Pirate scheduler

<p>This was done in golang,I didnt know what golang was at first ,later on found out it was a programming language by google ,I built the pirate scheduler in go after 
installing it in vs code .So first using the main packae ,i imported a few library packages necessary for it like bufio,fmt, os .I had no idea what those were but learned along the way
.Then using type ,i inputed the types of different inputs like int for id,arrival etc for all those which was needed in the scheduler.Then used different function to use the three algorithms
thats is :</p>

# First Come First Serve (FCFS):
<p> This algorithm as the name suggested was used for made sure to take the inputs and order them in the manner of arrival like
the first one to arrive would be first on the schedule and so on.In this the first crew which arrives first will start and it continues till their burst time and sets the currentTime= end and moves
on to the next group.</p>

# Shortest Job First(SJF):
<p> This was used to select the ones out of the inputs who had the shortest task and those whose arrival time was less than currentTime,in this case the shortest burst time.So this algorithm chose the crew in the order of their task timing
,the shortest task was taken first.</p>

# Round Robin(RR):
<p> This was used to give each crew kind of like equal opportunity.It works like the first crew in the queuw starts to run and they go till the set duration and if their journey isnt finished that crew get moved to the last
then the next group undergoes the same things</p>

<img width="1710" height="1107" alt="Screenshot 2026-08-30 at 4 32 50 PM" src="https://github.com/user-attachments/assets/4476f91e-d4c9-4b6c-9f48-bc1c1c757132" />

In this I mainly learned the three algorithms and how it worked.
