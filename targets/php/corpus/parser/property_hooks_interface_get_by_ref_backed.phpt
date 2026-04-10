<?php

interface I {
    public $prop { get; }
}

class A implements I {
    public $prop = 42 {
        get => $this->prop;
    }
}

$a = new A();
var_dump($a);

?>