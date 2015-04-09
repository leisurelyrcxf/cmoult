#include "load_code.h"

int _write_section_at_addr (pid_t pid, asection* sect, bfd_byte* sect_content, uint64_t base_addr) {
    for (unsigned int i = 0; i < sect->size/4; i++) {
        uint32_t value = 0;
        for (int j = 0; j < 8; j++)
            value += (((uint32_t)sect_content[4*i+j]) << (8*j));
        if (_um_write_addr(pid, base_addr + 4*i, value, 4) == -1)
            return -1;
    }
    for (unsigned int i = 4*(sect->size/4); i < sect->size; i++){
        if (_um_write_addr(pid, base_addr + i, sect_content[i], 1) == -1)
            return -1;
    }
    return 0;
}

int um_load_code (um_data* dbg, const char* file_name) {
    if (!dbg || !file_name)
        return -1;
    bfd* file;
    asection *plt, *text, *got, *got_plt, *dynamic, *dynsym, *dynstr;
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
    dynsym = bfd_get_section_by_name(file,".dynsym");
    if (!dynsym)
        return 2;
    dynstr = bfd_get_section_by_name(file,".dynstr");
    if (!dynstr)
        return 2;
    //Allocate memory in the program
    uint64_t base_address = add_memory(dbg->pid, plt->size + text->size + got->size + got_plt->size + dynamic->size + dynsym->size + dynstr->size);
    if (base_address == 0 || base_address == 0xffffffffffffffff)
        return 6;
    printf("DEBUG: Loading %d bytes at 0x%lx\n", plt->size + text->size + got->size + got_plt->size + dynamic->size + dynsym->size + dynstr->size, base_address);
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
        printf("DEBUG: %s at 0x%lx", func->name, func->lowpc);
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
    if (_write_section_at_addr(dbg->pid, plt, plt_content, base_address))
        return 5;
    free(plt_content);
    /******************.text**************/
    bfd_byte* text_content;
    if(!bfd_malloc_and_get_section(file, text, &text_content))
        return 4;
    if (_write_section_at_addr(dbg->pid, text, text_content, base_address + plt->size))
        return 5;
    free(text_content);
    /******************.got**************/
    bfd_byte* got_content;
    if(!bfd_malloc_and_get_section(file, got, &got_content))
        return 4;
    //Write .got in memory
    if (_write_section_at_addr(dbg->pid, got, got_content, base_address + plt->size + text->size))
        return 5;
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
    //From 4th qword: address to .plt after first jmp
    for (unsigned int i = 1; i < (plt->size >> 4); i++) {
        uint64_t plt_target = base_address + 16*i + 6;
        int tmp = 8*(i+2);
        got_plt_content[tmp] = plt_target & 0xff;
        got_plt_content[tmp + 1] = (plt_target >> 8) & 0xff;
        got_plt_content[tmp + 2] = (plt_target >> 16) & 0xff;
        got_plt_content[tmp + 3] = (plt_target >> 24) & 0xff;
        got_plt_content[tmp + 4] = (plt_target >> 32) & 0xff;
        got_plt_content[tmp + 5] = (plt_target >> 40) & 0xff;
        got_plt_content[tmp + 6] = (plt_target >> 48) & 0xff;
        got_plt_content[tmp + 7] = plt_target >> 56;
    }
    //Write .got.plt in memory
    if (_write_section_at_addr(dbg->pid, got_plt, got_plt_content, base_address + plt->size + text->size + got->size))
        return 5;
    free(got_plt_content);
    /******************.dynamic**************/
    bfd_byte* dynamic_content;
    if(!bfd_malloc_and_get_section(file, dynamic, &dynamic_content))
        return 4;
    if (_write_section_at_addr(dbg->pid, dynamic, dynamic_content, base_address + plt->size + text->size + got->size + got_plt->size))
        return 5;
    free(dynamic_content);
    /******************.dynsym**************/
    bfd_byte* dynsym_content;
    if(!bfd_malloc_and_get_section(file, dynsym, &dynsym_content))
        return 4;
    if (_write_section_at_addr(dbg->pid, dynsym, dynsym_content, base_address + plt->size + text->size + got->size + got_plt->size + dynamic->size))
        return 5;
    free(dynsym_content);
    /******************.dynstr**************/
    bfd_byte* dynstr_content;
    if(!bfd_malloc_and_get_section(file, dynstr, &dynstr_content))
        return 4;
    if (_write_section_at_addr(dbg->pid, dynstr, dynstr_content, base_address + plt->size + text->size + got->size + got_plt->size + dynamic->size + dynsym->size))
        return 5;
    free(dynstr_content);
    return 0;
}
