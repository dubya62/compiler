
#define A \
    10 + 2
#define B(a,b) (a##b);

int main(int argc, char** argv){
    int a = A;
    char* x = B(2, 3);
    return 0;
}
