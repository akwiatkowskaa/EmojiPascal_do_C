#include <stdio.h>

/* Program: SumaDoN */
int main(void) {
    int n;
    int i;
    int suma;
    
    printf("Podaj n: ");
    scanf("%d", &n);
    suma = 0;
    for (i = 1; i <= n; i++) {
        suma = (suma + i);
    }
    printf("Suma od 1 do n: ");
    printf("%d\n", suma);
    return 0;
}
