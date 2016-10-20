CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -g

SRCS = src/test.c
OBJS = $(SRCS:.c=.o)


all: test

test: $(OBJS)
	gcc -o $@ $^ ${CFLAGS}
	
$(OBJS): $(SRCS)
	$(CC) -c $(CFLAGS) $< -o $@

clean:
	rm -f src/*.o
	rm -f test
