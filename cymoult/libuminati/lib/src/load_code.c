#include "load_code.h"

int um_load_code (um_data* dbg, const char* file_name) {
    if (!dbg || !file_name)
        return -1;
    bfd* file;
    asection *plt, *text, *got, *got_plt, *dynamic;
    //Initialize BFD
    bfd_init();
    file = bfd_openr(file_name, "default");
    if (!file)
        return 1;
    char** matching;
    if (!bfd_check_format_matches (file, bfd_object, &matching))
        bfd_perror("format");
    //Get relevant sections
    plt = bfd_get_section_by_name(file,".plt");
    if (!plt)
        return 2;
    text = bfd_get_section_by_name(file,".text");
    if (!text)
        return 2;
    got = bfd_get_section_by_name(file,".got");
    if (!got)
        return 2;
    got_plt = bfd_get_section_by_name(file,".got.plt");
    if (!got_plt)
        return 2;
    dynamic = bfd_get_section_by_name(file,".dynamic");
    if (!dynamic)
        return 2;
    //Allocate memory in the program
    uint64_t base_address = add_memory(dbg->pid, plt->size + text->size + got->size + got_plt->size + dynamic->size);
    if (base_address == 0 || base_address == 0xffffffffffffffff)
        return 6;
    //Get the dynamic symbol table for the file
    char *command = malloc(strlen(file_name) + 50), *symtab = malloc(20);
    sprintf(symtab, "/tmp/%d_dynsym", getpid());
    sprintf(command, "nm -D %s | grep \" T \" | sort > %s", file_name, symtab);
    system(command);
    free(command);
    FILE* fd = fopen(symtab, "r");
    if (!fd) {
        free(symtab);
        return 3;
    }
    char* buf = malloc(1024);
    function *prev = NULL, *last = dbg->injected, *func = NULL;
    if (last)
        while(last->next)
            last = last->next;
    //For each entry, calculate the final address and store the info in dbg->injected
    while (fgets(buf, 1024, fd)) {
        uint64_t address_in_so;
        char* function_name = malloc(1024);
        func = malloc(sizeof(function));
        if (sscanf(buf, "%lx T %s\n", &address_in_so, function_name) < 2) {
            free(function_name);
            free(func);
            func = NULL;
            continue;
        }
        func->name = function_name;
        func->lowpc = address_in_so - text->vma + plt->size + base_address;
        if (prev) {
            prev->highpc = func->lowpc;
            prev->next = func;
        } else if (last)
            last->next = func;
        else
            dbg->injected = func;
        prev = func;
    }
    if (func) {
        func->highpc = base_address + plt->size + text->size;
        func->next = NULL;
    }
    //Cleaning
    free(buf);
    fclose(fd);
    unlink(symtab);
    free(symtab);
    /******************.plt**************/
    //Fix .plt: edit references to the GOT (plt[0] : change bytes 3 to 6 and 9 to 12, others : change bytes 3 to 6)
    bfd_byte* plt_content;
    if(!bfd_malloc_and_get_section(file, plt, &plt_content))
        return 4;
    uint32_t new_target;
    //plt[0]: 2 jumps
    new_target = plt->size + text->size + got->size + 0x12;
    plt_content[2] = new_target & 0xff;
    plt_content[3] = (new_target >> 8) & 0xff;
    plt_content[4] = (new_target >> 16) & 0xff;
    plt_content[5] = new_target >> 24;
    new_target = plt->size + text->size + got->size + 0x14;
    plt_content[8] = new_target & 0xff;
    plt_content[9] = (new_target >> 8) & 0xff;
    plt_content[10] = (new_target >> 16) & 0xff;
    plt_content[11] = new_target >> 24;
    //plt[n]: 1 jump
    for (unsigned int i = 1; i < (plt->size >> 4); i++) {
        new_target = plt->size + text->size + got->size + 0x12 - 8*(i-1);
        plt_content[16*i + 2] = new_target & 0xff;
        plt_content[16*i + 3] = (new_target >> 8) & 0xff;
        plt_content[16*i + 4] = (new_target >> 16) & 0xff;
        plt_content[16*i + 5] = new_target >> 24;
    }
    //Write .plt in memory
    for (unsigned int i = 0; i < plt->size/4; i++) {
        uint32_t value = 0;
        for (int j = 0; j < 4; j++)
            value += (((uint32_t)plt_content[4*i+j]) << (8*j));
        if (_um_write_addr(dbg->pid, base_address + 4*i, value, 4) == -1)
            return 5;
    }
    free(plt_content);
    /******************.text**************/
    bfd_byte* text_content;
    if(!bfd_malloc_and_get_section(file, text, &text_content))
        return 4;
    for (unsigned int i = 0; i < text->size/4; i++) {
        uint32_t value = 0;
        for (int j = 0; j < 4; j++)
            value += (((uint32_t)text_content[4*i+j]) << (8*j));
        if (_um_write_addr(dbg->pid, base_address + plt->size + 4*i, value, 4) == -1)
            return 5;
    }
    for (unsigned int i = 4*(text->size/4); i < text->size; i++){
        if (_um_write_addr(dbg->pid, base_address + plt->size + i, text_content[i], 1) == -1)
            return 5;}
    free(text_content);
    /******************.got**************/
    bfd_byte* got_content;
    if(!bfd_malloc_and_get_section(file, got, &got_content))
        return 4;
    //Write .got in memory
    for (unsigned int i = 0; i < got->size/4; i++) {
        uint32_t value = 0;
        for (int j = 0; j < 4; j++)
            value += (((uint32_t)got_content[4*i+j]) << (8*j));
        if (_um_write_addr(dbg->pid, base_address + plt->size + text->size + 4*i, value, 4) == -1)
            return 5;
    }
    free(got_content);
    /******************.got.plt**************/
    bfd_byte* got_plt_content;
    if(!bfd_malloc_and_get_section(file, got_plt, &got_plt_content))
        return 4;
    //Fix .got.plt
    //First qword: address of .dynamic
    uint64_t dyn_addr = base_address + plt->size + text->size + got->size + got_plt->size;
    got_plt_content[0] = dyn_addr & 0xff;
    got_plt_content[1] = (dyn_addr >> 8) & 0xff;
    got_plt_content[2] = (dyn_addr >> 16) & 0xff;
    got_plt_content[3] = (dyn_addr >> 24) & 0xff;
    got_plt_content[4] = (dyn_addr >> 32) & 0xff;
    got_plt_content[5] = (dyn_addr >> 40) & 0xff;
    got_plt_content[6] = (dyn_addr >> 48) & 0xff;
    got_plt_content[7] = (dyn_addr >> 56);
    //TODO: From 4th qword: address to .plt after first jmp
    //Write .got.plt in memory
    for (unsigned int i = 0; i < got_plt->size/4; i++) {
        uint32_t value = 0;
        for (int j = 0; j < 8; j++)
            value += (((uint32_t)got_plt_content[4*i+j]) << (8*j));
        if (_um_write_addr(dbg->pid, base_address + plt->size + text->size + got->size + 4*i, value, 4) == -1)
            return 5;
    }
    free(got_plt_content);
    /******************.dynamic**************/
    bfd_byte* dynamic_content;
    if(!bfd_malloc_and_get_section(file, dynamic, &dynamic_content))
        return 4;
    for (unsigned int i = 0; i < dynamic->size/4; i++) {
        uint32_t value = 0;
        for (int j = 0; j < 8; j++)
            value += (((uint32_t)dynamic_content[4*i+j]) << (8*j));
        if (_um_write_addr(dbg->pid, base_address + plt->size + text->size + got->size + got_plt->size + 4*i, value, 4) == -1)
            return 5;
    }
    free(dynamic_content);
    return 0;
}
