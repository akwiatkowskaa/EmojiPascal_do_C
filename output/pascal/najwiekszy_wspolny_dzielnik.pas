program NajwiekszyWspolnyDzielnik ;

var
    a : integer ;
    b : integer ;
    temp : integer ;

begin
    writeln ( "Podaj pierwsza liczbe: " ) ;
    readln ( a ) ;
    writeln ( "Podaj druga liczbe: " ) ;
    readln ( b ) ;

    while b <> 0 do
        begin
            temp := b ;
            b := a mod b ;
            a := temp ;
        end ;

    writeln ( "Najwiekszy wspolny dzielnik to: " ) ;
    writeln ( a ) ;
end .