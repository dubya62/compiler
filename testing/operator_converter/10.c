
#include <stdio.h>
struct TestStruct{
    int a;
};

int add(int a, int b){
    return a + b;
}

int main(int argc, char** argv){
    struct TestStruct test;

    while (1){
        break;
    }


    test.a = 2;

    int c = add(2, 3);
    printf("%d\n", c);

    return c;
}
