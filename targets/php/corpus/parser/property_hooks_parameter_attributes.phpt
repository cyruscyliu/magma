<?php

class C {
    public $prop {
        set(#[SensitiveParameter] $value) {
            throw new Exception('Exception from $prop');
        }
    }
}

$c = new C();
try {
    $c->prop = 'secret';
} catch (Exception $e) {
    echo $e;
}

?>