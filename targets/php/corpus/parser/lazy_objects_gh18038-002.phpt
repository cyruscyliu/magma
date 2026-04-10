<?php

#[AllowDynamicProperties]
class RealInstance {
    public $_;
    public function __set($name, $value) {
        global $obj;
        var_dump(get_class($this)."::".__FUNCTION__);
        $obj->$name = $value * 2;
        unset($this->$name);
        $this->$name = $value * 2;
    }
}

#[AllowDynamicProperties]
class Proxy extends RealInstance {
}

$rc = new ReflectionClass(Proxy::class);

$obj = $rc->newLazyProxy(function () {
    echo "init\n";
    return new RealInstance;
});

$real = $rc->initializeLazyObject($obj);
$real->prop = 1;
var_dump($obj->prop);

?>