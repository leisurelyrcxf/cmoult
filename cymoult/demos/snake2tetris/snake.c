#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "functions.h"

gameConfig gc;
gameData gd;

int main(){
        //Start Game
        initGameConfig(&gc);
        initGameData(&gd,&gc);
        clearConsole();
        drawBoard(&gd);
        drawGamePanel(&gc,&gd);
        while(1){
                delayTurn(&gc);
                getDirection(&gd);
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
        return 0;
}
