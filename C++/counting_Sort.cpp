// created by Nicholas Garrett
/*
*
*
*
*/


//import libraries
#include <assert.h>
#include <iostream>     
#include <string>      
#include <ctime> 
#include <iostream>
#include <math.h>
#include <vector>

using namespace std;


//variables
unsigned long arraySize = 100;			// size of the array

unsigned long arrayRange = 10; 			// range of integers the array can hold.
	
unsigned long freqArraySize = pow(2, 32) - 1;


//create array
/*
	intput: unsigned long array, 
*/
void createZeroedArray(unsigned long* array, unsigned long arraySize)
{	
	cout << "\nzeroing array";
	
	for(unsigned long x = 0; x < arraySize; x++)
	{
		array[x] = 0;
	}
	cout << "\tzeroing completed\n";
} 


//randomize array
void randomizeArray(unsigned long* array, unsigned long arraySize)
{
	cout << "\nrandomize array values {";
	
	//print array
	for(int x = 0; x < arraySize; x++)
	{
		cout << array[x];
	}
	
	cout << "} to {";
	
	for(int x = 0; x < arraySize; x++)
	{
		array[x] = rand()%arrayRange;
		cout << array[x];
	}
	
	cout << "}\n";
}


//print array
void printArray(unsigned long* array, unsigned long arraySize)
{
	cout << "\nprint array: ";
	for(unsigned long x = 0; x < arraySize; x++)
	{
		cout << array[x] << " ";
	}
	cout << "printing complete\n";

}


// FooSort, sort an inputted array using the counting sort
/*
*	inputs:
*		unsortedArray, a 32-bit unsigned integer array
*		freqCountArray, a 32-bit unsigned integer array to hold the frequencies of values
*	return:
*		none
*/
void FooSort(unsigned long* unsortedArray, unsigned long* freqCountArray)
{
	//print a divising line
	cout << "\n\n";
	for(int x = 0; x < 50; x++)
	{
		cout << "=";
	}
	cout << "\nsorting algorithm started\n";
	
	// temporary variable to store what the i(th) value of unsorted array is
	unsigned long termValue;
	
	//iterate through all the terms in the array and count them,
	for(unsigned long x = 0; x < arraySize; x++)
	{
		termValue = unsortedArray[x];
		
		//increase the value of the relavent term in the frequncy count array that corresponds to the value of the xth term in the unsorted array
		freqCountArray[termValue]++;	
	}
	
	//print the frequency array
	cout << "\nfrequency array:";
	printArray(freqCountArray, arrayRange);
	
	
	//variable to store which term is being re-written in the unsorted array
	unsigned long termToReWrite = 0;
	
	// iterate through the freqCountArray[x][y] and itterate y terms of x to the unsortedArray[x] 
	for(unsigned long x = 0; x < arrayRange; x++)
	{
		//if the freqCountArray[x] is not 0 
		if(freqCountArray[x] != 0)
		{

			// iterate through the freqCountArray[x][y] and itterate y terms of x to the unsortedArray[x] 
			for(unsigned long y = 0; y < freqCountArray[x]; y++)
			{			
				unsortedArray[termToReWrite] = x;
				//iterate to overwrite the next term in the unsorted array
				termToReWrite++;
			}
		}		
	}
}



// main
int main()
{
	
	cout << "length of the frequency array: " << (unsigned long) freqArraySize << "\n";

	/*
	*	create the array to be sorted
	*/
	cout << "creating array to sort";
	unsigned long* array = new unsigned long[arraySize];
	
	//zero out the array, because the array is not cleared initially (the values will be overwritten by the randomization function, but it should be good for array data sanitization) 
	createZeroedArray(array, arraySize);
	
	//randomize the array
	randomizeArray(array, arraySize);
	
	//print the unsorted array
	printArray(array, arraySize);
	

	/*
	*	create the frequency count array
	*/
	unsigned long* freqCount = new unsigned long[freqArraySize];
	
	//zero out the frequency array
	createZeroedArray(freqCount, freqArraySize);
	
	//print freq array
	//printArray(freqCount, freqArraySize);
	
	
	/*
		run the sorting algorithm
	*/

	clock_t start = clock();	//start clock
	FooSort(array, freqCount);
	clock_t end = clock();	//end clock
	
	//print the (now)sorted array
	cout << "\nsorted aray: ";
	printArray(unsortedArray, arraySize);\
	
	cout << "speed: " << (double)(abs(start-end))/CLOCKS_PER_SEC << endl;
	
	/*
		delete arrays
	*/
	delete array;
	delete freqCount;
	
	// return a "success" value
	return 1;
}

