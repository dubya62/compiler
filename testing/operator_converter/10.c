
struct TestStruct{
    int a;
};

int main(int argc, char** argv){
    struct TestStruct test;

    test->a = 2;
    return 0;
}
