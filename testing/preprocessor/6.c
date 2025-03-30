
#define DEBUG 6

#if defined(DEBUG)
    #define a 0
#else
    #define a DEBUG
#endif


int main(int argc, char** argv){
    int b = a;
    return 0;
}

