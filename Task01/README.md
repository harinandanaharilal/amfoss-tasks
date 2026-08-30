# TASK-01:Prologue – The Logbook of the Grand Line

# Level 1

<p>The first level was to find the real devil fruit among the replicas ,it took place in Loguetown .The task was pretty straightforward but I realized it only later.
A few commands like cd ,ls -a and ./eat.sh was used.First I cloned the git repository using clone git and pasting the https path ,then used cd to get into that folder ,again multiple cd to get into Loguetown folder,There i found multiple files when i used ls -a .I had cloned the repo the first day the task was released so even after i tried running ./eat.sh multiple times nothing came up so i looked into the code in eat.sh file ,tried changing it and couldn't revert it back,I tried this after a few days later so i cloned it again and then when i used ./eat.sh it worked .By trial and error I found that the real devil fruit was in sector C ,devil_fruit_6.txt.I am a beginner 
when it comes to coding and other tech related activities so I took a lot of time with this level.As for my references for doing this was the git doc provided in the amfoss 
workshop .I completed level 1 on 26/07/2026.</p>
<img width="1710" height="1107" alt="Screenshot 2026-07-26 at 11 15 37 AM" src="https://github.com/user-attachments/assets/1113119d-0ca9-4935-8684-940a5a931884" />
<img width="1710" height="1107" alt="Screenshot 2026-07-26 at 11 15 47 AM" src="https://github.com/user-attachments/assets/562b902f-3aab-4122-a6eb-d67b19edaebc" />

# Level 2

<p>Level 2 was about getting a transmission code and a new thing came up git branch -a and git switch .I began by switching the branch into whiskey peak investigation in order to find the transmission code.Then I used ls -a to list all the files in it and used cd •baroque works cache and again used ls and found a unlock_vault.sh file ,I tried running it and it showed access denied put in password so i went opened the file in vs code and saw that the awakening signature i got from the last level "ONE_PIECE{GITO_GITO_NO_AWAKENING}" was the password and i put it in and then again ran the file and it gave me two log fils but no code so i was at it for days trying to find 
 what was wrong, it kept coming like this:</p>
 <p>sed: 2: "bounty_hunter_feed.log
": undefined label 'ounty_hunter_feed.1og'</p>
<p>So opened the file in vs code and looked at that line ,i tried google,tried recloning the repository but nothing worked .I even tried ai but it didn't know what was wrong.so i was just obssesing over that line in vs code ,i clicked it and vs code showed an option to modify it so i clicked it and it changed"/" to this "|" and when i ran it again it worked .At last I got the transmission code.</p>
<img width="856" height="98" alt="Screenshot 2026-07-29 at 3 01 12 AM" src="https://github.com/user-attachments/assets/b951b97a-22a9-4a12-9ad9-9dfdbf14424c" />
<p>The part after the sed ,i felt like something was there so i went through the code of unlock_vault.sh and on the sed line vs code suggested a modify or not option so i clicked modify so it changed "/" to this "|" and after that when i ran diff i got the transmission code.Maybe i changed it before or something I am not sure if it was an error i did on my part.Still I got the code.</p>
<img width="1710" height="1107" alt="Screenshot 2026-07-28 at 9 57 40 PM" src="https://github.com/user-attachments/assets/18e2369d-855d-4744-b395-40a25e84f146" />

# Level 3

<p>Level 3 was about finding the log report with the transmission code from level 2 in the little garden branch.After level 2 i got the hang of it.In this level the tricky part was finding which to encode the transmission code to,I just used Base64 because it came first when i searched about encodings.Then I used the encoding with git grep and i recieved the exact file on which the poneygleph fragment 1 was in </p>
<img width="1203" height="609" alt="Screenshot 2026-07-29 at 3 23 23 AM" src="https://github.com/user-attachments/assets/d5829e3f-2107-4d8a-82fa-a3ab1ab1b493" />
<img width="1710" height="1107" alt="Screenshot 2026-07-28 at 11 29 56 PM" src="https://github.com/user-attachments/assets/67521dc0-e5d8-4bdd-9500-fcfdf453ece1" />

# Level 4

<p>Level 4 was the easiest of all ,it was to find the other fragment among in the water7 folder .i dont know if i was meant to do it this way but when i opened the file i had an option to open it using archive utility and i opened it directly and i got the text file.I was unsure on whether to do it using terminal or not so since i got what i needed i just moved on to the next task</p>
<img width="863" height="400" alt="Screenshot 2026-07-29 at 3 26 49 AM" src="https://github.com/user-attachments/assets/8533a023-c1b3-45e6-92a7-15893ad2f71d" />
<img width="619" height="293" alt="Screenshot 2026-07-29 at 3 25 45 AM" src="https://github.com/user-attachments/assets/3f032522-91a5-40d5-a145-8b3c0d868b30" />

# Level 5

<p>Level 5 was in the alternative timeline branch ,enis lobby.This task was to run the python code and input both the poneygleph fragments together.It took me quite some time to understand that I had to put it together but after reading through the python code a few times and trying different combos i got the github link to level 6.</p>
<img width="1710" height="1107" alt="Screenshot 2026-07-29 at 12 58 38 AM" src="https://github.com/user-attachments/assets/988c2774-d3a4-4659-9ff8-ba48280e553e" />

# Level 6
 <p>Level 6 had a different repository so I first cloned it and it had two branches.The objective was to merge both of the treasure files without actually combining both of them.So first I merged the branches using git merge and got two merged text files.Then it got complicated when i used git mergetool and vimdiff to merge the files.But after two failed attempts i found out i an use vs code for the same purpose so i used vs code to get rid of the unwanted things and finally added and commited it to the repositary and then ran the file ,put in the password(TheGrandLineRemembers) and thats all.</p>
 <img width="1710" height="1076" alt="Screenshot 2026-07-29 at 2 21 39 AM" src="https://github.com/user-attachments/assets/4fe1da48-428e-402a-bd6e-d9d3651f1c34" />

 # My source of help and information 

[github docs](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/resolving-a-merge-conflict-using-the-command-line)
[Git](https://git-scm.com/)
[stack overflow](https://stackoverflow.com/questions/22424142/error-your-local-changes-to-the-following-files-would-be-overwritten-by-checkou)





