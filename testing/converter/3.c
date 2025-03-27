

int main(int argc, char** argv){
    int a = 2;

    switch(a){
        case 1:
            return 2;
        case 2:
            return 4;
        case 3:
        case 4:
            return 1;
        case 5:
            a = 1;
            break;
        case 6:
            break;
        default:
            a = 5;
    }

    int b = a == 1;
    if (b){
        return 2;
    } 
    b = b || (a == 2);
    if (b){
        return 4;
    }
    b = b || (a == 3);
    if (b){
    }
    b = b || (a == 4);
    if (b){
        return 1;
    }
    b = b || (a == 5);
    if (b){
        a = 1;
        goto end;
    }
    b = b || (a == 6);
    if (b){
        goto end;
    }
    if (!b){
        a = 5;
    }
    end:



}
