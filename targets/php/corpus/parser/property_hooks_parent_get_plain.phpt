<?php

class P {
    public $prop = 42;
}

class C extends P {
    public $prop = 42 {
        get => parent::$prop::get();
    }
}

$c = new C();
var_dump($c->prop);

?>