<?php

trait T {
    public readonly int $prop;
}

readonly class C {
    use T;

    public function __construct()
    {
        $this->prop = 1;
    }
}

$c = new C();
var_dump($c->prop);

?>