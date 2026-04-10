<?php

class A {
    public $prop = 42 {
        get {
            echo __METHOD__, "\n";
            return $this->prop;
        }
        set {
            echo __METHOD__, "\n";
            $this->prop = $value;
        }
    }
}

$a = new A();
var_dump($a);
var_dump($a->prop);
$a->prop = 43;
var_dump($a->prop);

?>