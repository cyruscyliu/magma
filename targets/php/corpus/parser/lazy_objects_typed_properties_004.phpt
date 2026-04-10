<?php

class C {
    public int $a = 1;
    private int $_b = 1;
    public int $b {
        &get { $value = &$this->_b; return $value; }
    }
}

$reflector = new ReflectionClass(C::class);
$obj = $reflector->newLazyProxy(function () {
    return new C();
});

foreach ($obj as $key => &$value) {
    var_dump($key);
    try {
        $value = 'string';
    } catch (Error $e) {
        printf("%s: %s\n", $e::class, $e->getMessage());
    }
    $value = 2;
}

var_dump($obj);

?>