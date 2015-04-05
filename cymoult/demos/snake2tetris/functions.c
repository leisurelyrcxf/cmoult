#include "functions.h"

void initGameConfig(gameConfig* gc){
        gc->height=15;
        gc->width=11;
        gc->timeDelay=1000;
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
        gd->currentBlock=NULL;
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

void getDirection(gameConfig* gc, gameData* gd){
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
                        getDirection(gc,gd);
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

/* To Tetris functions */

void initGameDataTetris(gameData* gd,gameConfig* gc){
        gd->score=0;
        gd->map=(char **) calloc(gc->height,sizeof(char*));
        gd->mapData= (char *) calloc(gc->width*gc->height,sizeof(char));
        for(int i=0; i<gc->height*gc->width; i++){
                gd->mapData[i]=' ';
        }
        for(int i=0; i<gc->height; i++){
                gd->map[i] = &gd->mapData[i*gc->width];
        }
        gd->lost=0;
}

void moveTetris(gameConfig* gc, gameData* gd){
        if(gd->currentBlock != NULL){
                /* Find next positions */
                int next[4][2];
                next[0][0]=((gd->currentBlock)->SWCoords[0])+1;
                next[0][1]=((gd->currentBlock)->SWCoords[1]);
                for(int i=1;i<4;i++){
                        next[i][0]=((gd->currentBlock)->form)->blocksPositions[(gd->currentBlock)->formDirection][i][0]+next[0][0];
                        next[i][1]=((gd->currentBlock)->form)->blocksPositions[(gd->currentBlock)->formDirection][i][1]+next[0][1];
                }

                /* Check possible */
                for(int i=0;i<4;i++){
                        if(next[i][0]>=gc->height){
                                blockStop(gc,gd);
                                return;
                        }
                        if((gd->map[next[i][0]][next[i][1]] == '*') && (checkIsInPreviousPosition(gd,next[i][0],next[i][1]) == 0)){
                                blockStop(gc,gd);
                                return;
                        }
                }

                /* If ok, move block */
                removeBlockMap(gd);
                ((gd->currentBlock)->SWCoords[0])=next[0][0];
                updateMapTetris(gd);
                clearConsole();
                drawBoard(gd);
                drawGamePanel(gc,gd);
        }
        else{
                /* Cheating : Should only happen on update */
                //blockStop(gc,gd);
        }
}

int checkIsInPreviousPosition(gameData *gd, int nextY, int nextX){
        /* Get positions */
        int block[4][2];
        block[0][0]=((gd->currentBlock)->SWCoords[0]);
        block[0][1]=((gd->currentBlock)->SWCoords[1]);
        for(int i=1;i<4;i++){
                block[i][0]=((gd->currentBlock)->form)->blocksPositions[(gd->currentBlock)->formDirection][i][0]+block[0][0];
                block[i][1]=((gd->currentBlock)->form)->blocksPositions[(gd->currentBlock)->formDirection][i][1]+block[0][1];
        }

        /* Check */
        for(int i=0;i<4;i++){
                if((block[i][0]==nextY) && (block[i][1] == nextX))
                        return 1;
        }
        return 0;
}

void blockStop(gameConfig *gc, gameData *gd){
        gd->currentBlock = NULL;
        for(int i=0;i<gc->height;i++){
                int count=0;
                for(int j=0;j<gc->width;j++){
                        if(gd->map[i][j]=='*')
                                count++;
                        else
                                break;
                }
                /* Line is full, delete and move all above ones */
                if(count==gc->width){
                        if(i==0){
                                for(int l=0;l<gc->width;l++){
                                        gd->map[0][l]=' ';
                                }
                        }else{
                                for(int k=i;k>0;k--){
                                        for(int l=0;l<gc->width;l++){
                                                gd->map[k][l]=gd->map[k-1][l];
                                        }
                                }
                        }
                        /* Grant points ! */
                        gd->score+=10;
                        /* And increase speed else it is not fun */
                        if(gc->timeDelay >800){
                                gc->timeDelay-=50;
                        }
                        if(gc->timeDelay >50){
                                gc->timeDelay-=50;
                        }

                }
        }
        generateRandomForm(gc,gd);
        /* Get positions */
        int block[4][2];
        block[0][0]=((gd->currentBlock)->SWCoords[0]);
        block[0][1]=((gd->currentBlock)->SWCoords[1]);
        for(int i=1;i<4;i++){
                block[i][0]=((gd->currentBlock)->form)->blocksPositions[(gd->currentBlock)->formDirection][i][0]+block[0][0];
                block[i][1]=((gd->currentBlock)->form)->blocksPositions[(gd->currentBlock)->formDirection][i][1]+block[0][1];
        }
        /* Check possible */
        for(int i=0;i<4;i++){
                if(gd->map[block[i][0]][block[i][1]] == '*'){
                        gd->lost=1; 
                        return;
                }
        }
        /* Refresh screen */
        updateMapTetris(gd);
        clearConsole();
        drawBoard(gd);
        drawGamePanel(gc,gd);
}

void shiftTetris(gameConfig* gc, gameData *gd, int dir){
        if(gd->currentBlock == NULL)
                return;

        /* Find next positions */
        int next[4][2];
        next[0][0]=((gd->currentBlock)->SWCoords[0]);
        if(dir==EAST){
                next[0][1]=((gd->currentBlock)->SWCoords[1])+1;
        }
        else if(dir==WEST){
                next[0][1]=((gd->currentBlock)->SWCoords[1])-1;
        }
        else{
                exit(EXIT_FAILURE);
        }
        for(int i=1;i<4;i++){
                next[i][0]=((gd->currentBlock)->form)->blocksPositions[(gd->currentBlock)->formDirection][i][0]+next[0][0];
                next[i][1]=((gd->currentBlock)->form)->blocksPositions[(gd->currentBlock)->formDirection][i][1]+next[0][1];
        }

        /* Check possible */
        for(int i=0;i<4;i++){
                if(next[i][0] <0 || next[i][0]>=gc->height || next[i][1]<0 || next[i][1]>= gc->width)
                        return;
                if((gd->map[next[i][0]][next[i][1]] == '*') && (checkIsInPreviousPosition(gd,next[i][0],next[i][1]) == 0))
                        return;
        }

        /* If ok, move block */
        removeBlockMap(gd);
        ((gd->currentBlock)->SWCoords[1])=next[0][1];
        updateMapTetris(gd);
        clearConsole();
        drawBoard(gd);
        drawGamePanel(gc,gd);
}

void getDirectionTetris(gameConfig* gc, gameData* gd){
        char input;
        int keyHit;
        if( (keyHit=kbhit()) >0 ){
                input=getch();
                switch(input){
                        case KEY_LEFT:
                                shiftTetris(gc,gd,WEST);
                                break;
                        case KEY_RIGHT:
                                shiftTetris(gc,gd,EAST);
                                break;
                        case KEY_ROT:
                                rotForm(gc,gd);
                                break;
                        default:
                                break;
                }
                if(keyHit>1)
                        getDirectionTetris(gc,gd);
        }
}
void generateRandomForm(gameConfig* gc, gameData* gd){
        srand(time(NULL));
        tetrisBlocks* newBlock = (tetrisBlocks *) malloc(sizeof(tetrisBlocks));
        newBlock->form=&(gc->forms[rand() % 7]);
        newBlock->formDirection=0;
        newBlock->SWCoords[0]=1;
        newBlock->SWCoords[1]=gc->width/2-1;
        gd->currentBlock=newBlock;
}
void rotForm(gameConfig *gc, gameData *gd){
        if(gd->currentBlock == NULL)
                return;

        /* Find next positions */
        int next[4][2];
        next[0][0]=((gd->currentBlock)->SWCoords[0]);
        next[0][1]=((gd->currentBlock)->SWCoords[1]);
        for(int i=1;i<4;i++){
                next[i][0]=((gd->currentBlock)->form)->blocksPositions[((((gd->currentBlock)->formDirection)+1)%4)][i][0]+next[0][0];
                next[i][1]=((gd->currentBlock)->form)->blocksPositions[((((gd->currentBlock)->formDirection)+1)%4)][i][1]+next[0][1];
        }

        /* Check possible */
        for(int i=0;i<4;i++){
                if(next[i][0] <0 || next[i][0]>=gc->height || next[i][1]<0 || next[i][1]>= gc->width)
                        return;
                if((gd->map[next[i][0]][next[i][1]] == '*') && (checkIsInPreviousPosition(gd,next[i][0],next[i][1]) == 0))
                        return;
        }

        /* If ok, move block */
        removeBlockMap(gd);
        (gd->currentBlock)->formDirection=((((gd->currentBlock)->formDirection)+1)%4);
        updateMapTetris(gd);
        clearConsole();
        drawBoard(gd);
        drawGamePanel(gc,gd);
}

void removeBlockMap(gameData *gd){
        /* Get positions */
        int block[4][2];
        block[0][0]=((gd->currentBlock)->SWCoords[0]);
        block[0][1]=((gd->currentBlock)->SWCoords[1]);
        for(int i=1;i<4;i++){
                block[i][0]=((gd->currentBlock)->form)->blocksPositions[(gd->currentBlock)->formDirection][i][0]+block[0][0];
                block[i][1]=((gd->currentBlock)->form)->blocksPositions[(gd->currentBlock)->formDirection][i][1]+block[0][1];
        }
        /* Remove from map */
        for(int i=0;i<4;i++){
                gd->map[block[i][0]][block[i][1]]= ' ';
        }
}

void updateMapTetris(gameData *gd){
        /* Get positions */
        int block[4][2];
        block[0][0]=((gd->currentBlock)->SWCoords[0]);
        block[0][1]=((gd->currentBlock)->SWCoords[1]);
        for(int i=1;i<4;i++){
                block[i][0]=((gd->currentBlock)->form)->blocksPositions[(gd->currentBlock)->formDirection][i][0]+block[0][0];
                block[i][1]=((gd->currentBlock)->form)->blocksPositions[(gd->currentBlock)->formDirection][i][1]+block[0][1];
        }
        /* Print on map */
        for(int i=0;i<4;i++){
                gd->map[block[i][0]][block[i][1]]= '*';
        }

}

void initTetrisForms(gameConfig *gc){
        /* triangle */
        int triangle[4][4][2] = {
                { {0,0},{0,1},{0,2},{-1,1} },
                { {0,0},{-1,0},{-2,0},{-1,1} },
                { {0,0},{-1,-1},{-1,0},{-1,1} },
                { {0,0},{-1,0},{-2,0},{-1,-1} }
        };
        /* line pizz */
        int line[4][4][2] = {
                { {0,0},{0,1},{0,2},{0,3} },
                { {0,0},{-1,0},{-2,0},{-3,0} },
                { {0,0},{0,1},{0,2},{0,3} },
                { {0,0},{-1,0},{-2,0},{-3,0} }
        };
        /* z */
        int z[4][4][2] = {
                { {0,0},{0,1},{-1,-1},{-1,0} },
                { {0,0},{-1,0},{-1,1},{-2,1} },
                { {0,0},{0,1},{-1,-1},{-1,0} },
                { {0,0},{-1,0},{-1,1},{-2,1} }
        };
        /* inversed z */
        int invz[4][4][2] = {
                { {0,0},{0,1},{-1,1},{-1,2} },
                { {0,0},{-1,0},{-1,-1},{-2,-1} },
                { {0,0},{0,1},{-1,1},{-1,2} },
                { {0,0},{-1,0},{-1,-1},{-2,-1} }
        };
        /* L */
        int L[4][4][2] = {
                { {0,0},{0,1},{0,2},{-1,2} },
                { {0,0},{0,1},{-1,0},{-2,0} },
                { {0,0},{-1,0},{-1,1},{-1,2} },
                { {0,0},{-1,0},{-2,0},{-2,-1} }
        };
        /* inversed L */
        int invL[4][4][2] = {
                { {0,0},{-1,0},{-1,-1},{-1,-2} },
                { {0,0},{0,1},{-1,1},{-2,1} },
                { {0,0},{0,1},{0,2},{-1,0} },
                { {0,0},{-1,0},{-2,0},{-2,1} }
        };
        /* square */
        int square[4][4][2] = {
                { {0,0},{0,1},{-1,0},{-1,1} },
                { {0,0},{0,1},{-1,0},{-1,1} },
                { {0,0},{0,1},{-1,0},{-1,1} },
                { {0,0},{0,1},{-1,0},{-1,1} }
        };
        /* TODO: temporar */
        memcpy((gc->forms[0]).blocksPositions,triangle,sizeof(int[4][4][2]));
        memcpy((gc->forms[1]).blocksPositions,line,sizeof(int[4][4][2]));
        memcpy((gc->forms[2]).blocksPositions,z,sizeof(int[4][4][2]));
        memcpy((gc->forms[3]).blocksPositions,invz,sizeof(int[4][4][2]));
        memcpy((gc->forms[4]).blocksPositions,L,sizeof(int[4][4][2]));
        memcpy((gc->forms[5]).blocksPositions,invL,sizeof(int[4][4][2]));
        memcpy((gc->forms[6]).blocksPositions,square,sizeof(int[4][4][2]));
}
