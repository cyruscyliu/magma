<?php

abstract class A {
    abstract public $prop { get; set; }
}

class B extends A {
    public $prop;
}

?>
===DONE===