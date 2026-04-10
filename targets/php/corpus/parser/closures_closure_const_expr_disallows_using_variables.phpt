<?php

$foo = "bar";

const Closure = static function () use ($foo) {
    echo $foo, PHP_EOL;
};

var_dump(Closure);
(Closure)();

?>