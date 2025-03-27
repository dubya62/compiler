
int main(int argc, char** argv){
    for (int i=0; i<10; --i){
        int* a = &i;
        *a++;
        i++;
        i *= 2;
    }
    return 0;
}
