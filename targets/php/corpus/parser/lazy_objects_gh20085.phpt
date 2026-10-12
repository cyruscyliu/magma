<?php
class C {
    public int $a;
    public function __construct() {
        $this->a = 1;
    }
}
$obj = new C;
$reflector = new ReflectionClass(C::class);
foreach ($obj as &$value) {
    $obj = $reflector->newLazyGhost(function ($obj) {
        throw new Error;
    });
}
echo !obj;
?>