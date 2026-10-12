<?php

class Test {
    public $prop {
        get {
            var_dump(__FUNCTION__);
            var_dump(__METHOD__);
            var_dump(__CLASS__);
            return null;
        }
    }
}

$test = new Test;
$test->prop;

?>