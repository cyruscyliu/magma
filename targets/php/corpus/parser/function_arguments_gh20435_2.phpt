<?php

class C {
    public static function __callStatic($name, $args) {
        echo (new Exception())->__toString(), "\n\n";
    }
    public function __call($name, $args) {
        echo (new Exception())->__toString(), "\n\n";
    }
    public function __invoke(...$args) {
        echo (new Exception())->__toString(), "\n";
    }
}

$c = new C();
$c->foo(bar: 'bar');
C::foo(bar: 'bar');
$c(bar: 'bar');

?>