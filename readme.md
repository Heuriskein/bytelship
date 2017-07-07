

# Rules

## Overview

The game is played on a set of 4096 cells. Each cell contains an instruction for a custom VM. The cells are initialized to all contain the 'crash' instruction. Your program will be loaded at a random location in this memory space and begin executing. Another program will simultaneously be loaded into the memory space and *also* begin executing. The goal is to cause the other program to crash before it causes you to crash. There are two ways for a program to crash. It can either execute a 'crash' instruction, or it can execute off the end of the memory space.

## Registers
Each executor has some private memory locations called *registers*. These can only be seen by your executor and can only be written to by your executor. They are:
* i - Contains the address of the next instruction that will be executed. Note that on a given turn, this register is incremented *before* the instruction is executed. Writable.
* a - Arbitrary storage register. Can contain a single 12-bit integer. Initialized to 0. Writable.
* b - Arbitrary storage register. Can contain a single 12-bit integer. Initialized to 0. Writable.

## Instructions

The following instructions can be stored in a cell:

* crash - Causes the game to end and the executing player to lose. If both players execute a crash instruction on the same turn, the game is a draw.
* noop - Has no effect
* write [instruction] [address] - Sets the cell at the given address to contain the given instruction
 * May not contain a write instruction.
 * Attempting to write off the end of the memory space does *not* crash you, the memory space wraps. This is different from the way that the instruction pointer behaves.
* store [value] [register] - Sets the given register to the given 12-bit integer

## Input
You program your executor by feeding it a file containing at least 1 instruction and up to 128 instructions, one instruction per line (may be \n\r or \n delimited). So for example, the simplest program possible:

    store [i]-1 i

This program simply overwrites its instruction register with its previous value, forever looping. 

Here's a slightly more interesting program:

    write crash [i]+[a]+4 
    write crash [i]+[a]+4
    store [a]+2 a
    store [i]-4 i

This program simply starts immediately following its code and begins writing 'crash' instructions over all the memory after it, hoping to overwrite the other player's program.

If you pitted these two programs against each other, the second program would win because the first one will just wait forever.

## Turn structure

The execution of a turn goes like this:

1. Read the instruction from the cell referenced by executor 1's i register.
1. Read the instruction from the cell referenced by executor 2's i register.
1. Increment executor 1's i register.
1. Increment executor 2's i register.
1. Execute executor 1's instruction.
1. Execute executor 2's instruction.
1. Check for victory/draw

Note that this means that if you overwrite the instruction the other player is executing this turn *or yourself* with a 'crash' instruction, that will not be executed.

## Bootstrapping

At the start of the game, both players have their programs loaded into memory at random addresses. You are guaranteed that:
 * Your program will fit before the end of the memory space
 * Your program will not overwrite the other player's program
 * Your i register will be initialized to the address of the first instruction in your program.

## Syntax

    instr = <crash_instr> | <noop_instr> | <write_instr> | <store_instr> 
    crash_instr ::= 'crash'
    noop_instr ::= 'noop'
    write_instr ::= 'write' <crash_instr> <value_expr>
                | 'write' <noop_instr> <value_expr>
                | 'write' <store_instr> <value_expr>
    store_instr ::= 'store' <value_expr> <register_name>
    value_expr ::= <term>
                | <value_expr><operator><term>
    register_name ::= 'i' | 'a' | 'b'
    term ::= '['<register_name>']'
                | '['<number>']'
                | <number>
    operator ::= '+' | '-'

The [] syntax means *value at* or *dereference*, number is a 12-bit decimal number. Note that there are no spaces inside expressions.

## Draws

The game is a draw if both players execute a crash instruction on the same turn, or if both players' i registers contain the same value at the end of a turn.