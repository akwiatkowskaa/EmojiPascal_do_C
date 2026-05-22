#include <stdio.h>

/* Program: NajwiekszyWspolnyDzielnik */
int main(void) {
    int a;
    int b;
    int temp;
    
    printf("Podaj pierwsza liczbe: ");
    scanf("%d", &a);
    printf("Podaj druga liczbe: ");
    scanf("%d", &b);
    while ((b != 0)) {
        temp = b;
        b = (a % b);
        a = temp;
    }
    printf("Najwiekszy wspolny dzielnik to: ");
    printf("%d\n", a);
    return 0;
}
