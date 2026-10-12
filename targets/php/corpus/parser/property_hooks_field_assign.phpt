<?php

class Test {
    public $prop {
        set {
            $field ??= 42;
            var_dump($field);
            $field += 1;
            var_dump($field);
            $field -= 2;
            var_dump($field);
            $field *= 3;
            var_dump($field);
            $field++;
            var_dump($field);
            --$field;
            var_dump($field);
        }
    }
}

$test = new Test;
$test->prop = null;

?>