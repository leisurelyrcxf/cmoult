#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <string.h>
#include <termios.h>
#include <sys/ioctl.h>

/* Mappings */
#define KEY_UP 'z'
#define KEY_DOWN 's'
#define KEY_LEFT 'q'
#define KEY_RIGHT 'd'

#define NORTH 0
#define EAST 1
#define SOUTH 2
#define WEST 3

/* Game Infos */
typedef struct gameConfig{
        int height;
        int width;
        int timeDelay; //Unit is in ms
        
} gameConfig;

typedef struct gameData{
        int score;
        char **map;
        char *mapData;
        int snakeSize;
        int snakeDirection;
        int **snakePositions;
        int *snakePositionsData;
        int lost;
} gameData;

void initGameConfig(gameConfig* gc);
void initGameData(gameData* gd,gameConfig* gc);
void clearConsole();
void delayTurn(gameConfig* gc);
void drawGamePanel(gameConfig* gc, gameData* gd);
void moveSnake(gameConfig* gc, gameData* gd);
void createRandomFruit(gameConfig* gc, gameData* gd);
void updateMap(gameConfig *gc, gameData *gd);
void drawBoard(gameData *gd);
void drawLost(gameData *gd);
void getDirection(gameData* gd);
char getch();
int kbhit();
