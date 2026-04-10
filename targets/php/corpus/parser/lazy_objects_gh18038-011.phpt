<?php

#[AllowDynamicProperties]
class RealInstance {
    public $_;
    public function __unset($name) {
        global $obj;
        var_dump(get_class($this)."::".__FUNCTION__);
        unset($this->$name);
    }
}

#[AllowDynamicProperties]
class Proxy extends RealInstance {
    public function __isset($name) {
        var_dump(get_class($this)."::".__FUNCTION__);
        unset($this->$name);
    }
}

$rc = new ReflectionClass(Proxy::class);

$obj = $rc->newLazyProxy(function () {
    echo "init\n";
    return new RealInstance;
});

$real = $rc->initializeLazyObject($obj);
unset($real->prop);
var_dump($obj);

?>