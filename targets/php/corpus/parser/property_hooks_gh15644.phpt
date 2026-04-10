<?php

class C {
    public private(set) string $prop1 {
        set => $value;
    }
    public private(set) string $prop2 {
        get => $this->prop2;
    }
}

$c = new C();

try {
    $c->prop1 = 'hello world';
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

try {
    $c->prop2 = 'hello world';
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>