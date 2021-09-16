#!/bin/bash
#
#       CTF (capture the flag) script to print a simply-encrypted string
#
#by Nick Garrett


a="hello CTF-ers. I hope that you are having fun..."

#array of encoded values
array=(21 15 26 20 28 7 19 18 8 27  18 8 27   2 12 6 9 27  15 26 8 7  27    24 19 26 13 24 22 27   26 21 7 22 9 27   7 19 18 8 27   7 19 22 9 22 27   18 8 27   13  12  27  7 6 9 13 18 13 20 27   25  26  24 16 27     2 12 6 27   7 26 16 22 27    7 19 22 27    25 15 6 22 27   11 18 15 15 27   7 19 22 27    8 7 12 9 2 27   22 13 23 8 27     2 12 6 27    4 26 16 22 27    6 11 27   18 13 27   2 12 6 9 27   25 22 23 27       26 9 23 27    25 22 15 18 22 5 22 27    4 19 26 7 27    22 5 22 9 27   2 12 6 27     4 26 14 7 27    7 12  27   25 22 15 18 22 5 22 27   2 12 6 27   7 26 16 22 27    7 19 22 27    9 22 23 27    11 18 15 15 27   2 12 6 27   8 7 26 2 27   18 13 27    4 12 13 23 22 9 15 26 13 23 27     26 13 23 27         18 27   8 19 12 4 27   2 12 6 27   19 12 4 27    23 22 22 11  27      7 19 22 27    9 26 25 25 18 7 27   19 12 15 22 27    20 12 22 8 29)

#simple map of what the values correlate to
letter=("z" "y" "x" "w" "v" "u" "t" "s" "r" "q" "p" "o" "n" "m" "l" "k" "j" "i" "h" "g" "f" 'e' "d" "c" "b" "a" "_" "{" "}")  

#print when the program has completed
b="program complete... Have a nice Day"

#print two (2) newlines
echo ""
echo ""

#print each of the letters in the array using a for loop
for i in ${!array[@]}; do
        #iterate through numbers
num=${array[$i]}
numm=($num-1)
        #print the letter
printf  ${letter[$numm]}
        #for loop completed
done


#print three (3) newlines
echo ""
echo ""
echo ""

#print to the user that the program is complete
echo $b

