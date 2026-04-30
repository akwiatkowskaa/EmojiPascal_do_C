program SumaDoN ;

var
    n : integer ;
    i : integer ;
    suma : integer ;

begin
    writeln ( "Podaj n: " ) ;
    readln ( n ) ;

    suma := 0 ;

    for i := 1 to n do
        suma := suma + i ;

    writeln ( "Suma od 1 do n: " ) ;
    writeln ( suma ) ;
end .
