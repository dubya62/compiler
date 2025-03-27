
int a = 2;

int add(int a, int b);

int mul(int a, int b){
    return a * b;
}

int add(int a, int b){
    return a + b;
}


int main(int argc, char** argv){
    int d = add(2, 4);
    int e = mul(add(2, 3), d);

    char* test = "Hello, world\n";

    return add(e, 1);
}
