<?php

class C {
    const Closure = static function () {
        echo "called", PHP_EOL;
    };
}

var_dump(C::Closure);
(C::Closure)();

?>