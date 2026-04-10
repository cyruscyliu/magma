<?php

trait Foo {
    public string $bar {
        get => $this->getBar();
    }

    protected function getBar() {
        return 'bar';
    }
}

class A {
    use Foo;
}

class B {
    use Foo;
}

$a = new A();
$b = new B();
var_dump($a->bar);
var_dump($b->bar);

?>