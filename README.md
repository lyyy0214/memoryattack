# Minimal Docker Env for Buffer Overflow Test

## Intro

I followed the tutorial
[Part
1](https://blog.techorganic.com/2015/04/10/64-bit-linux-stack-smashing-tutorial-part-1/),[Part
2](https://blog.techorganic.com/2015/04/21/64-bit-linux-stack-smashing-tutorial-part-2/), and [Part
3](https://blog.techorganic.com/2016/03/18/64-bit-linux-stack-smashing-tutorial-part-3/). 
The exploitable code from the tutorials are
[stacksmash](./stacksmash). Associated tools and utilities
have been added to this repo and will be put into the image
once it is built with the docker build command. The one
thing that is dynamic is the location of the ENV variable
for the attack.

## Build Container

```bash
sudo docker build -t ndd/427hax .
```

## Launch The Container 

```bash
sudo docker run --privileged -it ndd/427hax /bin/bash
```

## Build attacks

Make the stacksmash directory.

## Build Input Files

You want to generate strings for input to overflow the buffer. These can be
generated by the [input/genvalidptrret.py](./input/genvalidptrret.py). Note that
this file doesn't generate the 400 A file or the 400 input patter with the BBBBB
at the 104 offset (I created in400A.txt and in400safe.txt for these in the repo
if you want). You can get that by modifying the script or looking at the blog
post. Also note that you need to find the right env location of the injected
shellcode before generating the workable input string that will transition
control properly.

## Constraints

Note that if you have security solutions turned on they will defeat your
attack. 

1. Address space layout randomization can be disabled by issuing the following
command: 

```bash
sudo sysctl -w kernel.randomize_va_space=0
```

But only if you've given proper authority to the conainter through privileged
creation with the `--privileged` flag. 

2. Do not do canary

3. Do not do non-executable stack

Please look at the stacksmash [Makefile](./stacksmash/Makefile) for how these
are generated.

## Lecture Sequence

I went through the sequence of operations as indicated in
[lecture](./lecture.md). This is somewhat a follow along with the blog post and
may be of interest.

## Useful Background

### Must Read

- [Smashing The Stack For Fun And Profit](http://phrack.org/issues/49/14.html#article)
- [Anatomy of a program in memory](https://manybutfinite.com/post/anatomy-of-a-program-in-memory/)

### Useful Info

- Eddie Kholer Background on
  [Assembly](https://cs61.seas.harvard.edu/site/2019/Asm/)
  and Low-Level Code:
  - [Assembly 1: Basics](https://cs61.seas.harvard.edu/site/2018/Asm1/)
  - [Assembly 2: Calling Convention](https://cs61.seas.harvard.edu/site/2018/Asm2/)
  - [Assebmly 4: Buffer Overflows](https://cs61.seas.harvard.edu/site/2018/Asm1/)
- Vasileios Kemerlis @ Brown on Hacking. Basically all the
  links from the first few lectures are useful:
  - [Course Website with Tons of Hacking Links](https://cs.brown.edu/courses/csci1650/lectures.html)

- [Program
  Startup](http://www.dbp-consulting.com/tutorials/debugging/linuxProgramStartup.html)

- [Heartbleed](https://readwrite.com/2014/04/13/heartbleed-security-codenomicon-discovery/)

### X86-64 Calling Convenctions

From [stack
overlow](https://stackoverflow.com/questions/28601414/calling-c-function-from-x64-assembly-with-registers-instead-of-stack):

> Passing arguments to variadic functions is more
> complicated. See x86-64 ELF ABI, section 3.5.7. Otherwise,
> x86-64 passes its first 6 arguments using registers: %rdi,
> %rsi, %rdx, %rcx, %r8, %r9 (excluding float / vector
> arguments).

> From the specification, %rax = 0 means that the variable
> argument list has no (0) floating-point arguments passed in
> vector registers. Your approach is wrong, as the first
> argument (e.g., the nul-terminated string: "Hello\n") must
> be passed in %rdi, and %rax must be zero when the function
> is called.
