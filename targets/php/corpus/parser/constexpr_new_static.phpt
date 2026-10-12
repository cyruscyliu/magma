<?php

class Foo {
    public static function singleton() {
        static $x = new static;
        return $x;
    }
}

$x = Foo::singleton();
$y = Foo::singleton();
var_dump($x, $y);

?>