<?php

class P {}

class C extends P {
    public $prop {
        get {
            return parent::$prop::get();
        }
    }
}

$c = new C();
try {
    var_dump($c->prop);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>