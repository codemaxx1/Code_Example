#!/bin/bash

#       Nick Garrett
#       Project6.bash
#       4/16/2021


#copy file to file
cpf2f() 
{

        #if the source file doesn't exist
        # $1 does not exist
        if [ ! -e $1 ]; then
                echo no such source file $1
                return 1
        fi

        #if the source and destination files are the same
        if [ $1 -ef $2 ]; then
                echo "never copy a file to itself"
                return 1
        fi

        #copy
        if [ -L $1 ]; then
                echo "copying symlink $1"
                link=$(readlink $1)
                ln -s $link $2
                return 0
        fi

        echo "copying $1 to $2"
        cp $1 $2 2> /dev/null
}


#copy file to directory
cpf2d()
{
        newfile=$2/$(basename $1)
        cpf2f $1 $newfile
}



#return if the input is a file or a directory
fileOrDirectory()
{
        #create local variable for the directory and file location
        local location="$2/$(basename $1)" 

        #if the term is a file:
        if   [[ -f $location ]]; then
                echo "${location} is a file"
                return 1

        #if the term is a directory
        elif [[ -d $location ]]; then
                echo "${location} is a directory"
                return 2
                
        #if the location is neither
        else
                echo "${location} is not valid"
                return 0
                
        fi
}


# make a directory named <term 1> at location <term 2>
makeDirectory()
{
        mkdir $2/$(basename $1) $2
        echo "made directory $1 in $2"
}


# recursive function to go through all the files and directories in the sourceDirectory
iterateThroughTerms()
{
#find each of the files or directories in $1, which is the source directory
for location in $(ls $1)
        do
        # variable for the location
        directory=$(pwd)/$1
        echo "location: \"$location\" in \"$directory\""
        
        # is the location a file or a directory
        fileOrDirectory $location $directory
        fOrD=$?
        echo "fOrD: $fOrD"
        
        if [ $fOrD == 1 ];then
                echo "$location is a file"
                # copy the file
                cpf2f $1/$location $2
                fi
                
        if [ $fOrD == 2 ];then
                echo "$location is a directory"
                #make a new directory in the target location
                makeDirectory $location $2
                
                # recursive call
                iterateThroughTerms $1/$location $2/$location 
                fi

        done
}





# **************************** entry point of myrcp ******************************

# iterate through and print the terms
#iteration=0
#for command in $*
        #do
        #echo "term($iteration) = $command " 
        #iteration=$((iteration+1))
        #done
#echo " "

# recursive call
iterateThroughTerms $1 $2


