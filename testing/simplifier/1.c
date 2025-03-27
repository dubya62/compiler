
struct TestStruct{
    int a;
    int* b;
};

int(*mypointer)(int,int);

int main(int argc, char** argv){
    struct TestStruct testing;
    testing.a = 2;
    testing.b = &(testing.a);
    int* a[testing.a];
    a[1] = &(testing.a);
    return 0;
}
