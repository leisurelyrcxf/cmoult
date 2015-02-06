
typedef struct{
  char * name;
  char (*requirements)(void);
  char (*alterability)(void);
  void (*apply)(void);
  char (*over)(void);

} generic_update;

