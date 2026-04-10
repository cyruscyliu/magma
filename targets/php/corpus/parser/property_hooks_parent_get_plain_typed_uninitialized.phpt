<?php

class P {
    public int $prop;
}

class C extends P {
    public int $prop {
        get => parent::$prop::get();
    }
}

$c = new C();
try {
    var_dump($c->prop);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>