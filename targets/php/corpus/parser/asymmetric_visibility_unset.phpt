<?php

class Foo {
    public protected(set) string $bar;

    public private(set) string $secret;

    public function setBar($bar) {
        $this->bar = $bar;
    }

    public function setSecret($s) {
        $this->secret = $s;
    }

    public function unsetBarPrivate() {
        unset($this->bar);
    }
}

class FooChild extends Foo {
    public function unsetBarProtected() {
        unset($this->bar);
    }

    public function unsetSecret() {
        unset($this->secret);
    }
}

$foo = new FooChild();

$foo->setBar('bar');
try {
    unset($foo->bar);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($foo->bar ?? 'unset');

$foo->setBar('bar');
$foo->unsetBarPrivate();
var_dump($foo->bar ?? 'unset');

$foo->setBar('bar');
$foo->unsetBarProtected();
var_dump($foo->bar ?? 'unset');

$foo->setSecret('beep');
try {
    $foo->unsetSecret();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($foo->secret ?? 'unset');

?>