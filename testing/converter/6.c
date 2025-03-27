
int main(int argc, char** argv){
    int j = 2;
    for (int i=0; i<10; i++){
        j *= 2;
        if (j == 2){
            continue;
        }
    }
    return 0;
}
