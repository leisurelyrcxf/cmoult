#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "functions.h"

gameConfig gc;
gameData gd;


int main(int argc, char **argv){
        if(argc>1){
                if(strcmp(argv[1],"tetris")==0){
                //Start Game
                initGameConfig(&gc);
                initGameDataTetris(&gd,&gc);
                initTetrisForms(&gc);
                generateRandomForm(&gc,&gd);
                updateMapTetris(&gd);
                clearConsole();
                drawBoard(&gd);
                drawGamePanel(&gc,&gd);
                while(1){
                        delayTurn(&gc);
                        getDirectionTetris(&gc,&gd);
                        moveTetris(&gc,&gd);
                        clearConsole();
                        if(gd.lost == 0){
                                drawBoard(&gd);
                                drawGamePanel(&gc,&gd);
                        }
                        else{
                                drawLost(&gd);
                                exit(EXIT_SUCCESS);
                        }
                }

                }
        }else{
                //Start Game
                initGameConfig(&gc);
                initGameData(&gd,&gc);
                initTetrisForms(&gc);
                clearConsole();
                drawBoard(&gd);
                drawGamePanel(&gc,&gd);
                while(1){
                        delayTurn(&gc);
                        getDirection(&gc,&gd);
                        moveSnake(&gc,&gd);
                        clearConsole();
                        if(gd.lost == 0){
                                drawBoard(&gd);
                                drawGamePanel(&gc,&gd);
                        }
                        else{
                                drawLost(&gd);
                                exit(EXIT_SUCCESS);
                        }
                }
        }
        return 0;
}
