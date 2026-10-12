<?php

#[AllowDynamicProperties]
class C {
    public $_;
    public function __isset($name) {
        var_dump(__METHOD__);
        return isset($this->$name['']);
    }
    public function __get($name) {
        var_dump(__METHOD__);
        return $this->$name[''];
    }
}

$rc = new ReflectionClass(C::class);

$obj = $rc->newLazyProxy(function () {
    echo "init\n";
    return new C;
});

var_dump(isset($obj->prop['']));

?>