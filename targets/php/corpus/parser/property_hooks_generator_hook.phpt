<?php

class A {
    public $backed = 2 {
        get {
            yield 1;
            yield $this->backed;
            yield 3;
        }
    }

    public $virtual {
        get {
            yield 1;
            yield 2;
            yield 3;
        }
    }
}

$a = new A();
var_dump(iterator_to_array($a->backed));
var_dump(iterator_to_array($a->virtual));

?>