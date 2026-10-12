<?php

#[Attribute(Attribute::TARGET_CLASS | Attribute::IS_REPEATABLE)]
class Attr {
    public function __construct(public Closure $value) {}
}

#[Attr(static function (E $e) {
    echo $e->secret, PHP_EOL;
})]
class C {
}

class E {
    public function __construct(
        private string $secret,
    ) {}
}

foreach ((new ReflectionClass(C::class))->getAttributes() as $reflectionAttribute) {
    ($reflectionAttribute->newInstance()->value)(new E('secret'));
}

?>