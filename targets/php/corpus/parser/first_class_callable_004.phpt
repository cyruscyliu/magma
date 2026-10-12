<?php
class Foo {
    private function method() {
        return __METHOD__;
    }

    public function bar()  {
        return $this->method(...);
    }
}

$foo = new Foo;
$bar = $foo->bar(...);

echo ($bar())();
?>