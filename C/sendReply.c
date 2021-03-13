//

/*
sendReply.c

Nick Garrett
*/

#include <stdio.h>
#include <signal.h>
#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>  

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




//funtion to run as the "parent" thread
int parent()
{
        //signal that parent has started
        //  printf("\033[95mparent %d running\n", getpid());

        //infinite loop to write to ppipe and read from replyPipe
        while(1)
        {
                close(ppipe[0]); //parent = pipe writer
                printf("\033[95m\n\nCHECK STATUS PARENT: input a line : \033[0m\n");
                fgets(line, LEN, stdin);
                line[strlen(line) -1] = 0;  //kill "\n" at the end of the stirng
                //  printf("\033[95mparent %d write to pipe\033[0m\n", getpid());
                
                //write to the ppipe
                write(ppipe[1], line, LEN); //write to pipe
                
                //infinite loop to prevent the parent from doing anything until the child returns the properly replied string
                while(1){
                        close(replyPipe[1]);
                        //  printf("\033[95mCHECK STATUS PARENT: recieving...\033[0m\n");
                        read(replyPipe[0], replyLine, LEN);
                        printf("\033[95mCHECK STATUS PARENT: message recieved: %s\033[0m\n",replyLine);
                        
                        //generate a string "line" to be the initially sent line + "::REPLY"
                        strcpy(line, line);
                        strcat(line, "::REPLY");
                        //compare "line" and "replyLine"
                        if(!strcmp(line,replyLine))
                                printf("\033[95mCHECK STATUS PARENT: The child successfully sent the properly replied string: %s\033[0m\n",replyLine);
                                break;
                }
        }
}





//funtion run as the child process
int child()
{
        char msg[LEN];
        int parent = getppid();
        //  printf("child %d running \n", getpid());
       
        //infinite loop to read ppipe and write relayPipe
        while(1)
        {
                
                close(ppipe[1]);  //child is pipe reader
                //  printf("\033[37mCHECK STATUS CHILD: read ppipe  \033[0m\n");
                
                //read from the ppipe
                read(ppipe[0], line, LEN); //read pipe
                printf("\033[37mCHECK STATUS CHILD: child %d got a message = %s\033[0m\n", getpid(), line);
                
                //copy then append "::REPLY" to the read line
                strcpy(replyLine, line);
                strcat(replyLine, "::REPLY");
                
                //  printf("\033[37mCHECK STATUS CHILD: send reply: %s\033[0m\n",replyLine);
                close(replyPipe[0]);
                
                //[commented] sleep for 3 seconds to make sure that parent waits for the signal from replyPipe
                //sleep(3);
                //write the edited line to the replyPipe
                write(replyPipe[1], replyLine, LEN);
                
        }
        
}


//main function
int main ()
{
        //create the two pipes
        pipe(ppipe); // create the pipe
        pipe(replyPipe);
        
        pid = fork(); // fork a child process
        
        if(pid) 
        {
                // parent
                printf("\033[36mCHECK STATUS MAIN: starting Parent\033[0m\n");
                parent();
        }
        else
        {
                //chile
                printf("\033[36mCHECK STATUS MAIN: starting Child\033[0m\n");
                child();
        }
        
        //return -1 in case of failure
        return -1;
}


