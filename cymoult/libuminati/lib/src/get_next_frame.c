#include "get_next_frame.h"

um_frame* um_get_next_frame (um_frame* cur)
{
    return cur?cur->next:NULL;
}
