<?php

const Closure = [static function () {
    echo "called", PHP_EOL;
}, static function () {
    echo "also called", PHP_EOL;
}];

var_dump(Closure);

foreach (Closure as $closure) {
    $closure();
}

?>