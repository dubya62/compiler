
#define B 2
#define C 1 - 1
#define D(x, y) x##y

#if B == 2
int main(int argc, char** argv){
    #ifdef C
    int a = C;
    int b = D(2, 3);
    #else
    int a = 3;
    #endif
}
#else
int add(int x, int y){
    return x + y;
}
#endif
