/* update.c This file is part of Cymoult */
/* Copyright (C) 2013 Sébastien Martinez, Fabien Dagnat, Jérémy Buisson */

/* This program is free software; you can redistribute it and/or modify */
/* it under the terms of the GNU General Public License as published by */
/* the Free Software Foundation; either version 2 of the License, or */
/* (at your option) any later version. */

/* This program is distributed in the hope that it will be useful, */
/* but WITHOUT ANY WARRANTY; without even the implied warranty of */
/* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the */
/* GNU General Public License for more details. */

/* You should have received a copy of the GNU General Public License along */
/* with this program; if not, write to the Free Software Foundation, Inc., */
/* 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA. */

/*

Basic update.

 */

#include "update.h"

/* Default empty update functions */


req_ans req_ans_empty_step(){
  return yes;
}

void void_empty_step(){
}

char char_empty_step(){
  return 1;
}



  
