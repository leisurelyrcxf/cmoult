#include "parse.h"

int um_count (Dwarf_Die* die, const char* parent_name, void* vargs, Dwarf_Addr bias)
  {
    um_count_args* args = vargs;
    if (dwarf_tag(die) != args->tag)
       return -1;
    if (args->name)
      {
        const char* die_name = dwarf_diename(die);
        if (!die_name)
            return -1;
        if (strcmp(args->name, die_name) != 0)
            return -1;
      }
    if (args->parent_name)
      {
        if (strcmp("*", args->parent_name) != 0)
          {
            if(!parent_name)
                return -1;
            if (strcmp(args->parent_name, parent_name) != 0)
                return -1;
          }
      }
    if (args->address)
        if (dwarf_haspc(die, args->address - bias) != 1)
            return -1;
    (args->result)++;
    return -1;
  }

int um_search_all (Dwarf_Die* die, const char* parent_name, void* vargs, Dwarf_Addr bias)
  {
    um_search_all_args* args = vargs;
    if (dwarf_tag(die) != args->tag)
        if ((dwarf_tag(die) != DW_TAG_variable && dwarf_tag(die) != DW_TAG_formal_parameter) || (args->tag != DW_TAG_variable && args->tag != DW_TAG_formal_parameter))
            return -1;
    if (args->name)
      {
        const char* die_name = dwarf_diename(die);
        if (!die_name)
            return -1;
        if (strcmp(args->name, die_name) != 0)
            return -1;
      }
    if (args->parent_name)
      {
        if (strcmp("*", args->parent_name) != 0)
          {
            if(!parent_name)
                return -1;
            if (strcmp(args->parent_name, parent_name) != 0)
                return -1;
          }
      }
    else
        if (parent_name)
            return -1;
    if (args->address)
        if (dwarf_haspc(die, args->address - bias) != 1)
            return -1;
    if (!dwarf_hasattr(die, args->wanted_attribute))
        return -1;
    Dwarf_Attribute wanted;
    dwarf_attr(die, args->wanted_attribute, &wanted);
    (args->n_results)++;
    Dwarf_Attribute *new_results = malloc((args->n_results)*sizeof(Dwarf_Attribute));
    for (int i = 0; i < (args->n_results)-1; i++)
        new_results[i] = (args->result)[i];
    new_results[(args->n_results)-1] = wanted;
    free(args->result);
    args->result = new_results;
    return 1;
  }

int um_search_first (Dwarf_Die* die, const char* parent_name, void* vargs, Dwarf_Addr bias)
  {
    um_search_first_args* args = vargs;
//    printf("tag %d, name %s, scope %s\n", dwarf_tag(die), dwarf_diename(die), parent_name);
    if (dwarf_tag(die) != args->tag)
        if ((dwarf_tag(die) != DW_TAG_variable && dwarf_tag(die) != DW_TAG_formal_parameter) || (args->tag != DW_TAG_variable && args->tag != DW_TAG_formal_parameter))
            return -1;
    if (args->name)
      {
        const char* die_name = dwarf_diename(die);
        if (!die_name)
            return -1;
        if (strcmp(args->name, die_name) != 0)
            return -1;
      }
    if (args->parent_name)
      {
        if (strcmp("*", args->parent_name) != 0)
          {
            if(!parent_name)
                return -1;
            if (strcmp(args->parent_name, parent_name) != 0)
                return -1;
          }
      }
    else
        if (parent_name)
            return -1;
    if (args->address)
        if (dwarf_haspc(die, args->address - bias) != 1)
            return -1;
    if (!dwarf_hasattr(die, args->wanted_attribute))
      {
        args->result = NULL;
        return -1;
      }

    int size = sizeof(Dwarf_Attribute);
    Dwarf_Attribute* wanted = malloc(sizeof(Dwarf_Attribute));
    Dwarf_Attribute* result;
    result = dwarf_attr(die, args->wanted_attribute, wanted);
    if(result == NULL){
      free(wanted);
      return -1;
    }
    args->result = result;
    return 0;
  }

int walk_tree (Dwarf_Die *cur_die, const char* parent_name, int (*callback) (Dwarf_Die*, const char*, void*, Dwarf_Addr), void* callback_args, Dwarf_Addr bias)
  {
    Dwarf_Die next;
    //Apply callback
    int child_result = -1, sibling_result = -1;
    int success = (*callback) (cur_die, parent_name, callback_args, bias);
    if (success == 0){
        return 0;
    }
    //Take care of the children
    int r = dwarf_child(cur_die, &next);
    if (r == 0)
      {
        child_result = walk_tree(&next, dwarf_diename(cur_die)?dwarf_diename(cur_die):parent_name, callback, callback_args, bias);
        if (child_result == 0)
            return 0;
      }
    //Take care of the siblings
    r = dwarf_siblingof(cur_die, &next);
    if (r == 0)
        sibling_result = walk_tree(&next, parent_name, callback, callback_args, bias);
        if (sibling_result == 0)
            return 0;
    return -1;
  }

int um_parse (um_data* dbg, int (*callback) (Dwarf_Die*, const char*, void*, Dwarf_Addr), void* callback_args)
  {
    Dwarf_Addr bias;
    Dwarf_Die *cu = NULL;
    int r = 0;

    while ((cu = dwfl_nextcu(dbg->debug_raw, cu, &bias)))
      {
        int tree_res = walk_tree(cu, NULL, callback, callback_args, bias);
//        printf("tree_res:%d\n", tree_res);
        if (tree_res == 0)
            return 1;
        if (tree_res == 1)
            r++;
      }

    return r;
  }

