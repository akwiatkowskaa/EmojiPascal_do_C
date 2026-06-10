program DemoRozszerzenia ;

// Stare: const
const
    MAX = 100 ;
    ETYKIETA = "demo" ;

// Ostateczne: enum + set
type
    Kolor = ( Czerwony , Zielony , Niebieski ) ;

// Stare + nowe: var (int, bool, string, tablica, real, char, record, enum, set)
var
    i : integer ;
    suma : integer ;
    ok : boolean ;
    tekst : string ;
    waga : real ;
    sr : real ;
    znak : char ;
    liczby : array ( 1 .. 3 ) of integer ;
    punkt : record begin
        x : integer ;
        y : integer ;
    end ;
    barwy : set of Kolor ;
    aktywny : Kolor ;

// Nowe: BYREF (var)
procedure Zwieksz ( var v : integer ) ;
begin
    v := v + 1 ;
end ;

// Stare: function + nowe: real
function Srednia ( a : integer ; b : integer ) : real ;
begin
    exit  ( a + b ) : real / 2.0 ;
end ;

begin
    // Stare: assign, wyrazenia, bool
    suma := 0 ;
    ok := true ;
    tekst := ETYKIETA ;
    znak := 'X' ;
    waga := 3.5 ;

    // Nowe: pola rekordu (.)
    punkt . x := 10 ;
    punkt . y := 20 ;

    // Stare: for + tablica
    for i := 1 to 3 do
        liczby ( i ) := i * 10 ;
        suma := suma + i * 10 ;

    // Nowe: CAST () — int na real przed dzieleniem
    waga :=  ( suma ) : real / 2.0 ;

    // Stare: while
    while ok and suma < MAX do
        Zwieksz ( suma ) ;

    // Stare: if
    if suma >= 50 then ok := true else ok := false ;

    // Stare: repeat-until
    repeat
        suma := suma - 1 ;
    until suma = 50 ;

    // Ostateczne: set — literał, suma zbiorów, IN
    barwy := [ Czerwony , Niebieski ] ;
    barwy := barwy + [ Zielony ] ;
    aktywny := Czerwony ;
    if Czerwony in barwy then ok := true else ok := false ;

    // Stare: case (także etykieta enum)
    case aktywny of
        Czerwony then suma := suma + 1 ;
        Zielony then suma := suma + 2 ;
        else suma := suma ;
    end ;

    case punkt . x of
        10 then punkt . y := punkt . y + 1 ;
        20 then punkt . y := punkt . y - 1 ;
        else punkt . y := 0 ;
    end ;

    // Stare: print (int, string, bool, real, char, record fields)
    writeln ( tekst ) ;
    writeln ( suma ) ;
    writeln ( ok ) ;
    writeln ( waga ) ;
    writeln ( znak ) ;
    writeln ( punkt . x ) ;
    writeln ( punkt . y ) ;
    writeln ( barwy ) ;
    writeln ( aktywny ) ;
    sr := Srednia ( punkt . x , punkt . y ) ;
    writeln ( sr ) ;
end .
