<?php

#[AllowDynamicProperties]
class C {
    public $_;
    public function __unset($name) {
        var_dump(__METHOD__);
        unset($this->$name);
    }
}

$rc = new ReflectionClass(C::class);

$obj = $rc->newLazyProxy(function () {
    echo "init\n";
    return new C;
});

unset($obj->prop);
var_dump($obj);

?>