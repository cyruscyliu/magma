<?php

abstract class P {
    abstract protected(set) mixed $foo { get; set; }
}

class C1 extends P {
    public protected(set) mixed $foo { get => 2; set {} }
}

class C2 extends P {
    public mixed $foo = 1;

    static function foo($c) { return $c->foo += 1; }
}

var_dump(C2::foo(new C1));

?>