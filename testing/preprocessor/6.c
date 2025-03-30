
#define DEBUG 6

#if defined(DEBUGGING)
    #define a 0
#else
    #define a 1
#endif

#if DEBUG || 6 << 2 + 3
#endif


int main(int argc, char** argv){
    int b = a;
    return 0;
}

