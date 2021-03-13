//

/*
timeStamp.c

Nick Garrett
March 12 2021
*/

#include <stdio.h>
#include <signal.h>
#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>  
#include <time.h>
#define LEN 64

int ppipe[2]; //pipe descripttors 
int replyPipe[2];
int pid; //child pid
char line[LEN];
char replyLine[LEN];

int close(int fd);
ssize_t write(int fd, const void *buf, size_t count);
ssize_t read(int fd, void *buf, size_t count);
pid_t getppid(void);
struct timezone *tz;
int gettimeofday(struct timeval *tv, struct timezone *tz);
int atoi(const char *nptr);



//function to find the difference between the two times appended onto the replied String
long *timeDifference(char* replyLine)
{
        
        long    startHour, endHour, 
                startMinute, endMinute, 
                startSecond, endSecond, 
                startMillis, endMillis;  
                      
        double diff_t;

        //  printf("\033[34mCHECK STATUS TIMEDIFFERENCE: inputted string \"replyLine\"=\033[4m%s\033[0m\n",replyLine);
        
        int iteration = 0;
        char *p = strtok(replyLine, ":");
        int replyLineTokenized[8];
        
        //tokenize the string with ":" as the key
        while(p != NULL) {
                //  printf("\033[34mCHECK STATUS TIMEDIFFERENCE: string: %s \033[0m\n", p);
                
                int integerOfString = atoi(p);
                
                replyLineTokenized[iteration] = integerOfString;
                //  printf("\033[34mCHECK STATUS TIMEDIFFERENCE: integer: %d \t %d\033[0m\n", replyLineTokenized[iteration], iteration);
                p = strtok(NULL, ":");
                
                iteration++;   
        }
        
        //set the hour, minute, second, millisecond based on the order in which they appear in the replyLine string returned by the replyPipe
        startHour = (replyLineTokenized[iteration-8]);
        endHour = (replyLineTokenized[iteration-4]);
        startMinute = (replyLineTokenized[iteration-7]); 
        endMinute = (replyLineTokenized[iteration-3]); 
        startSecond = (replyLineTokenized[iteration-6]); 
        endSecond = (replyLineTokenized[iteration-2]); 
        startMillis = (replyLineTokenized[iteration-5]);
        endMillis = (replyLineTokenized[iteration-1]);          

        //compute the difference in time between the start and end
        static long differenceInTime[4];
        differenceInTime[0] = (endHour - startHour);
        differenceInTime[1] = (endMinute - startMinute);
        differenceInTime[2] = (endSecond - startSecond);
        differenceInTime[3] = (endMillis - startMillis);

        //print the difference between the hours, minutes, seconds, and milliseconds
          printf("\033[34mCHECK STATUS TIMEDIFFERENCE: differences:\n\tdiffernce in Hours:%ld\n\tdiffence in Minutes:%ld\n\tdifference in Seconds:%ld\n\tdifference in Milliseconds:%ld\033[0m\n",
                      differenceInTime[0],
                      differenceInTime[1],
                      differenceInTime[2],
                      differenceInTime[3]);
                        
        return differenceInTime;
} 


//function to find and return current time.
long *currentTime()
{
        
        struct timeval tp;
        gettimeofday(&tp, 0);
        time_t curtime = tp.tv_sec;
        
        static long timeArray[4];       
        long seconds, millis, hour, minutes;
        
        time_t current_time = time(NULL);
        struct tm *tm = localtime(&current_time);
        //  printf("\nCurrent Date and Time:\n");
        //  printf("%d\n", tm->tm_hour);
        
        //define the hour, minute, seconds, and milliseconds
        hour = (long) tm->tm_hour;
        minutes = (long) tm->tm_min;
        seconds = tm->tm_sec;
        millis = tp.tv_usec/1000;
        //  printf("\033[92mCHECK STATUS CURRENTTIME: hour:%ld\t\tminute:%ld\tseconds:%ld\tmillis:%ld\n", hour,minutes,seconds,millis);
        
        //define the different element's meanings
        timeArray[0] = hour;
        timeArray[1] = minutes;
        timeArray[2] = seconds;
        timeArray[3] = millis;
        
        return timeArray;
}


//funtion to run as the "parent" thread
int parent()
{
        //signal that parent has started
        //  printf("\033[95mCHECK STATUS PARENT: %d running\n", getpid());

        //infinite loop to write to ppipe and read from replyPipe
        while(1)
        {
       
                
                close(ppipe[0]); //parent = pipe writer
                printf("\033[95mCHECK STATUS PARENT: %d: input a line : \033[0m\n", getpid());
                fgets(line, LEN, stdin);
                line[strlen(line) -1] = 0;  //kill "\n" at the end of the stirng
                //  printf("\033[95mCHECK STATUS PARENT: %d write to pipe\033[0m\n", getpid());
                
                
                //write to the ppipe + timestamp
                long *currentTimeArray = currentTime();
                
                //define initial variables
                long hour = currentTimeArray[0];
                long minute = currentTimeArray[1];
                long second = currentTimeArray[2];
                long millis = currentTimeArray[3];
                
                //typecase the strings of hour, minute, second, millisecond to integer
                char hourString[LEN], minuteString[LEN], secondString[LEN], millisString[LEN];
                sprintf(hourString, "%d", (int) hour);
                sprintf(minuteString, "%d", (int) minute);
                sprintf(secondString, "%d", (int) second);
                sprintf(millisString, "%d", (int) millis);
                
                //append the hour, minute, seconds, milliseconds to the line to be written
                strcat(line, ":");
                strcat(line, hourString);
                strcat(line, ":");
                strcat(line, minuteString);
                strcat(line, ":");
                strcat(line, secondString);
                strcat(line, ":");
                strcat(line, millisString);
                
                
                
                write(ppipe[1], line, LEN); //write to pipe
                //  printf("\033[95mparent %d send signal 10 to %d\033[0m\n", getpid(), pid);
                
                

                //compare the times appended and determine the round trip
                close(replyPipe[1]);
                //  printf("\033[95mCHECK STATUS PARENT: recieving...\033[0m\n");
                read(replyPipe[0], replyLine, LEN);
                printf("\033[95mCHECK STATUS PARENT: message recieved: %s\033[0m\n",replyLine);
                
                long *differenceInTime = timeDifference(replyLine);
                
                //  printf("\033[95mCHECK STATUS PARENT: \n\tdiffernce in Hours:%ld\n\tdiffence in Minutes:%ld\n\tdifference in Seconds:%ld\n\tdifference in Milliseconds:%ld\033[0m\n",
                //      differenceInTime[0],
                //      differenceInTime[1],
                //      differenceInTime[2],
                //      differenceInTime[3]
                //      );
                //
                        
                
        }
}




//funtion run as the child process
int child()
{
        char msg[LEN];
        int parent = getppid();
        //  printf("CHECK STATUS CHILD  %d running \n", getpid());
        
        
        //infinite loop to read ppipe and write relayPipe
        while(1)
        {
                
                close(ppipe[1]);  //child is pipe reader
                //  printf("\033[37mCHECK STATUS CHILD: read ppipe  \033[0m\n");
                
                //read from the ppipe
                read(ppipe[0], line, LEN); //read pipe
                //  printf("\033[37mCHECK STATUS CHILD: child %d got a message = %s\033[0m\n", getpid(), line);
                
                //copy then append ":" to the read line--this is then going to be tokenized with ":" as the key to determine the difference in time.
                strcpy(replyLine, line);
                strcat(replyLine, ":");
                
                printf("\033[37mCHECK STATUS CHILD: send reply: %s\033[0m\n",replyLine);
                close(replyPipe[0]);
                
                //[commented] sleep for 3 seconds to make sure that parent waits for the signal from replyPipe
                //sleep(3);
                
                //write to the Repplypipe + timestamp
                long *currentTimeArray = currentTime();
                
                long hour = currentTimeArray[0];
                long minute = currentTimeArray[1];
                long second = currentTimeArray[2];
                long millis = currentTimeArray[3];
                
                //typecast the hour, minute, second, and milliseconds (returned as stirngs) and cast them to integers
                char hourString[LEN], minuteString[LEN], secondString[LEN], millisString[LEN];
                sprintf(hourString, "%d", (int) hour);
                sprintf(minuteString, "%d", (int) minute);
                sprintf(secondString, "%d", (int) second);
                sprintf(millisString, "%d", (int) millis);
                
                //append the hours, minutes, seconds, and milliseconds to the replyLine
                strcat(replyLine, hourString);
                strcat(replyLine, ":");
                strcat(replyLine, minuteString);
                strcat(replyLine, ":");
                strcat(replyLine, secondString);
                strcat(replyLine, ":");
                strcat(replyLine, millisString);
                
                //write the edited line to the replyPipe
                write(replyPipe[1], replyLine, LEN);
                
        }
        
}


//main function
int main ()
{
        //create the two pipes
        pipe(ppipe); // create the pipe ppipe
        pipe(replyPipe); // create the pipe replyPipe
        
        pid = fork(); // fork a child process
        
        if(pid) 
        {
                // parent
                printf("\033[33mCHECK STATUS MAIN: starting Parent\033[0m\n");
                parent();
        }
        else
        {
                //child
                printf("\033[33mCHECK STATUS MAIN: starting Child\033[0m\n");
                child();
        }
        
        //return -1 in case of failure
        return -1;
}


