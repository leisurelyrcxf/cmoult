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

#define KEY_ROT 'r'

#define NORTH 0
#define EAST 1
#define SOUTH 2
#define WEST 3

/* Tetris structs */
typedef struct tetrisForm{
        int blocksPositions[4][4][2]; //4 directions, 4 blocks, 2 coords && First block is SW block.
} tetrisForm;

typedef struct tetrisBlocks{
        tetrisForm* form;
        int formDirection;
        int SWCoords[2];
} tetrisBlocks;

/* Snake Infos */
typedef struct gameConfig{
        int height; //>1
        int width;  //>2
        int timeDelay; //Unit is in ms
        /* Tetris gc */        
        tetrisForm forms[7];
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
        /* Tetris gd */
        tetrisBlocks* currentBlock;
} gameData;

/* Snake functions */
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
void getDirection(gameConfig *gc, gameData* gd);
char getch();
int kbhit();

/* To Tetris functions */
void initGameDataTetris(gameData* gd,gameConfig* gc);
void moveTetris(gameConfig* gc, gameData *gd);
int checkIsInPreviousPosition(gameData *gd, int nextY, int nextX);
void blockStop(gameConfig *gc, gameData *gd);
void shiftTetris(gameConfig* gc, gameData *gd, int dir);
void getDirectionTetris(gameConfig* gc, gameData* gd);
void generateRandomForm(gameConfig* gc, gameData* gd);
void rotForm(gameConfig *gc, gameData *gd);
void removeBlockMap(gameData *gd);
void updateMapTetris(gameData *gd);
void initTetrisForms(gameConfig *gc);
