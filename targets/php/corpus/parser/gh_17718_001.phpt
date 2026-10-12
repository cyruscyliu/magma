<?php

interface Foo {
    public static function __callStatic($method, $args);
}

Foo::bar();

?>