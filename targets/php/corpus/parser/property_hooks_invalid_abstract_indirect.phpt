<?php

abstract class A {
    public abstract $prop { get; }
}

class B extends A {
    public $prop { set {} }
}

?>