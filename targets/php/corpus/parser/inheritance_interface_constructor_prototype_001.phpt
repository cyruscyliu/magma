<?php

interface A {
    public function __construct(int $param);
}
interface B extends A {
    public function __construct(int|float $param);
}
class Test implements B {
    public function __construct(int $param) {}
}
new Test(42);

?>