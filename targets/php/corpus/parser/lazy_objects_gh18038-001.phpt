<?php

#[AllowDynamicProperties]
class C {
    public $_;
    public function __set($name, $value) {
        var_dump(__METHOD__);
        $this->$name = $value * 2;
    }
}

$rc = new ReflectionClass(C::class);

$obj = $rc->newLazyProxy(function () {
    echo "init\n";
    return new C;
});

$obj->prop = 1;
var_dump($obj->prop);

?>