
int pow(int x, int n){
    int result = 1;
    for (int i=0; i<n; i++){
        result *= x;
    }
    return result;
}
