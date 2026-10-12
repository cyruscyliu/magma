<?php

set_error_handler(function (int $errno, string $errstr, string $errfile, int $errline) {
    throw new \ErrorException($errstr, 0, $errno, $errfile, $errline);
});

trait Foo {
    public static function __callStatic($method, $args) {
        var_dump($method);
    }
}

try {
    Foo::bar();
} catch (ErrorException $e) {
    echo $e->getMessage(), PHP_EOL;
}

?>