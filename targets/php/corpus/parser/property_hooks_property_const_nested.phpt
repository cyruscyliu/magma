<?php

class Test {
    public $prop {
        get => (function () {
            return __PROPERTY__;
        })();
    }
}

$test = new Test;
var_dump($test->prop);

?>