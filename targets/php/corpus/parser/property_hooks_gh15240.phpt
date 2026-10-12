<?php

trait T {
    public $prop {
        set => $value;
    }
}

class C {
    use T;
}

$c = new C;
$c->prop = 42;
var_dump($c->prop);

?>