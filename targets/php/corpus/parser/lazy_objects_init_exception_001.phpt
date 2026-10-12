<?php

#[AllowDynamicProperties]
class C {
    public int $a;
    public $b;
}

$reflector = new ReflectionClass(C::class);

for ($i = 0; $i < 2; $i++) {
    $obj = $reflector->newLazyGhost(function ($obj) use ($i) {
        if ($i === 1) {
            throw new \Exception();
        }
    });
    $obj->c = 1;
}

?>