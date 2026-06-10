#include <stdio.h>

/* Program: DemoRozszerzenia */
typedef struct {
    int x;
    int y;
} Record_1;

#define MAX 100
#define ETYKIETA "demo"

void Zwieksz(int *v) {
    (*v) = ((*v) + 1);
}
double Srednia(int a, int b) {
    return (((double)(a + b)) / 2.0);
}

int main(void) {
    int i;
    int suma;
    int ok;
    char* tekst;
    double waga;
    double sr;
    char znak;
    int liczby[3];
    Record_1 punkt;
    
    suma = 0;
    ok = 1;
    tekst = ETYKIETA;
    znak = 'X';
    waga = 3.5;
    punkt.x = 10;
    punkt.y = 20;
    for (i = 1; i <= 3; i++) {
        liczby[(i - 1)] = (i * 10);
    }
    suma = (suma + (i * 10));
    waga = (((double)suma) / 2.0);
    while ((ok && (suma < MAX))) {
        Zwieksz(&suma);
    }
    if ((suma >= 50)) {
        ok = 1;
    } else {
        ok = 0;
    }
    do {
        suma = (suma - 1);
    } while (!((suma == 50)));
    switch (punkt.x) {
    case 10:
        punkt.y = (punkt.y + 1);
        break;
    case 20:
        punkt.y = (punkt.y - 1);
        break;
    default:
        punkt.y = 0;
        break;
    }
    printf("%s\n", tekst);
    printf("%d\n", suma);
    printf("%d\n", ok);
    printf("%lf\n", waga);
    printf("%c\n", znak);
    printf("%d\n", punkt.x);
    printf("%d\n", punkt.y);
    sr = Srednia(punkt.x, punkt.y);
    printf("%lf\n", sr);
    return 0;
}
