<?php

set_error_handler(function (int $errno, string $errstr, ?string $errfile = null, ?int $errline = null) {
    throw new \ErrorException($errstr, 0, $errno, $errfile, $errline);
});

trait Foo {
    public static function myMethod(string $foo) {
        echo "Called ", __METHOD__, PHP_EOL;
        var_dump($foo);
    }
}

function foo(Closure $c = Foo::myMethod(...)) {
    var_dump($c);
    $c("abc");  
}

try {
    foo();
} catch (ErrorException $e) {
    echo "Caught: ", $e->getMessage(), PHP_EOL;
}


?>