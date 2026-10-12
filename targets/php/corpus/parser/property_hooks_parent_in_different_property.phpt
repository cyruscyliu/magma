<?php

class A {
    public $foo {
        get {
            return parent::$bar::get();
        }
    }
}

?>