#include "functions.h"

void initGameConfig(gameConfig* gc){
        gc->height=15;
        gc->width=11;
        gc->timeDelay=1500;
}

void initGameData(gameData* gd,gameConfig* gc){
        gd->score=0;
        gd->map=(char **) calloc(gc->height,sizeof(char*));
        gd->mapData= (char *) calloc(gc->width*gc->height,sizeof(char));
        for(int i=0; i<gc->height*gc->width; i++){
                gd->mapData[i]=' ';
        }
        for(int i=0; i<gc->height; i++){
                gd->map[i] = &gd->mapData[i*gc->width];
        }
        gd->map[gc->height/2][gc->width/2]='*';
        gd->snakeSize=1;
        gd->snakeDirection=NORTH;
        gd->snakePositions=(int **) calloc(gd->snakeSize,sizeof(int*));
        gd->snakePositionsData= (int *) calloc(2*gd->snakeSize,sizeof(int));
        for(int i=0; i<gd->snakeSize; i++){
                gd->snakePositions[i] = &gd->snakePositionsData[i*2];
        }
        gd->snakePositions[0][0]=gc->height/2;
        gd->snakePositions[0][1]=gc->width/2;
        gd->lost=0;
        createRandomFruit(gc,gd);
}

void clearConsole(){
        printf("\e[H\e[2J");
}

void delayTurn(gameConfig* gc){
        usleep(gc->timeDelay*1000); //timeDelay in ms
}

void drawGamePanel(gameConfig* gc, gameData* gd){
        char* hBorder=malloc((2*(gc->width)+3)*sizeof(char));
        for(int i=0;i<(2*(gc->width)+3);i++){
                hBorder[i]='-';
        }
        printf("\t\t\t%s\n",hBorder);
        for(int i=0;i<gc->height;i++){
                printf("\t\t\t|");
                for(int j=0;j<gc->width;j++){
                        printf(" %c",gd->map[i][j]);
                }
                printf(" |\n");
        }
        printf("\t\t\t%s\n",hBorder);
}

void moveSnake(gameConfig* gc, gameData* gd){
        /* Check Direction */
        if((gd->snakeDirection==NORTH && gd->snakePositions[0][0]==0) || (gd->snakeDirection==SOUTH && gd->snakePositions[0][0]==(gc->height-1)) || (gd->snakeDirection==EAST && gd->snakePositions[0][1]==0) || (gd->snakeDirection==WEST && gd->snakePositions[0][1]==(gc->width-1))){
                gd->lost=1;
                return;
        }

        /* Find Next Head Position */
        int next[2] = {gd->snakePositions[0][0],gd->snakePositions[0][1]};
        switch(gd->snakeDirection){
                case NORTH:
                        next[0]-=1;
                        break;
                case SOUTH:
                        next[0]+=1;
                        break;
                case EAST:
                        next[1]-=1;
                        break;
                case WEST:
                        next[1]+=1;
                        break;
                default:
                        exit(EXIT_FAILURE);
                        break;
        }

        /* Check Next in Body */
        if(gd->map[next[0]][next[1]] == '*'){
                gd->lost=1;
                return;
        }

        /* Check Fruit */
        if(gd->map[next[0]][next[1]] == '@'){
                /* Copy and extends snake body */
                (gd->snakeSize)+=1;
                int** newSnakePositions=(int **) calloc(gd->snakeSize,sizeof(int*));
                int* newSnakePositionsData= (int *) calloc(2*gd->snakeSize,sizeof(int));
                for(int i=0; i<gd->snakeSize; i++){
                        newSnakePositions[i] = &newSnakePositionsData[i*2];
                }
                newSnakePositions[0][0]=next[0];
                newSnakePositions[0][1]=next[1];
                for(int j=1;j<gd->snakeSize;j++){
                        newSnakePositions[j][0]=gd->snakePositions[j-1][0];
                        newSnakePositions[j][1]=gd->snakePositions[j-1][1];
                }

                /* Free and Replace */
                free(gd->snakePositions);
                free(gd->snakePositionsData);
                gd->snakePositions=newSnakePositions;
                gd->snakePositionsData=newSnakePositionsData;

                /* Create fruit */
                createRandomFruit(gc,gd);

                /* Give points */
                gd->score+=10;

                /* Increase Speed (faster if > 800ms) */
                if(gc->timeDelay >800){
                        gc->timeDelay-=50;
                }
                if(gc->timeDelay >50){
                        gc->timeDelay-=50;
                }
        }
        else{
                /* Just move snake */
                for(int i=gd->snakeSize-1;i>0;i--){
                        gd->snakePositions[i][0]=gd->snakePositions[i-1][0];
                        gd->snakePositions[i][1]=gd->snakePositions[i-1][1];
                }
                gd->snakePositions[0][0]=next[0];
                gd->snakePositions[0][1]=next[1];
        }
        updateMap(gc,gd);
}

void createRandomFruit(gameConfig* gc, gameData* gd){
        srand(time(NULL));
        int fruit[2] = {rand() % gc->height,rand() % gc->width};
        if(gd->map[fruit[0]][fruit[1]] == '*' || gd->map[fruit[0]][fruit[1]] == '@'){
                createRandomFruit(gc,gd);
        }
        else{
                gd->map[fruit[0]][fruit[1]]='@';
        }
}

void updateMap(gameConfig *gc, gameData *gd){
        for(int i=0;i<gc->height*gc->width;i++){
                if( gd->mapData[i] == '*' )
                        gd->mapData[i] = ' ';                        
        }
        for(int i=0;i<gd->snakeSize;i++){
                gd->map[gd->snakePositions[i][0]][gd->snakePositions[i][1]] = '*';
        }
}

void drawBoard(gameData *gd){
        printf("\t\t\t*** SNAKE GAME ***\n");
        printf("\t\t\t- dorian.gilly@telecom-bretagne.eu -\n");
        printf("\t\t\tKeys:\n");
        printf("\t\t\t Z \n");
        printf("\t\t\tQSD\n");
        printf("\n\t\t\tScore: %d\n\n",gd->score);
}

void drawLost(gameData *gd){
        printf("\t\t\t*** SNAKE GAME ***\n");
        printf("\t\t\t- dorian.gilly@telecom-bretagne.eu -\n");
        printf("\n\t\t\tYOU LOST\n");
        printf("\n\t\t\tFinal Score: %d\n\n",gd->score);
}

void getDirection(gameData* gd){
        char input;
        int keyHit;
        if( (keyHit=kbhit()) >0 ){
                input=getch();
                switch(input){
                        case KEY_UP:
                                gd->snakeDirection = NORTH;
                                break;
                        case KEY_DOWN:
                                gd->snakeDirection = SOUTH;
                                break;
                        case KEY_LEFT:
                                gd->snakeDirection = EAST;
                                break;
                        case KEY_RIGHT:
                                gd->snakeDirection = WEST;
                                break;
                        default:
                                break;
                }
                if(keyHit>1)
                        getDirection(gd);
        }
}

char getch() {
        char buf = 0;
        struct termios old = {0};
        if (tcgetattr(0, &old) < 0)
                perror("tcsetattr()");
        old.c_lflag &= ~ICANON;
        old.c_lflag &= ~ECHO;
        old.c_cc[VMIN] = 1;
        old.c_cc[VTIME] = 0;
        if (tcsetattr(0, TCSANOW, &old) < 0)
                perror("tcsetattr ICANON");
        int count = read(0, &buf, 1);
        if(count < 0)
                perror ("read()");
        old.c_lflag |= ICANON;
        old.c_lflag |= ECHO;
        if (tcsetattr(0, TCSADRAIN, &old) < 0)
                perror ("tcsetattr ~ICANON");
        return (buf);
}

int kbhit() {
        int count = 0;
        struct termios otty, ntty;
        tcgetattr(STDIN_FILENO, &otty);
        ntty = otty;
        ntty.c_lflag &= ~ICANON;
        if(tcsetattr(STDIN_FILENO, TCSANOW, &ntty) == 0) {
                ioctl(STDIN_FILENO, FIONREAD, &count);
                tcsetattr(STDIN_FILENO, TCSANOW, &otty);
        }
        return count;
}
