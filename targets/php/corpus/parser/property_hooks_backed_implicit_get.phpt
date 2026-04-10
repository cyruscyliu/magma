<?php

class C {
    public $prop {
        set {
            echo __METHOD__, "\n";
            $this->prop = $value;
        }
    }
}

$c = new C();
$c->prop = 42;
var_dump($c->prop);

?>