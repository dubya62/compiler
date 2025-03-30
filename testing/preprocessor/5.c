
#define TEST(a, b, ...) (a + b - __VA_ARGS__)

int main(int argc, char** argv){

    int a = TEST(1, 2, 3, 4, 5);

    return 0;
}
