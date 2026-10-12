<?php

const Closure = static function () {
    static $x = [];
    static $i = 1;
    $i *= 2;
    $x[] = $i;
    var_dump($x);
};

var_dump(Closure);
(Closure)();
(Closure)();
(Closure)();
var_dump(Closure);

?>