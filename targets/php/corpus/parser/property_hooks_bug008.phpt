<?php

class Foo {
    private $_bar;
    public $bar {
        &get {
            echo __METHOD__, PHP_EOL;
            return $this->_bar;
        }
    }
}

$foo = new Foo;
$foo->bar = 'bar';

?>