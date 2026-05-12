program TestGramatyki ;

// [ETAP] DECLARACJE: const + var
const
    LIMIT = 10 ;

var
    i : integer ;
    suma : integer ;
    ok : boolean ;
    arr : array ( 1 .. 5 ) of integer ;

// [ETAP] PODPROGRAMY: procedure + function
procedure WypiszInfo ( txt : string ) ;
begin
    // [ETAP] INSTRUKCJA: print + procedure call z argumentem
    writeln ( txt ) ;
end ;

function CzyDodatnia ( x : integer ) : boolean ;
begin
    // [ETAP] STEROWANIE + BOOL: relacja i return
    if x > 0 then exit true else exit false ;
end ;

begin
    // [ETAP] ASSIGN + WYRAZENIA MATEMATYCZNE
    suma := 0 ;
    ok := true ;

    // [ETAP] FOR TO
    for i := 1 to 5 do
        arr ( i ) := i * 2 ;

    // [ETAP] WHILE + BOOL (zmienna bool + and + not)
    while ok and not false do
        begin
            suma := suma + 1 ;
            if suma >= LIMIT then ok := false ;
        end ;

    // [ETAP] REPEAT UNTIL
    repeat
        suma := suma - 1 ;
    until suma = 0 ;

    // [ETAP] CASE OF
    case 2 of
        1 then writeln ( "jeden" ) ;
        2 , 3 then writeln ( "dwa albo trzy" ) ;
        else writeln ( "inne" ) ;
    end ;

    // [ETAP] PROCEDURE CALL (bez i z nawiasami)
    WypiszInfo ( "Koniec testu" ) ;
end .
