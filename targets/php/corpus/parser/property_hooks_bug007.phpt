<?php

class Test {
    public $prop = 0 {
        &get {
            echo __METHOD__, "\n";
            return $this->prop;
        }
    }
}

$test = new Test();
$test->prop = &$ref;

?>