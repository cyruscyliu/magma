<?php
class Base {
    public $y { get => 1; }
}

class Test extends Base {
    public $y {
        get => [new class {
            public $inner {get => __PROPERTY__;}
        }, parent::$y::get()];
    }
}

$test = new Test;
$y = $test->y;
var_dump($y);
var_dump($y[0]->inner);
?>