<?php

class C {
    public static Closure $d = strrev(...);
}

var_dump(C::$d);
var_dump((C::$d)("abc"));


?>