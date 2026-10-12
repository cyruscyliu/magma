<?php

class C {
    public $prop {
        get {
            echo __METHOD__, "\n";
            return $this->prop;
        }
    }
}

$c = new C();
$c->prop = 42;
var_dump($c->prop);

?>