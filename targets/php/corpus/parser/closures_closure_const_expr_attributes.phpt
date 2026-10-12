<?php

#[Attribute(Attribute::TARGET_CLASS | Attribute::IS_REPEATABLE)]
class Attr {
    public function __construct(public Closure $value) {
        $value('foo');
    }
}

#[Attr(static function () { })]
#[Attr(static function (...$args) {
    var_dump($args);
})]
class C {}

foreach ((new ReflectionClass(C::class))->getAttributes() as $reflectionAttribute) {
    var_dump($reflectionAttribute->newInstance());
}

?>