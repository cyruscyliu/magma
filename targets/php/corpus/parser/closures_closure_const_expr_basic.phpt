<?php

const Closure = static function () {
    echo "called", PHP_EOL;
};

var_dump(Closure);
(Closure)();

?>