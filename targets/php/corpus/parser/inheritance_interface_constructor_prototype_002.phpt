<?php

interface A {
    public function __construct(int|float $param);
}
interface B {
    public function __construct(int $param);
}
class X implements A, B {
    public function __construct(int|float $param) {}
}
class Y extends X {
    public function __construct(int $param) {}
}
new Y(42);

?>