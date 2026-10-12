<?php

class Test {
    public $prop {
        get => $this->prop;
        set => $value;
    }

    public function __get($name) {
        echo __METHOD__, "\n";
        return 42;
    }

    public function __set($name, $value) {
        echo __METHOD__, "\n";
    }
}

$test = new Test;
var_dump($test->prop);
$test->prop = 42;
var_dump($test->prop);

?>