
int add(int a, int b){
    return a + b;
}

int main(int argc, char** argv){
    int a = 2;
    while (a > 1){
        a += add(10, -5) - 2;
        a /= 2;
    }
    return 0;
}
