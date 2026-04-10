<?php

abstract class P {
    abstract public mixed $foo { get; }
}

class C1 extends P {
    public mixed $foo { get => 1; }
}

class GrandC1 extends C1 {
    public protected(set) mixed $foo { get => 2; set {} }
}

class C2 extends C1 {
    static function foo($c) { return $c->foo += 1; }
}

var_dump(C2::foo(new GrandC1));

?>