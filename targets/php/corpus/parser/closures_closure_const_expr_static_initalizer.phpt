<?php

function foo() {
    static $closure = static function () {
        echo "called", PHP_EOL;
    };

    var_dump($closure);
    $closure();
}

foo();

?>