<?php

abstract class Foo {
    abstract public static function __callStatic($method, $args);
}

Foo::bar();

?>