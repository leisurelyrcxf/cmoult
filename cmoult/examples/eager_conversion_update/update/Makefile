export LUMINATI_INCLUDE = $(CMOULT_PROJECT_HOME)/libuminati/include
export LUMINATI_LIB = $(CMOULT_PROJECT_HOME)/../_build/libuminati/lib
export CMOULT_INCLUDE = $(CMOULT_PROJECT_HOME)/cmoult/include
export CMOULT_LIB = $(CMOULT_PROJECT_HOME)/../_build/cmoult/lib

CC = gcc
CFLAGS = -fPIC -Wall -Wextra  -std=c99 -O2 -I$(LUMINATI_INCLUDE) -I$(CMOULT_INCLUDE) -Iinclude
LDFLAGSSHARED =  -L$(LUMINATI_LIB) -L$(CMOULT_LIB) -luminati -lcmoult -ldw -lelf -lpthread -shared
#LDFLAGSMAIN =  -L$(LUMINATI_LIB) -L$(CMOULT_LIB) -luminati -lcmoult -ldw -lelf -lpthread

RM = rm -f
TARGET_LIB = lib/libupdate.so

SRCDIR = src

SRCS := $(wildcard $(SRCDIR)/*.c)
OBJS = $(SRCS:.c=.o)

.PHONY: all

all: ${TARGET_LIB} 

$(TARGET_LIB): $(OBJS)
	$(CC) $(CFLAGS) $^ -o $@ ${LDFLAGSSHARED} 

$(OBJS) : $(SRCDIR)/%.o :$(SRCDIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: clean

clean:
	-${RM} ${TARGET_LIB} ${OBJS}
