<?php

#[Attribute(Attribute::TARGET_CLASS | Attribute::IS_REPEATABLE)]
class Attr {
    public function __construct(public Closure $value) {}
}

class E {
    private static function myMethod(string $foo) {
        echo "Called ", __METHOD__, PHP_EOL;
        var_dump($foo);
    }
}

#[Attr(E::myMethod(...))]
class C {
}

foreach ((new ReflectionClass(C::class))->getAttributes() as $reflectionAttribute) {
    ($reflectionAttribute->newInstance()->value)('abc');
}

?>