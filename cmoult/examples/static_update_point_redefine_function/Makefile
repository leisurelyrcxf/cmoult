export LUMINATI_INCLUDE = $(CMOULT_PROJECT_HOME)/libuminati/include
export LUMINATI_LIB = $(CMOULT_PROJECT_HOME)/../_build/libuminati/lib
export CMOULT_INCLUDE = $(CMOULT_PROJECT_HOME)/cmoult/include
export CMOULT_LIB = $(CMOULT_PROJECT_HOME)/../_build/cmoult/lib

CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -g -I$(LUMINATI_INCLUDE) -I$(CMOULT_INCLUDE) -Iinclude
LDFLAGS =  -L$(LUMINATI_LIB) -L$(CMOULT_LIB) -luminati -lcmoult -ldw -lelf -lpthread

SRCDIR = src

SRCS := $(wildcard $(SRCDIR)/*.c)
OBJS = $(SRCS:.c=.o)

TARGET = test

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $^ -o $@ ${LDFLAGS} 

$(OBJS) : $(SRCDIR)/%.o :$(SRCDIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)
	