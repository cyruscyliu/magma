<?php
class Foo {
    public function bar()  {
        echo "OK";
    }
}

$foo = new Foo;
$bar = $foo->bar(...);

echo $bar();
?>