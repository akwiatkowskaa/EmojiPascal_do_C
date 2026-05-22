#include <stdio.h>

/* Program: TestGramatyki */
#define LIMIT 10

void WypiszInfo(char* txt) {
    printf("%s\n", txt);
}
int CzyDodatnia(int x) {
    if ((x > 0)) {
        return 1;
    } else {
        return 0;
    }
}

int main(void) {
    int i;
    int suma;
    int ok;
    int arr[5];
    
    suma = 0;
    ok = 1;
    for (i = 1; i <= 5; i++) {
        arr[(i - 1)] = (i * 2);
    }
    while ((ok && (!0))) {
        suma = (suma + 1);
        if ((suma >= LIMIT)) {
            ok = 0;
        }
    }
    do {
        suma = (suma - 1);
    } while (!((suma == 0)));
    switch (2) {
    case 1:
        printf("jeden");
        break;
    case 2:
    case 3:
        printf("dwa albo trzy");
        break;
    default:
        printf("inne");
        break;
    }
    WypiszInfo("Koniec testu");
    return 0;
}
