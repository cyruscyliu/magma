<?php

class P {
    public $prop;
}

class C extends P {
    public $prop {
        set {
            var_dump(parent::$prop::set($value));
        }
    }
}

$c = new C();
$c->prop = 42;

?>