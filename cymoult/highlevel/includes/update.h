#include <stdlib.h>

typedef struct{
  char (*requirements)();
  char (*alterability)();
  void (*apply)();
  char (*over)();
  char applied;
}update;


