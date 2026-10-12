<?php

class C {
    public static Closure $d = static function () {
        echo "called", PHP_EOL;
    };
}

var_dump(C::$d);
(C::$d)();


?>