
int main(int argc, char** argv){

    int i = 0;
    while (i < 10){
        int j = 1;
        i++;
        while (j > 5){
            j -= 2;
            continue;
            i += 5;
        }
        break;
    }

    return 0;

}
