<?php

class Foo {
    public $prop {
        get => parent::$prop::get();
    }
}

$foo = new Foo();
try {
    var_dump($foo->prop);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>