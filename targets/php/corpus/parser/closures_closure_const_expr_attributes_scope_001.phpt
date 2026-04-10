<?php

#[Attribute(Attribute::TARGET_CLASS | Attribute::IS_REPEATABLE)]
class Attr {
    public function __construct(public Closure $value) {}
}

#[Attr(static function (C $c) {
    echo $c->secret, PHP_EOL;
})]
class C {
    public function __construct(
        private string $secret,
    ) {}
}

foreach ((new ReflectionClass(C::class))->getAttributes() as $reflectionAttribute) {
    ($reflectionAttribute->newInstance()->value)(new C('secret'));
}

?>