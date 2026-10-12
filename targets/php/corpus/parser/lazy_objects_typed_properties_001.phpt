<?php

class Test {
    public int $prop;
}

$name = new class {
    public function __toString() {
        return 'prop';
    }
};

$reflector = new ReflectionClass(Test::class);
$test = $reflector->newLazyProxy(function () {
    return new Test();
});
$ref = "foobar";
try {
    $test->$name =& $ref;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
var_dump($test);

?>