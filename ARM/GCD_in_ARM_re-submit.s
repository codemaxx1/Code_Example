@By Nick Garrett
@ greatest common denominator
@
@
@	This re-submission incorperates a function which ensures that a devision by zero error does not occur, this function
@	  doubles as a zero and negative number filter for user input, as both of these inputs cause errors in the system.  
@
@
@ To use, run code, a prompt will ask for the first integer.  Please, no zero's, negatives, or decimals.  While there is an error checker
@   for the first two, there is no system checking that the numberentered is a whole number.
@ After entering your integers, the program will determine the smallest of the two, and take a copy of the number checking if it is a devisor
@   of both integers.  If it is, then that integer will be returned in an output to the user.  Otherwise, it will subtract one from that integer,
@      and check it again.  Recursively operating until eventually, it returns an answer, or an error message. (preferably the prior)
@
@






.data
@	variable deffinitions
var:	.word
info: .asciz "Please enter the first integer.  Please, no negative numbers, zeros, or decimals. \n"
infoo: .asciz "Please enter the second integer.  The same rules apply as for the prior.\n"
output: .asciz "The GCD of %d and %d is %d\n"
iteration: .asciz "the current iteratios is # %d\n"
which: .asciz "number %d is smaller\n "
zeroErrorTXT: .asciz "\n\nThe numbers you provided do not appear to have a common devisor.  This most likely means that one of the numbers provided was 0 or a negative.\n\n"
mod: .asciz "the modulus of %d and %d, is %d"
order: .asciz "the smaller number is %d the larger number is %d and the first devisor is %d \n"
base: .asciz "%d"
baseo: .asciz "%d"
.align 2


.global main
.global gcd

.func  main
main:
	@main function

	push {fp, lr}
	add fp,sp,#4
	sub sp, sp, #12
		@fp -8
		@fp -12
		@fp -16	

	@ load first variable
	ldr r0,=info
	bl printf

	@take user input for first var
	ldr r0,=base
	sub r1, fp,#8	 @#8 address of first int
	bl scanf

	@reuest second var
	ldr r0, =infoo
	bl printf

	@take user input for second var
	ldr r0,=baseo
	sub r1,fp,#12 	@#12 address for second int
	bl scanf

	@branch to function for computing GCD	
	bl gcd






	sub sp,fp,#16
	pop {fp,pc}
	.endfunc
	


.func gcd
gcd:


@for loop declaration
@enters the value 0 to fp#-20 as a placeholding value
sub sp,sp,#4 @fp #-20
mov r0,#0
str r0,[fp,#-20]

b for_loop_init


pop {fp,pc}

@for loop compare
for_loop_init:
@the next three lines I only kept as they have the addresses of the variables in an orderly system, so that I could reference them throughout the program without haveing to write them down somewhere
	ldr r0, [fp, #-20]@iteration
	ldr r1, [fp, #-8] @first number
	ldr r2, [fp, #-12] @second number

	sub sp,sp, #8	@opens -24, -28
	 @if the first is greater(second is less)
        ldr r0,[fp,#-8]
        ldr r1,[fp,#-12]
        cmp r0,r1
        ldrgt r1,[fp,#-12]      @if first is larger, run for second
        ldrle r1,[fp,#-8]       @if second is larger, run for first

	str r1, [fp,#-24]	@stores the smaller number



	@check that this is working r0 = text, r1 = smaller number
        ldr r0,=which
        bl printf


	ldr r1,[fp,#-24]@smaller number

	@make fp,-20 the smaller variable for iterations
	ldr r3,[fp,#-20]
	mov r3,r1
	add r3,r3,#1
	str r3,[fp,#-20]

	ldr r0,[fp,#-8]
	cmp r0,r1
	ldrgt r2, [fp,#-8]	@store larger number as r2
	ldrle r2,[fp,#-12]	@see above
	str r2,[fp,#-28]	@store the larger number
	ldr r2,[fp,#-28]
	
	ldr r0, =order
	bl printf


	
	b for_loop_comp
	sub sp,fp,#4	
.endfunc


@recursively check if the decreasing int at fp-20 is a GCD of both integers	
for_loop_comp:
@
	@check that the next iteration of fp,#-20 > 0
	@ also acts as a 0, negative number filter.  If the variable provided causes this error, it will branch back to the start of the program
	mov r0,#1
	ldr r1,[fp,#-20]
	cmp r0,r1
	bge ZeroError


	@next iterations, (subtract 1 from fp,-20)
	ldr r3,[fp,#-20]
	sub r3,r3,#1
	str r3,[fp,#-20]

	@check first variable if the iteration variable is a devisor
	ldr r1, [fp,#-20]
	ldr r0, [fp,#-24]
	bl __aeabi_idivmod
@	push {r0,r1, lr}
@	bl div	
@	pop {r0,r1, pc}

	mov r0,#0
	cmp r1,r0
	bne for_loop_comp


	@check second variable, test if the 'iteration' variable is a devisor 
	ldr r1,[fp,#-20]
	ldr r0,[fp,#-28]
	bl __aeabi_idivmod
@	push {r0,r1, lr}
@	bl div
@	pop {r0,r1, pc}

	mov r0,#0
	cmp r1,r0
	bne for_loop_comp


	@only if the iteration variable is a devisor of both vars, does the program end
	b end



@function called if the iterator passes one, mainly caused by either zero or a negative number being provided
@ouputs a text message and then branches back to the start of the program, giving the user another enter a proper number
.func ZeroError
ZeroError:
	ldr r0, =zeroErrorTXT
	bl printf
	b main
	
.endfunc



@function called when an integer is found to be a devisor of both entered numbers.
.func end
end:
	ldr r0, =output
	ldr r1,[fp,#-8]
	ldr r2,[fp,#-12]
	ldr r3, [fp,#-20]
	bl printf

	sub sp, fp, #28
.endfunc










@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@	experimental subtractive devision function	@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@lets just accept that there was an attempt.  An apparently poor attempt, but an attempt nevertheless.

.func div
div:
	pop {r0,r1, pc}
	@n/d	n%d
	@ldr r0,r0 @smaller number			@n
	@ldr r1,r1 @iterator for external function 	@d
	mov r2,#0 @iterator for this function
	b div_init	
div_init:
	@iterate r2 +=1;
	add r2,r2,#1
	
	@r3 = r0-r1
	sub r3,r0,r1
	
	
	@check if r3(n-d) < r0(n)
	@if r3>r0, run again
	@if r3<=r0, return a modulus and a dev
	cmp r3,r0
	bgt div_init	@r3>r0
	
	mov r0, r2	@div(function iterator)

	sub r4,r1,r3 @r4=r1-r3
	mov r1,	r4	@mod(r1-r3)
	
	
	push {r0,r1,lr}
	
	bx lr
	@.endfunc






