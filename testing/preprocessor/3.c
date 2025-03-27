#define TESTING
#ifdef TESTING
int add(int a, int b){
    return a + b;
}
#else
int mul(int a, int b){
    return a * b;
}
#endif
