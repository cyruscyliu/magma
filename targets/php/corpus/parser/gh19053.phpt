<?php

abstract class GP {
    public abstract mixed $foo { get; }
}

class P extends GP {
    public mixed $foo = 1;
}

class C extends P {
    public mixed $foo { get => 2; }
}

$c = new C;
var_dump($c);

?>