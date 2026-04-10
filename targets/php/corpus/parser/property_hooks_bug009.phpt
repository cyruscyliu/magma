<?php

class Foo {
    public $bar = [] {
        &get {
            echo __METHOD__ . "\n";
            return $this->bar;
        }
    }
}

$foo = new Foo;
$foo->bar[] = 'bar';
var_dump($foo);

?>