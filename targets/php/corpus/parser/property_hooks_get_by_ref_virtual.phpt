<?php

class Test {
    private $_prop;
    public $prop {
        &get => $this->_prop;
        set { $this->_prop = $value; }
    }
}

function inc(&$ref) {
    $ref++;
}

$test = new Test();
$test->prop = 42;

$prop = &$test->prop;
$prop++;
var_dump($test);
var_dump($test->prop);
unset($prop);

inc($test->prop);
var_dump($test);
var_dump($test->prop);

?>